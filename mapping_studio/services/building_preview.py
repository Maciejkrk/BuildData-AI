from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from collections.abc import Iterable, Iterator
from typing import Any

from data_master_app.mapping import apply_cleanup
from mapping_studio.models import PimModelBundle, ProductReferenceIndex
from mapping_studio.services.source_reader import SourceTable
from mapping_studio.services.normalization import lookup_key
from mapping_studio.services.product_reference import product_identity


BUILDING_ELEMENT_ID_START = 910000
BUILDING_ELEMENT_TYPE_ID = 1


def preview_building_elements(
    rows: Iterable[dict[str, Any]],
    mapping: dict[str, str],
    product_index: ProductReferenceIndex | None,
    *,
    preview_offset: int = 0,
    preview_limit: int | None = None,
    stop_after_preview_window: bool = False,
    preview_roles: dict[str, str] | None = None,
) -> dict[str, Any]:
    systems: dict[str, dict[str, Any]] = {}
    unresolved_products: list[dict[str, Any]] = []
    system_order: list[str] = []
    system_indexes: dict[str, int] = {}
    stopped_after_window = False
    preview_offset = max(preview_offset, 0)
    preview_limit = max(preview_limit, 1) if preview_limit is not None else None
    preview_roles = preview_roles or preview_roles_from_mapping_profile(mapping if isinstance(mapping, dict) else {})
    for source_index, row in enumerate(rows, start=1):
        mapped = apply_simple_mapping(row, mapping)
        system_name = role_value(mapped, preview_roles, "system_name") or first_system_value(mapped) or first_system_value(row) or "System bez nazwy"
        variant_name = role_value(mapped, preview_roles, "variant_name") or first_variant_value(mapped) or first_variant_value(row) or "Wariant domyślny"
        layer_name = role_value(mapped, preview_roles, "layer_name") or first_layer_value(mapped) or first_layer_value(row) or "Warstwa bez nazwy"
        product_key = role_value(mapped, preview_roles, "product") or first_product_value(mapped) or first_product_value(row)
        system_key = str(system_name)
        if system_key not in system_indexes:
            system_indexes[system_key] = len(system_order)
            system_order.append(system_key)
        system_index = system_indexes[system_key]
        if stop_after_preview_window and preview_limit is not None and system_index >= preview_offset + preview_limit:
            stopped_after_window = True
            break
        if system_index < preview_offset:
            continue
        if preview_limit is not None and system_index >= preview_offset + preview_limit:
            continue

        system = systems.setdefault(system_key, {"name": system_name, "variants": {}})
        variant = system["variants"].setdefault(str(variant_name), {"name": variant_name, "layers": {}})
        layer = variant["layers"].setdefault(str(layer_name), {"name": layer_name, "source_rows": [], "products": [], "features": []})
        layer["source_rows"].append(source_index)
        merge_features(layer["features"], row_features(mapped, source_index))

        for product_value in product_values(product_key):
            reference = resolve_product_reference(product_value, product_index)
            match = reference.get("product") if reference else None
            product_entry = {
                "raw": product_value,
                "resolved": bool(match),
                "product_id": match.get("Id") if match else None,
                "product_name": product_identity(match)[0] if match else "",
                "variant_hash": reference.get("variant_hash") if reference else "",
                "variant_label": reference.get("variant_label") if reference else "",
                "variant_row_i": reference.get("variant_row_i") if reference else None,
                "variant_scope": product_variant_scope(reference),
                "variant_scope_label": product_variant_scope_label(reference),
                "identity_source": reference.get("source") if reference else product_identity_source(product_value, product_index, match),
            }
            layer["products"].append(product_entry)
            if not match:
                unresolved_products.append({"row": source_index, "value": product_value, "layer": layer_name})

    return {
        "systems": normalize_tree(systems),
        "quality": {
            "systems": len(system_order),
            "preview_offset": preview_offset,
            "preview_limit": preview_limit,
            "preview_systems_count": len(systems),
            "systems_count_is_exact": not stopped_after_window,
            "has_previous": preview_offset > 0,
            "has_next": preview_limit is not None and len(system_order) > preview_offset + len(systems),
            "unresolved_products": unresolved_products,
            "unresolved_products_count": len(unresolved_products),
            "product_reference_loaded": product_index is not None and product_index.products_count > 0,
        },
    }


