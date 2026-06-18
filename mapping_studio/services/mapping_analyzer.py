from __future__ import annotations

from typing import Any

from mapping_studio.models import PimField, PimModelBundle
from mapping_studio.services.normalization import normalize
from mapping_studio.services.source_reader import SourceTable


def analyze_source_tables(tables: list[SourceTable], model: PimModelBundle) -> dict[str, Any]:
    return {
        "model": bundle_payload(model),
        "tables": [
            {
                "name": table.name,
                "rows": len(table.rows),
                "columns": columns_for_rows(table.rows),
                "sample_rows": table.rows[:20],
                "suggested_mapping": suggest_mapping(table.rows, model.fields),
            }
            for table in tables
        ],
    }


def bundle_payload(model: PimModelBundle) -> dict[str, Any]:
    return {
        "domain": model.domain,
        "root_model_id": model.root_model_id,
        "root_model_name": model.root_model_name,
        "fields": [
            {
                "key": field.key,
                "label": field.label,
                "attribute_id": field.attribute_id,
                "model_id": field.model_id,
                "kind": field.kind,
                "required": field.required,
                "group": field.group,
                "unit": field.unit,
                "options": [option.__dict__ for option in field.options],
            }
            for field in model.fields
        ],
        "relations": [relation.__dict__ for relation in model.relations],
    }


def columns_for_rows(rows: list[dict[str, Any]]) -> list[str]:
    seen: list[str] = []
    for row in rows[:25]:
        for key in row:
            if key not in seen:
                seen.append(key)
    return seen


def suggest_mapping(rows: list[dict[str, Any]], fields: tuple[PimField, ...]) -> dict[str, Any]:
    columns = columns_for_rows(rows)
    mapping: dict[str, str] = {}
    confidence: dict[str, float] = {}
    for column in columns:
        field, score = best_field_match(column, fields)
        if field and score >= 0.55:
            mapping[column] = field.key
            confidence[column] = round(score, 3)
    return {
        "mapping": mapping,
        "confidence": confidence,
        "target_fields": [
            {
                "key": field.key,
                "label": field.label,
                "kind": field.kind,
                "group": field.group,
                "options": [option.__dict__ for option in field.options],
            }
            for field in fields
        ],
    }


def best_field_match(column: str, fields: tuple[PimField, ...]) -> tuple[PimField | None, float]:
    normalized = normalize(column)
    best: tuple[PimField | None, float] = (None, 0.0)
    for field in fields:
        candidates = {field.key, field.label, *field.aliases}
        for candidate in candidates:
            score = similarity(normalized, normalize(candidate))
            if score > best[1]:
                best = (field, score)
    return best


def similarity(left: str, right: str) -> float:
    if not left or not right:
        return 0.0
    if left == right:
        return 1.0
    if left in right or right in left:
        return min(len(left), len(right)) / max(len(left), len(right))
    left_tokens = set(left.split())
    right_tokens = set(right.split())
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)

