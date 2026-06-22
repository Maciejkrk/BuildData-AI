from __future__ import annotations

import json
from typing import Any

from mapping_studio.models import FieldKind, NestedRelation, PimField, PimModelBundle, PimModelChoice, PimOption
from mapping_studio.services.normalization import first_present, int_value, normalize, text_value


def load_product_model(files: dict[str, bytes], root_model_id: int | None = None) -> PimModelBundle:
    models_payload, attributes_payload = _load_model_pair(
        files,
        ("productsmodels", "productmodels"),
        ("productsattributes", "productattributes"),
    )
    return _load_bundle(models_payload, attributes_payload, domain="products", root_type="product", root_model_id=root_model_id)


def load_building_element_model(files: dict[str, bytes], root_model_id: int | None = None) -> PimModelBundle:
    models_payload, attributes_payload = _load_model_pair(
        files,
        (
            "buildingselementsmodels",
            "buildingelementsmodels",
            "buildingelementmodels",
            "systemsmodels",
            "systemmodels",
        ),
        (
            "buildingselementsattributes",
            "buildingelementsattributes",
            "buildingelementattributes",
            "systemsattributes",
            "systemattributes",
        ),
    )
    return _load_bundle(models_payload, attributes_payload, domain="building_elements", root_type="building_element", root_model_id=root_model_id)


def _load_model_pair(
    files: dict[str, bytes],
    models_keys: str | tuple[str, ...],
    attributes_keys: str | tuple[str, ...],
) -> tuple[Any, Any]:
    keyed = {_file_key(name): content for name, content in files.items()}
    models = _first_matching_file(keyed, models_keys)
    attributes = _first_matching_file(keyed, attributes_keys)
    if models is None or attributes is None:
        raise ValueError("Both model and attribute JSON files are required.")
    return json.loads(models.decode("utf-8-sig")), json.loads(attributes.decode("utf-8-sig"))


def _first_matching_file(keyed: dict[str, bytes], expected_keys: str | tuple[str, ...]) -> bytes | None:
    keys = (expected_keys,) if isinstance(expected_keys, str) else expected_keys
    for key in keys:
        if key in keyed:
            return keyed[key]
    return None


def _file_key(filename: str) -> str:
    return "".join(char for char in filename.lower().removesuffix(".json") if char.isalnum())


def _load_bundle(models_payload: Any, attributes_payload: Any, *, domain: str, root_type: str, root_model_id: int | None = None) -> PimModelBundle:
    root_model_id = int_value(root_model_id)
    models = _items(models_payload, "models")
    attributes = [item for item in _items(attributes_payload, "attributes") if not _is_deleted(item)]
    if not models or not attributes:
        raise ValueError("The uploaded files do not contain a readable PIM model export.")

    root_models = _root_model_choices(models, root_type)
    root_model = next((model for model in models if int_value(model.get("Id")) == root_model_id), None) if root_model_id is not None else None
    root_model = root_model or _root_model(models, root_type)
    root_model_id = int_value(root_model.get("Id"))
    if root_model_id is None:
        raise ValueError("Root PIM model has no Id.")

    model_name_by_id = {
        model_id: text_value(first_present(model, "Name", "DispName", "AttributeName") or model_id)
        for model in models
        if (model_id := int_value(model.get("Id"))) is not None
    }
    attributes_by_model: dict[int, list[dict[str, Any]]] = {}
    for attribute in attributes:
        model_id = int_value(attribute.get("ProductModelId"))
        if model_id is not None:
            attributes_by_model.setdefault(model_id, []).append(attribute)
    for grouped in attributes_by_model.values():
        grouped.sort(key=lambda item: (int_value(item.get("DisplayOrder")) or 999999, int_value(item.get("Id")) or 0))

    relations: list[NestedRelation] = []
    fields: list[PimField] = []

    def visit_model(model_id: int, group: str, parent_relation_key: str | None = None) -> None:
        for attribute in attributes_by_model.get(model_id, []):
            attr_id = int_value(attribute.get("Id"))
            if attr_id is None:
                continue
            target_model_id = int_value(attribute.get("TargetModelId"))
            kind = field_kind(attribute)
            label = text_value(first_present(attribute, "DispName", "AttributeName", "Name") or attr_id)
            if target_model_id and kind == FieldKind.NESTED_MODEL:
                relation_key = f"model.{model_id}.attribute.{attr_id}"
                relations.append(
                    NestedRelation(
                        key=relation_key,
                        label=label,
                        attribute_id=attr_id,
                        source_model_id=model_id,
                        target_model_id=target_model_id,
                        parent_relation_key=parent_relation_key,
                    )
                )
                visit_model(target_model_id, label, relation_key)
                continue
            fields.append(
                PimField(
                    key=semantic_key(domain, attribute, group=group),
                    label=label,
                    attribute_id=attr_id,
                    model_id=model_id,
                    kind=kind,
                    required=bool(attribute.get("IsRequired")),
                    parent_attribute_id=0,
                    target_model_id=target_model_id,
                    unit=text_value(attribute.get("Unit")) or None,
                    group=group,
                    parent_relation_key=parent_relation_key,
                    aliases=aliases(attribute, label),
                    options=options(attribute),
                )
            )

    visit_model(root_model_id, model_name_by_id.get(root_model_id, root_type))
    return PimModelBundle(
        domain=domain,
        root_model_id=root_model_id,
        root_model_name=model_name_by_id.get(root_model_id, root_type),
        fields=tuple(fields),
        relations=tuple(relations),
        root_models=tuple(root_models),
    )


