from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class MappingTargetKind(StrEnum):
    IGNORE = "ignore"
    CANONICAL_FIELD = "canonical_field"
    TYPE_SERIES_FIELD = "type_series_field"


class ValueTransformKind(StrEnum):
    TRIM = "trim"
    REPLACE_TEXT = "replace_text"
    REMOVE_TEXT = "remove_text"
    REMOVE_REGEX = "remove_regex"
    DECIMAL_COMMA_TO_DOT = "decimal_comma_to_dot"
    PARSE_NUMBER = "parse_number"
    UNIT_CONVERSION = "unit_conversion"


class TypicalDataAction(StrEnum):
    FILL_IF_MISSING = "fill_if_missing"
    REPLACE_EXISTING = "replace_existing"
    ADD_TYPE_SERIES_PROPERTY = "add_type_series_property"


class ValueTransform(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: ValueTransformKind
    search: str | None = None
    replace_with: str | None = None
    from_unit: str | None = None
    to_unit: str | None = None
    factor: float | None = None


class ColumnMappingRule(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_column: str
    target_kind: MappingTargetKind
    target_path: str | None = None
    unit: str | None = None
    unit_source_column: str | None = None
    transforms: list[ValueTransform] = Field(default_factory=list)
    required: bool = False
    notes: str | None = None


class MappingProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    source_type: str
    product_rules: list[ColumnMappingRule] = Field(default_factory=list)
    type_series_row_key_columns: list[str] = Field(default_factory=list)


class TypicalDataRule(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rule_id: str
    action: TypicalDataAction
    target_path: str
    typical_source_path: str
    condition_path: str | None = None
    condition_value: Any = None
    requires_review: bool = True
    reason: str


class TypicalDataProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    source_file_name: str | None = None
    rules: list[TypicalDataRule] = Field(default_factory=list)


def apply_text_transforms(value: Any, transforms: list[ValueTransform]) -> Any:
    result = value
    for transform in transforms:
        if result is None:
            return None
        if transform.kind == ValueTransformKind.TRIM:
            result = str(result).strip()
        elif transform.kind == ValueTransformKind.REPLACE_TEXT:
            result = str(result).replace(transform.search or "", transform.replace_with or "")
        elif transform.kind == ValueTransformKind.REMOVE_TEXT:
            result = str(result).replace(transform.search or "", "")
        elif transform.kind == ValueTransformKind.DECIMAL_COMMA_TO_DOT:
            result = str(result).replace(",", ".")
        elif transform.kind == ValueTransformKind.PARSE_NUMBER:
            result = _parse_number(result)
        elif transform.kind == ValueTransformKind.UNIT_CONVERSION:
            number = _parse_number(result)
            result = number * transform.factor if number is not None and transform.factor is not None else result
    return result


def _parse_number(value: Any) -> float | None:
    text = str(value).strip().replace(",", ".")
    current = ""
    for char in text:
        if char.isdigit() or char in ".-":
            current += char
        elif current:
            break
    if not current:
        return None
    try:
        return float(current)
    except ValueError:
        return None
