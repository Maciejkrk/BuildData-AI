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
) -> dict[str, Any]:
    systems: dict[str, dict[str, Any]] = {}
    unresolved_products: list[dict[str, Any]] = []
    system_order: list[str] = []
    system_indexes: dict[str, int] = {}
    stopped_after_window = False
    preview_offset = max(preview_offset, 0)
    preview_limit = max(preview_limit, 1) if preview_limit is not None else None
    for source_index, row in enumerate(rows, start=1):
        mapped = apply_simple_mapping(row, mapping)
        system_name = mapped.get("building_element.name.value") or mapped.get("system.name") or row.get("Nazwa systemu") or row.get("System") or "System bez nazwy"
        variant_name = mapped.get("building_element.variant_name.value") or row.get("Wariant") or "Wariant domyślny"
        layer_name = mapped.get("building_element.layer_name.value") or row.get("Nazwa warstwy") or row.get("Warstwa") or "Warstwa bez nazwy"
        product_key = first_product_value(mapped) or first_product_value(row)
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
        layer = variant["layers"].setdefault(str(layer_name), {"name": layer_name, "source_rows": [], "products": []})
        layer["source_rows"].append(source_index)

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


def first_product_value(row: dict[str, Any]) -> Any:
    preferred = (
        "building_element.product.value",
        "building_element.produkt.value",
        "Kod produktu",
        "Nazwa produktu",
        "Produkt",
        "Produkty",
    )
    for key in preferred:
        value = row.get(key)
        if value not in (None, ""):
            return value
    for key, value in row.items():
        if str(key).startswith("_") or value in (None, ""):
            continue
        normalized_key = lookup_key(key)
        if "product" in normalized_key or "produkt" in normalized_key:
            return value
    return None


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
    )


def is_legacy_mapping(mapping_profile: dict[str, Any]) -> bool:
    return all(isinstance(value, str) for value in mapping_profile.values())


def mapped_rows_from_profile(tables: list[SourceTable], mapping_profile: dict[str, Any]) -> list[dict[str, Any]]:
    return list(iter_mapped_rows_from_profile(tables, mapping_profile))


def iter_mapped_rows_from_profile(tables: list[SourceTable], mapping_profile: dict[str, Any]) -> Iterator[dict[str, Any]]:
    tables_by_name = {table.name: table for table in tables}
    fallback_table = tables[0] if tables else SourceTable("data", [])
    row_count = max((len(table.rows) for table in tables), default=0)
    levels = mapping_profile.get("_levels") if isinstance(mapping_profile.get("_levels"), dict) else {}
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