def _items(payload: Any, key: str) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get(key), list):
        return [item for item in payload[key] if isinstance(item, dict)]
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    return []


def _root_model(models: list[dict[str, Any]], root_type: str) -> dict[str, Any]:
    normalized_root_type = normalize(root_type)
    for model in models:
        if normalize(first_present(model, "modelType", "ModelType", "type")) == normalized_root_type:
            return model
    if models:
        return models[0]
    raise ValueError("No PIM models found.")


def _root_model_choices(models: list[dict[str, Any]], root_type: str) -> list[PimModelChoice]:
    result = []
    normalized_root_type = normalize(root_type)
    for model in models:
        model_id = int_value(model.get("Id"))
        if model_id is None:
            continue
        model_type = text_value(first_present(model, "modelType", "ModelType", "type") or "")
        if normalize(model_type) != normalized_root_type:
            continue
        result.append(
            PimModelChoice(
                id=model_id,
                name=text_value(first_present(model, "Name", "DispName", "AttributeName") or model_id),
                model_type=model_type,
            )
        )
    return sorted(result, key=lambda item: (item.name, item.id))


def _is_deleted(attribute: dict[str, Any]) -> bool:
    return str(attribute.get("deleted") or attribute.get("Deleted") or "").lower() in {"true", "1", "yes"}


def field_kind(attribute: dict[str, Any]) -> FieldKind:
    attr_type = str(attribute.get("AttributeType") or "")
    if attr_type in {"Model_Array", "Table_Model"}:
        return FieldKind.NESTED_MODEL
    if attr_type in {"Select", "Dropdown", "Radio", "List"}:
        return FieldKind.SINGLE_CHOICE
    if attr_type in {"Checkboxes", "MultiSelect", "Multi_Select"}:
        return FieldKind.MULTI_CHOICE
    if attr_type in {"Number", "Int", "Integer", "Decimal", "Float"}:
        return FieldKind.NUMBER
    if attr_type == "Boolean":
        return FieldKind.BOOLEAN
    if attr_type == "Files":
        return FieldKind.FILES
    if attr_type == "Product":
        return FieldKind.PRODUCT_REF
    return FieldKind.FREE_TEXT


def options(attribute: dict[str, Any]) -> tuple[PimOption, ...]:
    raw_options = attribute.get("AttributeOptions") or []
    result: list[PimOption] = []
    for item in raw_options:
        if not isinstance(item, dict):
            continue
        label = text_value(first_present(item, "OptionName", "label", "name", "Name"))
        if not label:
            continue
        result.append(PimOption(id=int_value(first_present(item, "Id", "id", "OptionId")), label=label, value=text_value(first_present(item, "OptionValue", "value", "Value"))))
    return tuple(result)


def aliases(attribute: dict[str, Any], label: str) -> tuple[str, ...]:
    values = {normalize(label)}
    for key in ("AttributeName", "DispName", "Name", "Code"):
        value = normalize(attribute.get(key))
        if value:
            values.add(value)
    return tuple(sorted(values))


def semantic_key(domain: str, attribute: dict[str, Any], *, group: str) -> str:
    attr_id = int_value(attribute.get("Id")) or 0
    label = normalize(first_present(attribute, "AttributeName", "DispName", "Name"))
    if domain == "products":
        if label in {"name", "nazwa", "nazwa produktu"}:
            return "product.name.value"
        if label in {"code", "kod", "external id", "external_id"}:
            return "product.code.value"
    if domain == "building_elements":
        name = normalize(attribute.get("AttributeName"))
        if name:
            return f"building_element.{name}.value"
    group_key = normalize(group).replace(" ", "_") or "pim"
    return f"{domain}.{group_key}.attribute.{attr_id}.value"

