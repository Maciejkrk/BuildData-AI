from __future__ import annotations

from typing import Any

from mapping_studio.models import ProductReferenceIndex
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

        if product_key not in (None, ""):
            match = resolve_product(product_key, product_index)
            product_entry = {"raw": product_key, "resolved": bool(match), "product_id": match.get("Id") if match else None}
            layer["products"].append(product_entry)
            if not match:
                unresolved_products.append({"row": source_index, "value": product_key, "layer": layer_name})

    return {
        "systems": normalize_tree(systems),
        "quality": {
            "systems": len(systems),
            "unresolved_products": unresolved_products,
            "unresolved_products_count": len(unresolved_products),
            "product_reference_loaded": product_index is not None and product_index.products_count > 0,
        },
    }


def apply_simple_mapping(row: dict[str, Any], mapping: dict[str, str]) -> dict[str, Any]:
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


def normalize_tree(systems: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for system in systems.values():
        variants = []
        for variant in system["variants"].values():
            layers = list(variant["layers"].values())
            variants.append({"name": variant["name"], "layers": layers})
        result.append({"name": system["name"], "variants": variants})
    return result

