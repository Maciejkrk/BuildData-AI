from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DataSource(StrEnum):
    CLIENT = "client"
    PIM_REFERENCE = "pim_reference"
    NORMATIVE_MODEL = "normative_model"
    MANUAL = "manual"
    IMPORT_RULE = "import_rule"


class Confidence(StrEnum):
    CONFIRMED = "confirmed"
    INFERRED = "inferred"
    ESTIMATED = "estimated"
    MISSING = "missing"


class FieldValue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    value: Any = None
    unit: str | None = None
    source: DataSource = DataSource.CLIENT
    confidence: Confidence = Confidence.CONFIRMED
    requires_review: bool = False
    reason: str | None = None
    rule_id: str | None = None
    updated_at: datetime | None = None


class TechnicalProperty(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: FieldValue
    value: FieldValue
    prefix: FieldValue | None = None
    unit: FieldValue | None = None
    group: FieldValue | None = None


class Measurement(BaseModel):
    model_config = ConfigDict(extra="forbid")

    value: FieldValue
    unit: FieldValue | None = None


class Package(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: FieldValue | None = None
    weight: FieldValue | None = None
    capacity: FieldValue | None = None
    unit_name: FieldValue | None = None
    raw_text: FieldValue | None = None


class DocumentLink(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: FieldValue
    url: FieldValue | None = None
    path: FieldValue | None = None
    category: FieldValue | None = None
    extension: FieldValue | None = None


class TypeSeriesRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    variant_code: FieldValue | None = None
    variant_name: FieldValue | None = None
    thickness: Measurement | None = None
    lambda_value: Measurement | None = None
    density: Measurement | None = None
    vapor_permeability_mu: Measurement | None = None
    specific_heat: Measurement | None = None


class Product(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_version: str = "product.v1"
    source_record_id: FieldValue | None = None
    pim_product_id: FieldValue | None = None
    code: FieldValue | None = None
    name: FieldValue
    category: list[FieldValue] = Field(default_factory=list)
    unit: FieldValue | None = None
    manufacturer: FieldValue | None = None
    product_url: FieldValue | None = None
    short_name: FieldValue | None = None
    full_name: FieldValue | None = None
    technical_name: FieldValue | None = None
    description: FieldValue | None = None
    properties: FieldValue | None = None
    application: FieldValue | None = None
    surface_preparation: FieldValue | None = None
    usage_method: FieldValue | None = None
    comments: FieldValue | None = None
    warnings: FieldValue | None = None
    norms: FieldValue | None = None
    storage: FieldValue | None = None
    packages: list[Package] = Field(default_factory=list)
    technical_properties: list[TechnicalProperty] = Field(default_factory=list)
    documents: list[DocumentLink] = Field(default_factory=list)
    type_series: list[TypeSeriesRow] = Field(default_factory=list)
    raw_links: list[FieldValue] = Field(default_factory=list)


def missing_field(reason: str = "Brak danych w zrodle.") -> FieldValue:
    return FieldValue(
        value=None,
        source=DataSource.CLIENT,
        confidence=Confidence.MISSING,
        requires_review=True,
        reason=reason,
    )


def inferred_normative_value(
    value: Any,
    *,
    unit: str | None,
    rule_id: str,
    reason: str,
) -> FieldValue:
    return FieldValue(
        value=value,
        unit=unit,
        source=DataSource.NORMATIVE_MODEL,
        confidence=Confidence.INFERRED,
        requires_review=True,
        rule_id=rule_id,
        reason=reason,
    )


def measurement(
    value: Any,
    *,
    unit: str | None,
    source: DataSource = DataSource.CLIENT,
    confidence: Confidence = Confidence.CONFIRMED,
    requires_review: bool = False,
    reason: str | None = None,
    rule_id: str | None = None,
) -> Measurement:
    return Measurement(
        value=FieldValue(
            value=value,
            source=source,
            confidence=confidence,
            requires_review=requires_review,
            reason=reason,
            rule_id=rule_id,
        ),
        unit=FieldValue(
            value=unit,
            source=source,
            confidence=confidence,
            requires_review=requires_review,
            reason=reason,
            rule_id=rule_id,
        )
        if unit
        else None,
    )


def inferred_normative_measurement(
    value: Any,
    *,
    unit: str | None,
    rule_id: str,
    reason: str,
) -> Measurement:
    return measurement(
        value,
        unit=unit,
        source=DataSource.NORMATIVE_MODEL,
        confidence=Confidence.INFERRED,
        requires_review=True,
        rule_id=rule_id,
        reason=reason,
    )
