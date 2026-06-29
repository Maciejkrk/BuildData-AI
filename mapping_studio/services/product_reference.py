from __future__ import annotations

import json
from typing import Any

from mapping_studio.models import ProductReferenceIndex
from mapping_studio.services.normalization import lookup_key


PRODUCT_NAME_ATTRIBUTE_IDS = {116, 225}
PRODUCT_CODE_ATTRIBUTE_IDS = {226, 318}
TYPE_SERIES_NAME_ATTRIBUTE_IDS = {319}
TYPE_SERIES_CODE_ATTRIBUTE_IDS = {155, 321}


def build_product_reference_index(content: bytes) -> ProductReferenceIndex:
    payload = json.loads(content.decode("utf-8-sig"))
    products = products_from_payload(payload)
    index = ProductReferenceIndex(products_count=len(products))
    for product in products:
        product_id = product.get("Id") or product.get("id")
        names, codes = product_aliases(product)
        add_unique(index.by_id, str(product_id), product, index.duplicates, "id") if product_id not in (None, "") else None
        for name in names:
            add_unique(index.by_name, lookup_key(name), product, index.duplicates, "name")
        for code in codes:
            add_unique(index.by_code, lookup_key(code), product, index.duplicates, "code")
    return index


def products_from_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        for key in ("products", "Products"):
            if isinstance(payload.get(key), list):
                return [item for item in payload[key] if isinstance(item, dict)]
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    return []


def product_identity(product: dict[str, Any]) -> tuple[str, str]:
    names, codes = product_aliases(product)
    return (names[0] if names else "", codes[0] if codes else "")


def product_aliases(product: dict[str, Any]) -> tuple[list[str], list[str]]:
    names: list[str] = []
    codes: list[str] = []
    for attr in product_attributes(product):
        attr_id = attr.get("AttributeId") or attr.get("attributeId")
        parent_id = attr.get("ParentAttributeId") or attr.get("parentAttributeId")
        value = attr.get("varcharValue") or attr.get("TextValue") or attr.get("IntValue")
        if value in (None, ""):
            continue
        if attr_id in PRODUCT_NAME_ATTRIBUTE_IDS:
            append_once(names, str(value))
        elif attr_id in PRODUCT_CODE_ATTRIBUTE_IDS:
            append_once(codes, str(value))
        elif parent_id not in (None, "", 0):
            if attr_id in TYPE_SERIES_NAME_ATTRIBUTE_IDS:
                append_once(names, str(value))
            elif attr_id in TYPE_SERIES_CODE_ATTRIBUTE_IDS:
                append_once(codes, str(value))
    return names, codes


def append_once(values: list[str], value: str) -> None:
    if value and value not in values:
        values.append(value)


def product_attributes(product: dict[str, Any]) -> list[dict[str, Any]]:
    versions = product.get("dataVersions") or product.get("DataVersions") or []
    attrs: list[dict[str, Any]] = []
    if isinstance(product.get("productAttributes"), list):
        attrs.extend(product["productAttributes"])
    for version in versions:
        if isinstance(version, dict):
            attrs.extend(version.get("productAttributes") or version.get("ProductAttributes") or [])
    return [attr for attr in attrs if isinstance(attr, dict)]


def add_unique(
    target: dict[str, dict[str, Any]],
    key: str,
    product: dict[str, Any],
    duplicates: dict[str, list[str]],
    namespace: str,
) -> None:
    if not key:
        return
    duplicate_key = f"{namespace}:{key}"
    if key in target:
        if product_id_text(target[key]) == product_id_text(product):
            return
        duplicates.setdefault(duplicate_key, [product_id_text(target[key])])
        duplicates[duplicate_key].append(product_id_text(product))
        return
    target[key] = product


def product_id_text(product: dict[str, Any]) -> str:
    return str(product.get("Id") or product.get("id") or "")

