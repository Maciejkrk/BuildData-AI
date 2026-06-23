from __future__ import annotations

import re
from typing import Any

from data_master_app.mapping import apply_cleanup
from mapping_studio.models import ProductReferenceIndex
from mapping_studio.services.source_reader import SourceTable
from mapping_studio.services.normalization import lookup_key


def preview_building_elements(rows: list[dict[str, Any]], mapping: dict[str, str], product_index: ProductReferenceIndex | None) -> dict[str, Any]:
    systems: dict[str, dict[str, Any]] = {}
    unresolved_products: list[dict[str, Any]] = []
    for source_index, row in enumerate(rows, start=1):
        mapped = apply_simple_mapping(row, mapping)
        system_name = mapped.get("building_element.name.value") or mapped.get("system.name") or row.get("Nazwa systemu") or row.get("System") or "System bez nazwy"
        variant_name = mapped.get("building_element.variant_name.value") or row.get("Wariant") or "Wariant domyślny"
        layer_name = mapped.get("building_element.layer_name.value") or row.get("Nazwa warstwy") or row.get("Warstwa") or "Warstwa bez nazwy"
        product_key = mapped.get("building_element.product.value") or row.get("Kod produktu") or row.get("Nazwa produktu") or row.get("Produkt")

        system = systems.setdefault(str(system_name), {"name": system_name, "variants": {}})
        variant = system["variants"].setdefault(str(variant_name), {"name": variant_name, "layers": {}})
        layer = variant["layers"].setdefault(str(layer_name), {"name": layer_name, "source_rows": [], "products": []})
        layer["source_rows"].append(source_index)

        for product_value in product_values(product_key):
            match = resolve_product(product_value, product_index)
            product_entry = {
                "raw": product_value,
                "resolved": bool(match),
                "product_id": match.get("Id") if match else None,
                "identity_source": product_identity_source(product_value, product_index, match),
            }
            layer["products"].append(product_entry)
            if not match:
                unresolved_products.append({"row": source_index, "value": product_value, "layer": layer_name})

    return {
        "systems": normalize_tree(systems),
        "quality": {
            "systems": len(systems),
            "unresolved_products": unresolved_products,
            "unresolved_products_count": len(unresolved_products),
            "product_reference_loaded": product_index is not None and product_index.products_count > 0,
        },
    }


def preview_building_elements_from_tables(
    tables: list[SourceTable],
    mapping_profile: dict[str, Any],
    product_index: ProductReferenceIndex | None,
) -> dict[str, Any]:
    if not mapping_profile:
        return preview_building_elements(tables[0].rows if tables else [], {}, product_index)
    if is_legacy_mapping(mapping_profile):
        return preview_building_elements(tables[0].rows if tables else [], mapping_profile, product_index)

    rows = mapped_rows_from_profile(tables, mapping_profile)
    return preview_building_elements(rows, {}, product_index)


def is_legacy_mapping(mapping_profile: dict[str, Any]) -> bool:
    return all(isinstance(value, str) for value in mapping_profile.values())


def mapped_rows_from_profile(tables: list[SourceTable], mapping_profile: dict[str, Any]) -> list[dict[str, Any]]:
    tables_by_name = {table.name: table for table in tables}
    fallback_table = tables[0] if tables else SourceTable("data", [])
    row_count = max((len(table.rows) for table in tables), default=0)
    result: list[dict[str, Any]] = []
    for index in range(row_count):
        mapped: dict[str, Any] = {}
        source_context: dict[str, Any] = {}
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
            result.append(mapped)
    return result


def apply_simple_mapping(row: dict[str, Any], mapping: dict[str, str]) -> dict[str, Any]:
    if not mapping:
        return dict(row)
    mapped: dict[str, Any] = {}
    for source, target in mapping.items():
        if target and target != "ignore":
            mapped[target] = row.get(source)
    return mapped


def resolve_product(value: Any, product_index: ProductReferenceIndex | None) -> dict[str, Any] | None:
    if product_index is None:
        return None
    key = lookup_key(value)
    return product_index.by_id.get(str(value)) or product_index.by_code.get(key) or product_index.by_name.get(key)


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