def first_system_value(row: dict[str, Any]) -> Any:
    return first_value_by_role(
        row,
        (
            "building_element.name.value",
            "building_element.nazwa_systemu.value",
            "system.name",
            "system_name",
            "Nazwa systemu",
            "System",
        ),
        ("nazwasystemu", "systemname", "system"),
        ("produkt", "product", "wariant", "variant", "warstwa", "layer"),
    )


def first_variant_value(row: dict[str, Any]) -> Any:
    return first_value_by_role(
        row,
        (
            "building_element.variant_name.value",
            "building_element.nazwa_wariantu.value",
            "variant_name",
            "Wariant",
            "Nazwa wariantu",
        ),
        ("nazwawariantu", "variantname", "wariant", "variant"),
        ("produkt", "product", "warstwa", "layer"),
    )


def first_layer_value(row: dict[str, Any]) -> Any:
    return first_value_by_role(
        row,
        (
            "building_element.layer_name.value",
            "building_element.nazwa_warstwy.value",
            "layer_name",
            "Nazwa warstwy",
            "Warstwa",
        ),
        ("nazwawarstwy", "layername", "warstwa", "layer"),
        ("produkt", "product", "wariant", "variant"),
    )


def first_product_value(row: dict[str, Any]) -> Any:
    return first_value_by_role(
        row,
        (
        "building_element.product.value",
        "building_element.produkt.value",
        "Kod produktu",
        "Nazwa produktu",
        "Produkt",
        "Produkty",
        ),
        ("nazwaproduktu", "kodproduktu", "productname", "productcode", "produkty", "produkt", "product"),
        (),
    )


def first_value_by_role(
    row: dict[str, Any],
    preferred: tuple[str, ...],
    include_markers: tuple[str, ...],
    exclude_markers: tuple[str, ...],
) -> Any:
    for key in preferred:
        value = row.get(key)
        if value not in (None, ""):
            return value
    for key, value in row.items():
        if str(key).startswith("_") or value in (None, ""):
            continue
        normalized_key = field_lookup_key(key)
        if any(marker in normalized_key for marker in include_markers) and not any(marker in normalized_key for marker in exclude_markers):
            return value
    return None


def field_lookup_key(key: Any) -> str:
    return lookup_key(str(key).replace(".", "_"))


STRUCTURE_FIELD_KEYS = {
    "buildingelementnamevalue",
    "buildingelementnazwasystemuvalue",
    "systemname",
    "nazwasystemu",
    "system",
    "buildingelementvariantnamevalue",
    "buildingelementnazwawariantuvalue",
    "variantname",
    "nazwawariantu",
    "wariant",
    "variant",
    "buildingelementlayernamevalue",
    "buildingelementnazwawarstwyvalue",
    "layername",
    "nazwawarstwy",
    "warstwa",
    "layer",
    "buildingelementproductvalue",
    "buildingelementproduktvalue",
    "productname",
    "productcode",
    "nazwaproduktu",
    "kodproduktu",
    "produkty",
    "produkt",
    "product",
}


def row_features(row: dict[str, Any], source_index: int) -> list[dict[str, Any]]:
    features: list[dict[str, Any]] = []
    for key, value in row.items():
        if str(key).startswith("_") or value in (None, ""):
            continue
        normalized_key = field_lookup_key(key)
        if normalized_key in STRUCTURE_FIELD_KEYS:
            continue
        features.append(
            {
                "key": str(key),
                "label": feature_label(key),
                "value": value,
                "source_row": source_index,
            }
        )
    return features


def merge_features(target: list[dict[str, Any]], features: list[dict[str, Any]]) -> None:
    seen = {(item.get("key"), str(item.get("value"))) for item in target}
    for feature in features:
        identity = (feature.get("key"), str(feature.get("value")))
        if identity not in seen:
            target.append(feature)
            seen.add(identity)


