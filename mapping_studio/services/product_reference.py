from __future__ import annotations

import json
from typing import Any

from mapping_studio.models import ProductReferenceIndex
from mapping_studio.services.normalization import lookup_key


def build_product_reference_index(content: bytes) -> ProductReferenceIndex:
    payload = json.loads(content.decode("utf-8-sig"))
    products = products_from_payload(payload)
    index = ProductReferenceIndex(products_count=len(products))
    for product in products:
        product_id = product.get("Id") or product.get("id")
        name, code = product_identity(product)
        add_unique(index.by_id, str(product_id), product, index.duplicates, "id") if product_id not in (None, "") else None
        add_unique(index.by_name, lookup_key(name), product, index.duplicates, "name") if name else None
        add_unique(index.by_code, lookup_key(code), product, index.duplicates, "code") if code else None
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
    name = ""
    code = ""
    for attr in product_attributes(product):
        attr_id = attr.get("AttributeId")
        value = attr.get("varcharValue") or attr.get("TextValue") or attr.get("IntValue")
        if value in (None, ""):
            continue
        if attr_id == 225 and not name:
            name = str(value)
        if attr_id == 226 and not code:
            code = str(value)
    return name, code


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
        duplicates.setdefault(duplicate_key, [str(target[key].get("Id") or "")])
        duplicates[duplicate_key].append(str(product.get("Id") or ""))
        return
    target[key] = product

