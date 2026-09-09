from __future__ import annotations

from typing import Any


CONNECTION_SCHEMA_VERSION = "builddata.connection_registry.v1"


def build_connection_registry(
    *,
    scope: str,
    mapping_profile: dict[str, Any] | None,
    source_file: str = "",
    source_type: str = "table",
    target_type: str = "pim",
    root_model_id: int | str | None = None,
) -> dict[str, Any]:
    """Normalize product and building-element mapping profiles into one connection format."""
    profile = mapping_profile if isinstance(mapping_profile, dict) else {}
    levels = normalized_levels(profile.get("_levels"))
    connections = [
        connection_from_rule(scope, profile_key, rule)
        for profile_key, rule in profile.items()
        if not str(profile_key).startswith("_") and isinstance(rule, dict)
    ]
    connections = [connection for connection in connections if connection]
    ignored_count = sum(1 for connection in connections if connection.get("status") == "ignored")
    active_count = sum(1 for connection in connections if connection.get("status") == "active")
    return {
        "schema": CONNECTION_SCHEMA_VERSION,
        "scope": scope,
        "source": {
            "type": source_type,
            "file": source_file,
        },
        "target": {
            "type": target_type,
            "root_model_id": root_model_id or "",
        },
        "summary": {
            "connections": len(connections),
            "active_connections": active_count,
            "ignored_connections": ignored_count,
            "levels": len(levels),
        },
        "levels": levels,
        "connections": connections,
    }


def normalized_levels(raw_levels: Any) -> list[dict[str, Any]]:
    if not isinstance(raw_levels, dict):
        return []
    result: list[dict[str, Any]] = []
    for level_key, config in raw_levels.items():
        if not isinstance(config, dict):
            continue
        result.append(
            {
                "level_key": str(level_key),
                "table": str(config.get("table") or ""),
                "id_column": str(config.get("id_column") or ""),
                "parent_id_column": str(config.get("parent_id_column") or ""),
                "level_name_field": str(config.get("level_name_field") or ""),
            }
        )
    return result


def connection_from_rule(scope: str, profile_key: Any, rule: dict[str, Any]) -> dict[str, Any] | None:
    target_path = str(rule.get("target_path") or profile_key or "")
    if not target_path:
        return None
    source_column = str(rule.get("source_column") or rule.get("column") or source_column_from_profile_key(profile_key))
    table = str(rule.get("table") or "")
    connection = {
        "id": stable_connection_id(scope, table, source_column, target_path, rule.get("level")),
        "scope": scope,
        "status": "ignored" if target_path == "ignore" else "active",
        "source": {
            "table": table,
            "column": source_column,
        },
        "target": {
            "path": "" if target_path == "ignore" else target_path,
            "label": str(rule.get("target_label") or rule.get("field_label") or ""),
            "group": str(rule.get("target_group") or rule.get("field_group") or rule.get("group") or ""),
            "value_kind": str(rule.get("target_value_kind") or rule.get("field_kind") or rule.get("value_kind") or ""),
            "unit": str(rule.get("target_unit") or rule.get("unit") or ""),
        },
        "level": str(rule.get("level") or ""),
        "cleanup": normalized_cleanup(rule.get("cleanup")),
        "choice_map": normalized_choice_map(rule.get("choice_map") or rule.get("value_map")),
    }
    return connection


def normalized_cleanup(cleanup: Any) -> dict[str, Any]:
    if not isinstance(cleanup, dict):
        return {}
    keys = (
        "trim",
        "parseNumber",
        "decimalComma",
        "removeText",
        "replaceFrom",
        "replaceTo",
        "splitBy",
        "splitPart",
        "unit",
        "targetUnit",
        "unitSourceColumn",
        "unitConversionFactor",
    )
    return {key: cleanup.get(key) for key in keys if cleanup.get(key) not in (None, "")}


def normalized_choice_map(choice_map: Any) -> dict[str, Any]:
    if not isinstance(choice_map, dict):
        return {}
    return {str(key): value for key, value in choice_map.items()}


def source_column_from_profile_key(profile_key: Any) -> str:
    return str(profile_key).split("::extract::", 1)[0]


def stable_connection_id(*parts: Any) -> str:
    clean_parts = [str(part or "").strip().lower() for part in parts if part not in (None, "")]
    return "::".join(clean_parts)