def feature_label(key: Any) -> str:
    text = str(key)
    if text.startswith("building_element."):
        text = text.removeprefix("building_element.")
    if text.endswith(".value"):
        text = text.removesuffix(".value")
    return text.replace("_", " ").replace(".", " / ")


def preview_building_elements_from_tables(
    tables: list[SourceTable],
    mapping_profile: dict[str, Any],
    product_index: ProductReferenceIndex | None,
    *,
    preview_offset: int = 0,
    preview_limit: int | None = None,
) -> dict[str, Any]:
    if not mapping_profile:
        return preview_building_elements(
            tables[0].rows if tables else [],
            {},
            product_index,
            preview_offset=preview_offset,
            preview_limit=preview_limit,
        )
    if is_legacy_mapping(mapping_profile):
        return preview_building_elements(
            tables[0].rows if tables else [],
            mapping_profile,
            product_index,
            preview_offset=preview_offset,
            preview_limit=preview_limit,
        )

    rows = iter_mapped_rows_from_profile(tables, mapping_profile)
    return preview_building_elements(
        rows,
        {},
        product_index,
        preview_offset=preview_offset,
        preview_limit=preview_limit,
        preview_roles=preview_roles_from_mapping_profile(mapping_profile),
    )


def is_legacy_mapping(mapping_profile: dict[str, Any]) -> bool:
    return all(isinstance(value, str) for value in mapping_profile.values())


def mapped_rows_from_profile(tables: list[SourceTable], mapping_profile: dict[str, Any]) -> list[dict[str, Any]]:
    return list(iter_mapped_rows_from_profile(tables, mapping_profile))


def iter_mapped_rows_from_profile(tables: list[SourceTable], mapping_profile: dict[str, Any]) -> Iterator[dict[str, Any]]:
    tables_by_name = {table.name: table for table in tables}
    fallback_table = tables[0] if tables else SourceTable("data", [])
    levels = mapping_profile.get("_levels") if isinstance(mapping_profile.get("_levels"), dict) else {}
    if should_join_levels_by_parent(tables_by_name, levels):
        yield from iter_joined_mapped_rows_from_profile(tables_by_name, fallback_table, mapping_profile, levels)
        return

    row_count = max((len(table.rows) for table in tables), default=0)
    for index in range(row_count):
        mapped: dict[str, Any] = {}
        source_context: dict[str, Any] = {}
        level_ids: dict[str, dict[str, Any]] = {}
        for level_key, config in levels.items():
            if not isinstance(config, dict):
                continue
            table = tables_by_name.get(str(config.get("table") or "")) or fallback_table
            if index >= len(table.rows):
                continue
            source_row = table.rows[index]
            level_data: dict[str, Any] = {}
            id_column = config.get("id_column")
            if id_column:
                level_data["id"] = source_row.get(str(id_column))
            parent_id_column = config.get("parent_id_column")
            if parent_id_column:
                level_data["parent_id"] = source_row.get(str(parent_id_column))
            if level_data:
                level_ids[str(level_key)] = level_data
        for target_path, rule in mapping_profile.items():
            if str(target_path).startswith("_") or not isinstance(rule, dict):
                continue
            table = tables_by_name.get(str(rule.get("table") or "")) or fallback_table
            if index >= len(table.rows):
                continue
            source_row = table.rows[index]
            column = rule.get("column")
            if not column:
                continue
            value = source_row.get(str(column))
            cleanup = rule.get("cleanup") or {}
            value = apply_cleanup(value, cleanup, source_row)
            if value not in (None, ""):
                mapped[target_path] = value
            source_context[target_path] = {
                "table": table.name,
                "column": column,
                "row": index + 1,
            }
        if mapped:
            mapped["_source_context"] = source_context
            if level_ids:
                mapped["_level_ids"] = level_ids
            yield mapped


