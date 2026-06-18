from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class FieldKind(StrEnum):
    FREE_TEXT = "free_text"
    NUMBER = "number"
    SINGLE_CHOICE = "single_choice"
    MULTI_CHOICE = "multi_choice"
    BOOLEAN = "boolean"
    FILES = "files"
    PRODUCT_REF = "product_ref"
    NESTED_MODEL = "nested_model"


@dataclass(frozen=True)
class PimOption:
    id: int | None
    label: str
    value: str


@dataclass(frozen=True)
class PimField:
    key: str
    label: str
    attribute_id: int
    model_id: int
    kind: FieldKind
    required: bool = False
    parent_attribute_id: int = 0
    target_model_id: int | None = None
    unit: str | None = None
    group: str = "General"
    aliases: tuple[str, ...] = ()
    options: tuple[PimOption, ...] = ()


@dataclass(frozen=True)
class NestedRelation:
    key: str
    label: str
    attribute_id: int
    source_model_id: int
    target_model_id: int
    parent_relation_key: str | None = None


@dataclass(frozen=True)
class PimModelBundle:
    domain: str
    root_model_id: int
    root_model_name: str
    fields: tuple[PimField, ...]
    relations: tuple[NestedRelation, ...] = ()


@dataclass
class ProductReferenceIndex:
    products_count: int = 0
    by_id: dict[str, dict[str, Any]] = field(default_factory=dict)
    by_code: dict[str, dict[str, Any]] = field(default_factory=dict)
    by_name: dict[str, dict[str, Any]] = field(default_factory=dict)
    duplicates: dict[str, list[str]] = field(default_factory=dict)

