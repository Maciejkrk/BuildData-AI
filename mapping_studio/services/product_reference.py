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
        for variant in product_variant_references(product):
            for alias in variant["aliases"]:
                add_unique_variant(index.by_variant, lookup_key(alias), variant, index.duplicates, "variant")
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


def product_variant_references(product: dict[str, Any]) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for attr in product_attributes(product):
        parent_id = attr.get("ParentAttributeId") or attr.get("parentAttributeId")
        variant_hash = str(attr.get("hash") or "").strip()
        if parent_id in (None, "", 0) or not variant_hash:
            continue
        entry = grouped.setdefault(
            variant_hash,
            {
                "product": product,
                "hash": variant_hash,
                "row_i": attr.get("RowI") if attr.get("RowI") is not None else attr.get("rowI"),
                "aliases": [],
            },
        )
        value = attr.get("varcharValue") or attr.get("TextValue") or attr.get("NumberValue") or attr.get("IntValue")
        if value not in (None, ""):
            append_once(entry["aliases"], str(value))
        attr_id = attr.get("AttributeId") or attr.get("attributeId")
        if attr_id in TYPE_SERIES_NAME_ATTRIBUTE_IDS | TYPE_SERIES_CODE_ATTRIBUTE_IDS and value not in (None, ""):
            append_once(entry["aliases"], str(value))
    return [entry for entry in grouped.values() if entry["aliases"]]


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
        if str(target[key].get("Id") or "") == str(product.get("Id") or ""):
            return
        duplicates.setdefault(duplicate_key, [str(target[key].get("Id") or "")])
        duplicates[duplicate_key].append(str(product.get("Id") or ""))
        return
    target[key] = product


def add_unique_variant(
    target: dict[str, dict[str, Any]],
    key: str,
    variant: dict[str, Any],
    duplicates: dict[str, list[str]],
    namespace: str,
) -> None:
    if not key:
        return
    product = variant.get("product") or {}
    variant_id = f"{product.get('Id') or ''}:{variant.get('hash') or ''}"
    duplicate_key = f"{namespace}:{key}"
    if key in target:
        existing = target[key]
        existing_product = existing.get("product") or {}
        existing_id = f"{existing_product.get('Id') or ''}:{existing.get('hash') or ''}"
        if existing_id == variant_id:
            return
        duplicates.setdefault(duplicate_key, [existing_id])
        duplicates[duplicate_key].append(variant_id)
        return
    target[key] = variant