def should_join_levels_by_parent(tables_by_name: dict[str, SourceTable], levels: dict[str, Any]) -> bool:
    level_tables = {
        str(config.get("table") or "")
        for config in levels.values()
        if isinstance(config, dict) and config.get("table")
    }
    return len(level_tables) > 1 and any(
        isinstance(config, dict)
        and config.get("parent_id_column")
        and str(config.get("table") or "") in tables_by_name
        for config in levels.values()
    )


def preview_roles_from_mapping_profile(mapping_profile: dict[str, Any]) -> dict[str, str]:
    explicit = mapping_profile.get("_preview_roles")
    if isinstance(explicit, dict):
        return {str(key): str(value) for key, value in explicit.items() if value}
    rules = [
        (str(target), rule)
        for target, rule in mapping_profile.items()
        if not str(target).startswith("_") and isinstance(rule, dict)
    ]
    levels = mapping_profile.get("_levels") if isinstance(mapping_profile.get("_levels"), dict) else {}
    ordered_level_keys = [str(key) for key in levels.keys()]
    root_level = next((key for key in ordered_level_keys if not isinstance(levels.get(key), dict) or not levels[key].get("parent_id_column")), ordered_level_keys[0] if ordered_level_keys else "")
    child_levels = [key for key in ordered_level_keys if key != root_level]
    product_level = next((str(rule.get("level") or "") for target, rule in rules if is_product_rule(target, rule)), "")
    layer_level = product_level or next((level for level in child_levels if select_role_field(rules, level, ("nazwa", "name", "warstwa", "layer"), prefer_non_product=True)), "")
    variant_level = ""
    if layer_level and layer_level in ordered_level_keys:
        layer_index = ordered_level_keys.index(layer_level)
        if layer_index > 0:
            variant_level = ordered_level_keys[layer_index - 1]
    if variant_level == root_level:
        variant_level = root_level if select_role_field(rules, root_level, ("wariant", "variant"), prefer_non_product=True) else ""
    elif not variant_level and child_levels:
        variant_level = child_levels[0]
    roles: dict[str, str] = {}
    roles["system_name"] = select_role_field(rules, root_level, ("nazwa", "name", "system", "element"), prefer_non_product=True)
    if variant_level:
        roles["variant_name"] = select_role_field(rules, variant_level, ("nazwa", "name", "wariant", "variant"), prefer_non_product=True)
    if layer_level:
        roles["layer_name"] = select_role_field(rules, layer_level, ("nazwa", "name", "warstwa", "layer"), prefer_non_product=True)
    if not roles.get("variant_name"):
        roles["variant_name"] = select_any_role_field(rules, ("wariant", "variant"))
    if not roles.get("layer_name"):
        roles["layer_name"] = select_any_role_field(rules, ("warstwa", "layer"))
    roles["product"] = select_role_field(rules, layer_level, ("produkt", "product"), product_only=True) or select_role_field(rules, "", ("produkt", "product"), product_only=True) or select_any_role_field(rules, ("produkt", "product"))
    return {key: value for key, value in roles.items() if value}


def is_product_rule(target: str, rule: dict[str, Any]) -> bool:
    return str(rule.get("field_kind") or "") == "product_ref" or field_rule_matches(target, rule, ("produkt", "product"))


def select_role_field(
    rules: list[tuple[str, dict[str, Any]]],
    level_key: str,
    markers: tuple[str, ...],
    *,
    prefer_non_product: bool = False,
    product_only: bool = False,
) -> str:
    candidates = [(target, rule) for target, rule in rules if not level_key or str(rule.get("level") or "") == level_key]
    if product_only:
        product = next((target for target, rule in candidates if str(rule.get("field_kind") or "") == "product_ref"), "")
        if product:
            return product
    for marker in markers:
        marked = next((target for target, rule in candidates if field_rule_matches(target, rule, (marker,))), "")
        if marked:
            return marked
    if prefer_non_product:
        return next((target for target, rule in candidates if str(rule.get("field_kind") or "") != "product_ref"), "")
    return candidates[0][0] if candidates else ""


def select_any_role_field(rules: list[tuple[str, dict[str, Any]]], markers: tuple[str, ...]) -> str:
    return next((target for target, rule in rules if field_rule_matches(target, rule, markers)), "")


def field_rule_matches(target: str, rule: dict[str, Any], markers: tuple[str, ...]) -> bool:
    haystack = field_lookup_key(" ".join([target, str(rule.get("field_label") or ""), str(rule.get("column") or "")]))
    return any(marker in haystack for marker in markers)


def role_value(row: dict[str, Any], roles: dict[str, str], role: str) -> Any:
    key = roles.get(role)
    value = row.get(key) if key else None
    return value if value not in (None, "") else None


def iter_joined_mapped_rows_from_profile(
    tables_by_name: dict[str, SourceTable],
    fallback_table: SourceTable,
    mapping_profile: dict[str, Any],
    levels: dict[str, Any],
) -> Iterator[dict[str, Any]]:
    ordered_levels = [(str(key), config) for key, config in levels.items() if isinstance(config, dict)]
    if not ordered_levels:
        return
    root_key, root_config = next(
        ((key, config) for key, config in ordered_levels if not config.get("parent_id_column")),
        ordered_levels[0],
    )
    root_table = tables_by_name.get(str(root_config.get("table") or "")) or fallback_table
    child_levels = [(key, config) for key, config in ordered_levels if key != root_key]
    for root_index, root_row in enumerate(root_table.rows):
        mapped, source_context = mapped_values_for_level(mapping_profile, tables_by_name, fallback_table, root_key, root_row, root_index)
        level_ids = level_ids_for_row(root_key, root_config, root_row)
        candidates = row_candidate_values(root_row, mapped)
        combinations = [(mapped, source_context, level_ids, candidates)]
        for level_key, config in child_levels:
            table = tables_by_name.get(str(config.get("table") or "")) or fallback_table
            parent_id_column = str(config.get("parent_id_column") or "")
            next_combinations: list[tuple[dict[str, Any], dict[str, Any], dict[str, dict[str, Any]], set[str]]] = []
            for base_mapped, base_context, base_level_ids, parent_candidates in combinations:
                if parent_id_column:
                    matching_rows = [
                        (index, row)
                        for index, row in enumerate(table.rows)
                        if normalized_match_value(row.get(parent_id_column)) in parent_candidates
                    ]
                else:
                    matching_rows = [(root_index, table.rows[root_index])] if root_index < len(table.rows) else []
                if not matching_rows:
                    next_combinations.append((base_mapped, base_context, base_level_ids, parent_candidates))
                    continue
                for child_index, child_row in matching_rows:
                    child_mapped, child_context = mapped_values_for_level(
                        mapping_profile,
                        tables_by_name,
                        fallback_table,
                        level_key,
                        child_row,
                        child_index,
                    )
                    if not child_mapped:
                        continue
                    merged = {**base_mapped, **child_mapped}
                    merged_context = {**base_context, **child_context}
                    merged_level_ids = {**base_level_ids, **level_ids_for_row(level_key, config, child_row)}
                    child_candidates = row_candidate_values(child_row, child_mapped)
                    next_combinations.append((merged, merged_context, merged_level_ids, child_candidates))
            combinations = next_combinations
        for mapped, source_context, level_ids, _candidates in combinations:
            if not mapped:
                continue
            mapped["_source_context"] = source_context
            if level_ids:
                mapped["_level_ids"] = level_ids
            yield mapped


def mapped_values_for_level(
    mapping_profile: dict[str, Any],
    tables_by_name: dict[str, SourceTable],
    fallback_table: SourceTable,
    level_key: str,
    source_row: dict[str, Any],
    source_index: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    mapped: dict[str, Any] = {}
    source_context: dict[str, Any] = {}
    for target_path, rule in mapping_profile.items():
        if str(target_path).startswith("_") or not isinstance(rule, dict):
            continue
        rule_level = str(rule.get("level") or "")
        table = tables_by_name.get(str(rule.get("table") or "")) or fallback_table
        if rule_level and rule_level != level_key:
            continue
        if not rule_level and table.rows and source_row not in table.rows:
            continue
        column = rule.get("column")
        if not column:
            continue
        value = source_row.get(str(column))
        value = apply_cleanup(value, rule.get("cleanup") or {}, source_row)
        if value not in (None, ""):
            mapped[target_path] = value
        source_context[target_path] = {
            "table": table.name,
            "column": column,
            "row": source_index + 1,
        }
    return mapped, source_context


def level_ids_for_row(level_key: str, config: dict[str, Any], source_row: dict[str, Any]) -> dict[str, dict[str, Any]]:
    level_data: dict[str, Any] = {}
    id_column = config.get("id_column")
    if id_column:
        level_data["id"] = source_row.get(str(id_column))
    parent_id_column = config.get("parent_id_column")
    if parent_id_column:
        level_data["parent_id"] = source_row.get(str(parent_id_column))
    return {level_key: level_data} if level_data else {}


def row_candidate_values(source_row: dict[str, Any], mapped: dict[str, Any]) -> set[str]:
    values = set()
    for value in list(source_row.values()) + list(mapped.values()):
        normalized = normalized_match_value(value)
        if normalized:
            values.add(normalized)
    return values


def normalized_match_value(value: Any) -> str:
    return lookup_key(value) if value not in (None, "") else ""


def apply_simple_mapping(row: dict[str, Any], mapping: dict[str, str]) -> dict[str, Any]:
    if not mapping:
        return dict(row)
    mapped: dict[str, Any] = {}
    for source, target in mapping.items():
        if target and target != "ignore":
            mapped[target] = row.get(source)
    return mapped


def resolve_product_reference(value: Any, product_index: ProductReferenceIndex | None) -> dict[str, Any] | None:
    if product_index is None:
        return None
    key = lookup_key(value)
    product = product_index.by_id.get(str(value))
    if product:
        return {"product": product, "source": "id", "variant_hash": "", "variant_row_i": None}
    variant = product_index.by_variant.get(key)
    if variant:
        return {
            "product": variant.get("product"),
            "source": "variant",
            "variant_hash": variant.get("hash") or "",
            "variant_label": variant_label(variant),
            "variant_row_i": variant.get("row_i"),
        }
    product = product_index.by_code.get(key)
    if product:
        return {"product": product, "source": "code", "variant_hash": "", "variant_row_i": None}
    product = product_index.by_name.get(key)
    if product:
        return {"product": product, "source": "name", "variant_hash": "", "variant_row_i": None}
    return None


def variant_label(variant: dict[str, Any]) -> str:
    aliases = variant.get("aliases") or []
    return str(aliases[0]) if aliases else ""


def product_variant_scope(reference: dict[str, Any] | None) -> str:
    if not reference:
        return "unresolved"
    return "specific_variant" if reference.get("variant_hash") else "all_variants"


def product_variant_scope_label(reference: dict[str, Any] | None) -> str:
    scope = product_variant_scope(reference)
    if scope == "specific_variant":
        return "tylko wskazany wariant"
    if scope == "all_variants":
        return "wszystkie warianty produktu"
    return "brak dopasowania"


def resolve_product(value: Any, product_index: ProductReferenceIndex | None) -> dict[str, Any] | None:
    reference = resolve_product_reference(value, product_index)
    return reference.get("product") if reference else None


def product_values(value: Any) -> list[str]:
    if value in (None, ""):
        return []
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            result.extend(product_values(item))
        return result
    text = str(value).strip()
    if not text:
        return []
    return [item.strip() for item in re.split(r"[,;|\n]+", text) if item.strip()]


def product_identity_source(value: Any, product_index: ProductReferenceIndex | None, match: dict[str, Any] | None) -> str:
    if product_index is None:
        return "raw"
    if not match:
        return "unresolved"
    key = lookup_key(value)
    if product_index.by_id.get(str(value)) is match:
        return "id"
    if product_index.by_code.get(key) is match:
        return "code"
    if product_index.by_name.get(key) is match:
        return "name"
    return "unknown"


def normalize_tree(systems: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for system in systems.values():
        variants = []
        for variant in system["variants"].values():
            layers = list(variant["layers"].values())
            variants.append({"name": variant["name"], "layers": layers})
        result.append({"name": system["name"], "variants": variants})
    return result


def convert_building_elements_from_tables(
    filename: str,
    content: bytes,
    tables: list[SourceTable],
    mapping_profile: dict[str, Any],
    model: PimModelBundle,
    product_index: ProductReferenceIndex | None,
    output_root: Path,
) -> dict[str, Any]:
    rows = mapped_rows_from_profile(tables, mapping_profile)
    field_by_key: dict[str, Any] = {}
    for field in model.fields:
        field_by_key[field.key] = field
        field_by_key[field.key.replace(" ", "_")] = field
    relation_by_key = {relation.key: relation for relation in model.relations}
    root_key = f"model.{model.root_model_id}"
    levels = mapping_profile.get("_levels") if isinstance(mapping_profile.get("_levels"), dict) else {}
    root_level = levels.get(root_key, {}) if isinstance(levels.get(root_key), dict) else {}
    root_name_field = root_level.get("level_name_field") or root_level.get("id_column") or next((field.key for field in model.fields if field.parent_relation_key is None), "")

    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        root_id = level_identity_value(row, root_key, "id")
        name = root_id or row.get(root_name_field) or row.get("building_element.name.value") or row.get("system.name") or "Building element"
        grouped.setdefault(str(name), []).append(row)

    elements = [
        build_element_entry(name, element_rows, index, field_by_key, relation_by_key, product_index, model.root_model_id)
        for index, (name, element_rows) in enumerate(grouped.items(), start=1)
    ]
    payload = {"buildingElementsCount": len(elements), "buildingElements": elements}
    job_id = stable_job_id("building-elements", filename, content, json.dumps(mapping_profile, sort_keys=True, ensure_ascii=False))
    output_dir = output_root / job_id
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "building_elements.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    report = {
        "source_filename": filename,
        "building_elements_count": len(elements),
        "product_identity": mapping_profile.get("_product_identity") or {},
    }
    (output_dir / "building_elements_mapping_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "status": "building_elements_converted",
        "job_id": job_id,
        "building_elements_count": len(elements),
        "files": {
            "building_elements_json": f"/outputs/{job_id}/building_elements.json",
            "mapping_report_json": f"/outputs/{job_id}/building_elements_mapping_report.json",
        },
        "report": report,
    }


def build_element_entry(
    name: str,
    rows: list[dict[str, Any]],
    index: int,
    field_by_key: dict[str, Any],
    relation_by_key: dict[str, Any],
    product_index: ProductReferenceIndex | None,
    model_id: int,
) -> dict[str, Any]:
    attrs: list[dict[str, Any]] = []
    relation_hashes: dict[tuple[str, str], str] = {}
    for row_index, row in enumerate(rows):
        for key, value in row.items():
            if key.startswith("_") or value in (None, ""):
                continue
            field = field_by_key.get(key)
            if not field:
                continue
            parent_attribute_id = 0
            parent_hash = ""
            row_hash = None
            relation_key = field.parent_relation_key
            if relation_key:
                relation = relation_by_key.get(relation_key)
                parent_attribute_id = relation.attribute_id if relation else 0
                relation_value = level_identity_value(row, relation_key, "id") or relation_identity_value(row, relation_key, field_by_key) or str(row_index + 1)
                row_hash = relation_hashes.setdefault((relation_key, relation_value), stable_hash(relation_key, relation_value))
                parent_relation_key = relation.parent_relation_key if relation else None
                if parent_relation_key:
                    parent_value = level_identity_value(row, relation_key, "parent_id") or relation_identity_value(row, parent_relation_key, field_by_key) or "root"
                    parent_hash = relation_hashes.setdefault((parent_relation_key, parent_value), stable_hash(parent_relation_key, parent_value))
            add_field_attrs(attrs, field, value, product_index, parent_attribute_id=parent_attribute_id, row_hash=row_hash, parent_hash=parent_hash, row_i=row_index)
    return {
        "Id": BUILDING_ELEMENT_ID_START + index,
        "elementTypeId": BUILDING_ELEMENT_TYPE_ID,
        "ModelType": model_id,
        "dataVersions": [
            {
                "VersionId": 1,
                "productAttributes": attrs,
                "filesAttributes": [],
                "colorsAttributes": [],
            }
        ],
    }


def relation_identity_value(row: dict[str, Any], relation_key: str, field_by_key: dict[str, Any]) -> str:
    for key, value in row.items():
        field = field_by_key.get(key)
        if field and field.parent_relation_key == relation_key and value not in (None, ""):
            return str(value)
    return ""


def level_identity_value(row: dict[str, Any], level_key: str, kind: str) -> str:
    value = ((row.get("_level_ids") or {}).get(level_key) or {}).get(kind)
    return "" if value in (None, "") else str(value)


def add_field_attrs(
    attrs: list[dict[str, Any]],
    field: Any,
    value: Any,
    product_index: ProductReferenceIndex | None,
    *,
    parent_attribute_id: int = 0,
    row_hash: str | None = None,
    parent_hash: str = "",
    row_i: int = 0,
) -> None:
    values = product_values(value) if str(field.kind) in {"product_ref", "multi_choice"} else [value]
    for item in values:
        add_attr(
            attrs,
            field.attribute_id,
            parent_attribute_id=parent_attribute_id,
            row_hash=row_hash,
            parent_hash=parent_hash,
            row_i=row_i,
            **attr_payload_for_value(field, item, product_index),
        )


def attr_payload_for_value(field: Any, value: Any, product_index: ProductReferenceIndex | None) -> dict[str, Any]:
    if str(field.kind) == "product_ref":
        reference = resolve_product_reference(value, product_index)
        match = reference.get("product") if reference else None
        if match and str(match.get("Id") or "").isdigit():
            return {"int_value": int(match["Id"]), "varchar": str(reference.get("variant_hash") or "")}
        return {"varchar": str(value)}
    if str(field.kind) == "number":
        number = parse_number(value)
        return {"number": number} if number is not None else {"varchar": str(value)}
    if str(field.kind) == "boolean":
        return {"boolean": parse_bool(value)}
    option_id = option_id_for_value(field, value)
    if option_id is not None:
        return {"int_value": option_id, "boolean": True}
    return {"varchar": str(value)}


def add_attr(
    attrs: list[dict[str, Any]],
    attribute_id: int,
    *,
    varchar: str | None = None,
    text: str | None = None,
    int_value: int | None = None,
    number: float | None = None,
    boolean: bool = False,
    parent_attribute_id: int = 0,
    row_hash: str | None = None,
    parent_hash: str = "",
    row_i: int = 0,
) -> None:
    attrs.append(
        {
            "AttributeId": attribute_id,
            "hash": row_hash,
            "parentHash": parent_hash,
            "ParentAttributeId": parent_attribute_id,
            "varcharValue": varchar,
            "TextValue": text,
            "IntValue": int_value,
            "IntValue2": None,
            "NumberValue": number,
            "BooleanValue": boolean,
            "MainAttributeId": None,
            "RowI": row_i,
        }
    )


def option_id_for_value(field: Any, value: Any) -> int | None:
    key = lookup_key(value)
    for option in getattr(field, "options", []) or []:
        if lookup_key(option.label) == key or lookup_key(option.value) == key or str(option.id or "") == str(value):
            return option.id
    return None


def parse_number(value: Any) -> float | None:
    match = re.search(r"-?\d+(?:[,.]\d+)?", str(value or ""))
    return float(match.group(0).replace(",", ".")) if match else None


def parse_bool(value: Any) -> bool:
    return lookup_key(value) in {"1", "true", "yes", "tak", "y", "t"}


def stable_hash(*parts: Any) -> str:
    return hashlib.md5("|".join(str(part) for part in parts).encode("utf-8")).hexdigest()


def stable_job_id(*parts: Any) -> str:
    digest = hashlib.sha1()
    for part in parts:
        digest.update(part if isinstance(part, bytes) else str(part).encode("utf-8"))
        digest.update(b"|")
    return digest.hexdigest()[:12]
