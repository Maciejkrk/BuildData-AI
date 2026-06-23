from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FieldDefinition:
    key: str
    label: str
    required: bool
    aliases: set[str]
    group: str = "General"
    value_kind: str = "free_text"
    options: tuple[dict[str, Any], ...] = ()
    unit: str | None = None


PRODUCT_FIELDS = [
    FieldDefinition("product.name.value", "Product / name / value", True, {"product_name", "name", "nazwa", "nazwa produktu", "produkt", "product", "model"}, "Product identity"),
    FieldDefinition("product.code.value", "Product / code / value", False, {"id", "sku", "kod", "kod produktu", "indeks", "external_id", "product id"}, "Product identity"),
    FieldDefinition("product.unit.value", "Product / unit / value", False, {"unit", "jednostka", "jm", "jednostka miary"}, "Product identity"),
    FieldDefinition("product.category[].value", "Product / category[] / value", False, {"category", "categories", "kategoria", "kategorie", "grupa", "parent_group", "parent path", "parent_path", "group id", "category id"}, "Classification"),
    FieldDefinition("product.description.value", "Product / description / value", False, {"description", "opis", "opis produktu"}, "Descriptions"),
    FieldDefinition("product.properties.value", "Product / properties / value", False, {"properties", "wlasciwosci", "cechy"}, "Descriptions"),
    FieldDefinition("product.application.value", "Product / application / value", False, {"zastosowanie", "application", "use", "przeznaczenie"}, "Descriptions"),
    FieldDefinition("product.usage_method.value", "Product / usage method / value", False, {"sposob uzycia", "usage_method", "aplikacja"}, "Descriptions"),
    FieldDefinition("product.norms.value", "Product / norms / value", False, {"normy", "norms", "certyfikaty", "aprobaty"}, "Documents and references"),
    FieldDefinition("product.manufacturer.value", "Product / manufacturer / value", False, {"manufacturer", "producent"}, "Product identity"),
    FieldDefinition("product.product_url.value", "Product / URL / value", False, {"url", "link", "www", "strona"}, "Documents and references"),
    FieldDefinition("product.documents[].url.value", "Product / documents[] / URL", False, {"files", "file", "file links", "document urls", "document_urls", "image urls", "image_urls", "packshot", "packshot_url", "zdjecie", "zdjęcie", "obraz", "asset"}, "Documents and references"),
    FieldDefinition("product.documents[].name.value", "Product / documents[] / name", False, {"file name", "document name", "caption", "podpis", "nazwa pliku"}, "Documents and references"),
    FieldDefinition("product.documents[].category.value", "Product / documents[] / category", False, {"file type", "document type", "typ pliku", "kategoria dokumentu"}, "Documents and references"),
    FieldDefinition("product.packages[].raw_text.value", "Product / packages[] / raw text", False, {"opakowanie", "package", "packaging"}, "Packages"),
    FieldDefinition("product.packages[].weight.value", "Product / packages[] / weight / value", False, {"waga", "weight", "masa"}, "Packages"),
    FieldDefinition("product.packages[].capacity.value", "Product / packages[] / capacity / value", False, {"pojemnosc", "capacity"}, "Packages"),
    FieldDefinition("type_series[].variant_code.value", "Type series / variant code / value", False, {"wariant kod", "variant code", "kod wariantu"}, "Type series"),
    FieldDefinition("type_series[].variant_name.value", "Type series / variant name / value", False, {"wariant", "variant", "nazwa wariantu"}, "Type series"),
    FieldDefinition("type_series[].thickness.value", "Type series / thickness / value", False, {"grubosc", "thickness", "sot_thickness"}, "Type series"),
    FieldDefinition("type_series[].thickness.unit", "Type series / thickness / unit", False, {"jednostka grubosci", "thickness unit", "unit thickness"}, "Type series"),
    FieldDefinition("type_series[].lambda_value.value", "Type series / lambda / value", False, {"lambda", "wspolczynnik lambda"}, "Type series"),
    FieldDefinition("type_series[].lambda_value.unit", "Type series / lambda / unit", False, {"jednostka lambda", "lambda unit"}, "Type series"),
    FieldDefinition("type_series[].density.value", "Type series / density / value", False, {"gestosc", "density"}, "Type series"),
    FieldDefinition("type_series[].density.unit", "Type series / density / unit", False, {"jednostka gestosci", "density unit"}, "Type series"),
    FieldDefinition("type_series[].vapor_permeability_mu.value", "Type series / mu / value", False, {"mu", "vapor permeability", "paroprzepuszczalnosc"}, "Type series"),
    FieldDefinition("type_series[].vapor_permeability_mu.unit", "Type series / mu / unit", False, {"jednostka mu", "mu unit"}, "Type series"),
    FieldDefinition("type_series[].specific_heat.value", "Type series / specific heat / value", False, {"cieplo wlasciwe", "specific heat", "heat capacity"}, "Type series"),
    FieldDefinition("type_series[].specific_heat.unit", "Type series / specific heat / unit", False, {"jednostka ciepla wlasciwego", "specific heat unit"}, "Type series"),
]


SYSTEM_FIELDS = [
    FieldDefinition("system_name", "Nazwa systemu", True, {"system_name", "system", "nazwa systemu", "nazwa elementu", "building element", "element"}),
    FieldDefinition("building_element_type", "Typ systemu", False, {"building_element_type", "typ systemu", "zastosowanie systemu", "typ elementu"}),
    FieldDefinition("insulation_type", "Rodzaj izolacji", False, {"insulation_type", "rodzaj izolacji", "izolacja"}),
    FieldDefinition("bim_building_element_type", "Typ BIM", False, {"bim_building_element_type", "bim type", "typ bim", "building element type bim"}),
    FieldDefinition("variant_name", "Wariant", True, {"variant_name", "wariant", "nazwa wariantu", "finish", "wykonczenie"}),
    FieldDefinition("layer_position", "Pozycja warstwy", False, {"layer_position", "pozycja warstwy", "kolejnosc", "nr warstwy"}),
    FieldDefinition("layer_name", "Nazwa warstwy", True, {"layer_name", "warstwa", "nazwa warstwy"}),
    FieldDefinition("product_code", "Kod produktu", False, {"product_code", "kod produktu", "sku", "indeks", "id produktu"}),
    FieldDefinition("product_name", "Nazwa produktu", False, {"product_name", "produkt", "nazwa produktu"}),
    FieldDefinition("default", "Produkt domyslny", False, {"default", "domyslny", "produkt domyslny"}),
    FieldDefinition("quantity", "Ilosc", False, {"quantity", "ilosc", "zuzycie"}),
]


def analyze_tables(tables: list[Any], product_fields: list[FieldDefinition] | None = None) -> dict[str, Any]:
    product_fields = product_fields or PRODUCT_FIELDS
    return {
        "tables": [
            {
                "name": table.name,
                "rows": len(table.rows),
                "columns": columns_for_rows(table.rows),
                "sample_rows": table.rows,
                "column_samples": column_samples(table.rows, columns_for_rows(table.rows)),
                "product_mapping": suggest_mapping(table.rows, product_fields),
                "system_mapping": suggest_mapping(table.rows, SYSTEM_FIELDS),
            }
            for table in tables
        ]
    }


def product_fields_from_json(content: bytes | str) -> list[FieldDefinition]:
    text = content.decode("utf-8-sig") if isinstance(content, bytes) else content
    payload = json.loads(text)
    return product_fields_from_payload(payload)


def product_fields_from_pim_bundle(files: dict[str, bytes | str], root_model_id: int | None = None) -> list[FieldDefinition]:
    root_model_id = int_value(root_model_id)
    keyed_files = {pim_bundle_file_key(filename): content for filename, content in files.items()}
    models_content = keyed_files.get("productsmodels")
    attributes_content = keyed_files.get("productsattributes")
    if models_content is not None and attributes_content is not None:
        models_payload = load_json_content(models_content)
        attributes_payload = load_json_content(attributes_content)
        fields = product_fields_from_pim_models(models_payload, attributes_payload, root_model_id=root_model_id)
        if fields:
            return fields
        return []
    for filename, content in files.items():
        if pim_bundle_file_key(filename) == "products":
            continue
        payload = load_json_content(content)
        fields = product_fields_from_payload(payload)
        if fields:
            return fields
    return []


def pim_bundle_file_key(filename: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "", str(filename or "").lower().removesuffix(".json"))
    if "productsmodels" in normalized or "productmodels" in normalized:
        return "productsmodels"
    if "productsattributes" in normalized or "productattributes" in normalized:
        return "productsattributes"
    if normalized in {"products", "product"} or normalized.endswith("products") or normalized.endswith("product"):
        return "products"
    return ""


def load_json_content(content: bytes | str) -> Any:
    text = content.decode("utf-8-sig") if isinstance(content, bytes) else content
    return json.loads(text)


def product_fields_from_pim_models(
    models_payload: Any,
    attributes_payload: Any,
    *,
    root_model_id: int | None = None,
) -> list[FieldDefinition]:
    root_model_id = int_value(root_model_id)
    models = pim_items(models_payload, "models")
    attributes = [attribute for attribute in pim_items(attributes_payload, "attributes") if not is_deleted(attribute)]
    if not models or not attributes:
        return []

    models_by_id = {model_id: model for model in models if (model_id := int_value(model.get("Id"))) is not None}
    model_ids = {
        int(model["Id"])
        for model in models
        if normalize(first_present(model, "modelType", "ModelType", "type")) == "product" and model.get("Id") is not None
    }
    if root_model_id is not None:
        model_ids = {root_model_id}
    if not model_ids:
        model_ids = {66}

    attributes_by_model: dict[int, list[dict[str, Any]]] = {}
    for attribute in attributes:
        model_id = int_value(attribute.get("ProductModelId"))
        if model_id is not None:
            attributes_by_model.setdefault(model_id, []).append(attribute)
    for grouped in attributes_by_model.values():
        grouped.sort(key=attribute_order)

    fields: list[FieldDefinition] = []
    seen: set[str] = set()
    for model_id in sorted(model_ids):
        for attribute in attributes_by_model.get(model_id, []):
            if skip_pim_attribute(attribute):
                continue
            target_model_id = int_value(attribute.get("TargetModelId"))
            if target_model_id and is_nested_attribute(attribute):
                if int_value(attribute.get("Id")) in TECHNICAL_NESTED_ATTRIBUTE_IDS:
                    continue
                target_model = models_by_id.get(target_model_id)
                child_attributes = [
                    child
                    for child in attributes_by_model.get(target_model_id, [])
                    if not skip_pim_attribute(child) and not is_nested_attribute(child)
                ]
                is_type_series = is_type_series_parent(attribute, target_model, child_attributes)
                parent_group = "Type series" if is_type_series else text_value(first_present(attribute, "DispName", "AttributeName", "Name") or "PIM model")
                for child in child_attributes:
                    field = pim_field_definition(
                        child,
                        parent_group,
                        parent_attribute=attribute,
                        parent_model=target_model,
                        parent_is_type_series=is_type_series,
                    )
                    if field and field.key not in seen:
                        fields.append(field)
                        seen.add(field.key)
                continue
            field = pim_field_definition(attribute, "Product identity")
            if field and field.key not in seen:
                fields.append(field)
                seen.add(field.key)

    return fields


def product_model_choices_from_pim_bundle(files: dict[str, bytes | str]) -> list[dict[str, Any]]:
    keyed_files = {pim_bundle_file_key(filename): content for filename, content in files.items()}
    models_content = keyed_files.get("productsmodels")
    if models_content is None:
        return []
    models_payload = load_json_content(models_content)
    choices = []
    for model in pim_items(models_payload, "models"):
        model_id = int_value(model.get("Id"))
        if model_id is None:
            continue
        model_type = text_value(first_present(model, "modelType", "ModelType", "type") or "")
        if normalize(model_type) != "product":
            continue
        choices.append(
            {
                "id": model_id,
                "name": text_value(first_present(model, "Name", "DispName", "AttributeName") or model_id),
                "modelType": model_type,
            }
        )
    return sorted(choices, key=lambda item: (item["name"], item["id"]))


def pim_items(payload: Any, key: str) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get(key), list):
        return [item for item in payload[key] if isinstance(item, dict)]
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    return []


def pim_field_definition(
    attribute: dict[str, Any],
    group: str,
    *,
    parent_attribute: dict[str, Any] | None = None,
    parent_model: dict[str, Any] | None = None,
    parent_is_type_series: bool = False,
) -> FieldDefinition | None:
    attribute_id = int_value(attribute.get("Id"))
    if attribute_id is None:
        return None
    label = text_value(first_present(attribute, "DispName", "AttributeName", "Name") or attribute_id)
    key = PIM_ATTRIBUTE_KEY_OVERRIDES.get(attribute_id)
    key = key or semantic_pim_field_key(
        attribute,
        parent_attribute=parent_attribute,
        parent_model=parent_model,
        parent_is_type_series=parent_is_type_series,
    )
    key = key or f"pim.attribute.{attribute_id}.value"
    aliases = aliases_from_pim_attribute(attribute, label)
    if parent_attribute:
        aliases.update(aliases_from_pim_attribute(parent_attribute, ""))
    if attribute.get("Unit"):
        aliases.add(normalize(attribute.get("Unit")))
    aliases.update(normalize(alias) for alias in PIM_ATTRIBUTE_EXTRA_ALIASES.get(attribute_id, set()))
    value_kind = value_kind_from_attribute(attribute)
    options = options_from_attribute(attribute)
    unit = text_value(attribute.get("Unit") or "")
    return FieldDefinition(key, label, bool(attribute.get("IsRequired") or attribute.get("Required")), aliases, group, value_kind, options, unit or None)


def aliases_from_pim_attribute(attribute: dict[str, Any], label: str) -> set[str]:
    aliases = {normalize(label)}
    for key in ("AttributeName", "DispName", "Name", "Code"):
        value = attribute.get(key)
        if value not in (None, ""):
            aliases.add(normalize(value))
    return {alias for alias in aliases if alias}


def is_nested_attribute(attribute: dict[str, Any]) -> bool:
    return str(attribute.get("AttributeType") or "") in {"Model_Array", "Table_Model"}


def value_kind_from_attribute(attribute: dict[str, Any]) -> str:
    attribute_type = str(attribute.get("AttributeType") or "")
    if attribute_type in {"Checkboxes", "MultiSelect", "Multi_Select"}:
        return "multi_choice"
    if attribute_type in {"Radio", "Select", "Dropdown", "List"}:
        return "single_choice"
    if attribute_type in {"Number", "Int", "Integer", "Decimal", "Float"}:
        return "number"
    if attribute_type == "Files":
        return "files"
    return "free_text"


def options_from_attribute(attribute: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    raw_options = first_present(
        attribute,
        "AttributeOptions",
        "Options",
        "options",
        "Values",
        "values",
        "AllowedValues",
        "allowed_values",
    )
    return normalized_options(raw_options)


def normalized_options(raw_options: Any) -> tuple[dict[str, Any], ...]:
    if isinstance(raw_options, dict):
        raw_options = raw_options.get("options") or raw_options.get("values") or raw_options.get("items") or []
    if not isinstance(raw_options, list):
        return ()
    options: list[dict[str, Any]] = []
    for item in raw_options:
        if isinstance(item, dict):
            label = first_present(item, "OptionName", "label", "name", "Name", "text", "value", "Value")
            value = first_present(item, "OptionValue", "value", "Value", "code", "Code")
            option_id = first_present(item, "Id", "id", "OptionId", "option_id")
        else:
            label = item
            value = item
            option_id = None
        label_text = text_value(label)
        if not label_text:
            continue
        options.append(
            {
                "id": option_id,
                "label": label_text,
                "value": text_value(value),
            }
        )
    return tuple(options)


def semantic_pim_field_key(
    attribute: dict[str, Any],
    *,
    parent_attribute: dict[str, Any] | None = None,
    parent_model: dict[str, Any] | None = None,
    parent_is_type_series: bool = False,
) -> str | None:
    attribute_label = normalized_pim_label(attribute)
    if parent_attribute and (parent_is_type_series or is_type_series_parent(parent_attribute, parent_model)):
        return type_series_field_key(attribute_label)

    if is_product_name_label(attribute_label):
        return "product.name.value"
    if str(attribute.get("AttributeType") or "") == "Files" or has_any(attribute_label, ("zdjecie", "image", "photo", "file", "asset")):
        return "product.documents[].url.value"
    if has_any(attribute_label, ("link do strony www", "product url", "url", "www")):
        return "product.product_url.value"
    if has_any(attribute_label, ("opis", "description")):
        return "product.description.value"
    return None


def is_type_series_parent(
    parent_attribute: dict[str, Any],
    parent_model: dict[str, Any] | None = None,
    children: list[dict[str, Any]] | None = None,
) -> bool:
    if truthy(parent_attribute.get("SOTFlag")):
        return True
    combined_label = f"{normalized_pim_label(parent_attribute)} {normalized_pim_label(parent_model or {})}"
    if has_any(combined_label, TYPE_SERIES_PARENT_MARKERS):
        return True
    return looks_like_technical_table(parent_attribute, parent_model, children or [])


def looks_like_technical_table(
    parent_attribute: dict[str, Any],
    parent_model: dict[str, Any] | None,
    children: list[dict[str, Any]],
) -> bool:
    if str(parent_attribute.get("AttributeType") or "") != "Table_Model":
        return False
    if has_any(normalized_pim_label(parent_attribute), NON_TYPE_SERIES_TABLE_MARKERS):
        return False
    if has_any(normalized_pim_label(parent_model or {}), NON_TYPE_SERIES_TABLE_MARKERS):
        return False
    if len(children) < 2:
        return False

    technical_count = sum(1 for child in children if is_technical_value_attribute(child))
    return technical_count >= 2 and technical_count / len(children) >= 0.5


def is_technical_value_attribute(attribute: dict[str, Any]) -> bool:
    attribute_type = str(attribute.get("AttributeType") or "")
    if attribute_type in {"Number", "Int", "Integer", "Decimal", "Float"}:
        return True
    if attribute.get("Unit") not in (None, ""):
        return True
    return bool(type_series_field_key(normalized_pim_label(attribute)))


def is_product_name_label(attribute_label: str) -> bool:
    tokens = set(attribute_label.split())
    return attribute_label in {"product name", "nazwa produktu"} or bool(tokens and tokens <= {"nazwa", "name"})


def type_series_field_key(attribute_label: str) -> str | None:
    if has_any(attribute_label, ("grubosc", "thickness", "sot thickness")):
        return "type_series[].thickness.value"
    if has_any(attribute_label, ("lambda", "wspolczynnik lambda", "ld")):
        return "type_series[].lambda_value.value"
    if has_any(attribute_label, ("gestosc", "density")):
        return "type_series[].density.value"
    if has_any(attribute_label, ("mu", "vapor permeability", "paroprzepuszczalnosc")):
        return "type_series[].vapor_permeability_mu.value"
    if has_any(attribute_label, ("cieplo wlasciwe", "specific heat", "heat capacity")):
        return "type_series[].specific_heat.value"
    if has_any(attribute_label, ("kod wariantu", "variant code")):
        return "type_series[].variant_code.value"
    if has_any(attribute_label, ("nazwa wariantu", "variant name")):
        return "type_series[].variant_name.value"
    return None


def normalized_pim_label(item: dict[str, Any]) -> str:
    values = [
        text_value(item.get(key))
        for key in ("DispName", "AttributeName", "Name", "Code")
        if item.get(key) not in (None, "")
    ]
    return normalize(" ".join(values))


def has_any(text: str, needles: tuple[str, ...]) -> bool:
    return any(normalize(needle) in text for needle in needles)


def truthy(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip().casefold() in {"true", "1", "yes", "tak"}
    return bool(value)


def skip_pim_attribute(attribute: dict[str, Any]) -> bool:
    attribute_type = str(attribute.get("AttributeType") or "")
    return attribute_type in {"Colors", "ColorsGroups"} or int_value(attribute.get("Id")) in {296, 297}


def is_deleted(attribute: dict[str, Any]) -> bool:
    value = attribute.get("deleted")
    return bool(value) and str(value).casefold() not in {"false", "0", "none"}


def attribute_order(attribute: dict[str, Any]) -> tuple[int, int]:
    return (int_value(attribute.get("DisplayOrder")) or 0, int_value(attribute.get("Id")) or 0)


def int_value(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


PIM_ATTRIBUTE_KEY_OVERRIDES = {
    225: "product.name.value",
    226: "product.code.value",
    230: "product.category[].value",
    231: "product.unit.value",
    246: "product.description.value",
    247: "product.properties.value",
    248: "product.application.value",
    250: "product.usage_method.value",
    253: "product.norms.value",
    270: "product.documents[].name.value",
    272: "product.documents[].category.value",
    273: "product.documents[].url.value",
    274: "product.documents[].extension.value",
    275: "product.documents[].safe_name.value",
    255: "product.packages[].raw_text.value",
    256: "product.packages[].weight.value",
    257: "product.packages[].capacity.value",
    277: "type_series[].thickness.value",
    278: "type_series[].lambda_value.value",
    279: "type_series[].density.value",
    295: "type_series[].vapor_permeability_mu.value",
    302: "product.manufacturer.value",
    303: "product.product_url.value",
    304: "product.packages[].raw_text.value",
}


TYPE_SERIES_PARENT_MARKERS = (
    "sot",
    "series of types",
    "type series",
    "typoszereg",
    "typoszeregi",
)


NON_TYPE_SERIES_TABLE_MARKERS = (
    "document",
    "documents",
    "dokument",
    "dokumenty",
    "file",
    "files",
    "plik",
    "pliki",
    "image",
    "images",
    "zdjecie",
    "zdjecia",
    "packshot",
    "opakowanie",
    "package",
    "packages",
    "kolor",
    "color",
    "colors",
)


PIM_ATTRIBUTE_EXTRA_ALIASES = {
    270: {"file name", "document name", "caption", "podpis", "nazwa pliku"},
    272: {"file type", "document type", "typ pliku", "kategoria dokumentu"},
    273: {"files", "file", "file links", "document urls", "document_urls", "image urls", "image_urls", "packshot", "packshot_url", "url", "link"},
    274: {"extension", "rozszerzenie"},
    275: {"safe name", "safe_name"},
}


TECHNICAL_NESTED_ATTRIBUTE_IDS = {232}


def product_fields_from_payload(payload: Any) -> list[FieldDefinition]:
    items = target_field_items(payload)
    fields: list[FieldDefinition] = []
    seen: set[str] = set()
    for item in items:
        field = field_definition_from_item(item)
        if field and field.key not in seen:
            fields.append(field)
            seen.add(field.key)
    return fields


def target_field_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("target_fields", "product_fields", "fields", "attributes", "productAttributes", "product_attributes"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    for key in ("model", "product_model", "schema", "data"):
        value = payload.get(key)
        nested = target_field_items(value)
        if nested:
            return nested
    return []


def field_definition_from_item(item: dict[str, Any]) -> FieldDefinition | None:
    raw_key = first_present(item, "key", "path", "field", "code", "attributeKey", "attribute_key")
    attribute_id = first_present(item, "attribute_id", "attributeId", "AttributeId", "id", "Id")
    label = first_present(item, "label", "name", "displayName", "display_name", "attributeName", "AttributeName", "title")
    if raw_key:
        key = str(raw_key)
    elif attribute_id is not None:
        key = f"pim.attribute.{attribute_id}.value"
    else:
        return None
    label_text = text_value(label or raw_key or attribute_id)
    group = text_value(first_present(item, "group", "category", "section", "attributeGroup", "attribute_group", "parentName") or "PIM model")
    required = bool(first_present(item, "required", "mandatory", "isRequired", "is_required") or False)
    aliases = aliases_from_item(item, label_text)
    value_kind = text_value(first_present(item, "value_kind", "valueKind", "type", "AttributeType", "attribute_type") or "free_text")
    options = normalized_options(first_present(item, "options", "AttributeOptions", "values", "allowed_values"))
    unit = text_value(first_present(item, "unit", "Unit", "unit_name", "unitName") or "")
    if options and value_kind == "free_text":
        value_kind = "multi_choice" if bool(first_present(item, "multiple", "multi", "isMulti")) else "single_choice"
    return FieldDefinition(key, label_text, required, aliases, group, normalize_value_kind(value_kind), options, unit or None)


def normalize_value_kind(value: Any) -> str:
    text = normalize(value)
    if text in {"checkboxes", "multi select", "multiselect", "multi choice", "multiple", "multi_choice"}:
        return "multi_choice"
    if text in {"radio", "select", "dropdown", "list", "single choice", "single_choice"}:
        return "single_choice"
    if text in {"number", "int", "integer", "decimal", "float"}:
        return "number"
    if text in {"files", "file"}:
        return "files"
    return "free_text"


def first_present(item: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in item and item[key] not in (None, ""):
            return item[key]
    return None


def aliases_from_item(item: dict[str, Any], label: str) -> set[str]:
    aliases = {normalize(label)}
    raw_aliases = item.get("aliases") or item.get("synonyms") or []
    if isinstance(raw_aliases, str):
        raw_aliases = [raw_aliases]
    if isinstance(raw_aliases, list):
        aliases.update(normalize(alias) for alias in raw_aliases if alias not in (None, ""))
    return {alias for alias in aliases if alias}


def text_value(value: Any) -> str:
    if isinstance(value, dict):
        nested = first_present(value, "label", "name", "displayName", "display_name", "title", "value", "Name")
        return text_value(nested) if nested is not None else ""
    return str(value or "")


def suggest_mapping(rows: list[dict[str, Any]], fields: list[FieldDefinition]) -> dict[str, Any]:
    columns = columns_for_rows(rows)
    mapping: dict[str, str] = {}
    confidence: dict[str, float] = {}

    for column in columns:
        match, score = best_field_match(column, fields)
        if match and score >= 0.72:
            mapping[column] = match.key
            confidence[column] = score
        else:
            mapping[column] = "ignore"
            confidence[column] = score

    mapped_fields = set(mapping.values())
    missing_required = [field.key for field in fields if field.required and field.key not in mapped_fields]
    return {
        "mapping": mapping,
        "confidence": confidence,
        "missing_required": missing_required,
        "field_quality": field_quality(rows, mapping, fields),
        "score": mapping_score(mapping, fields),
        "target_fields": field_definitions_payload(fields),
    }


def field_definitions_payload(fields: list[FieldDefinition]) -> list[dict[str, Any]]:
    return [
        {
            "key": field.key,
            "label": field.label,
            "required": field.required,
            "group": field.group,
            "value_kind": field.value_kind,
            "options": list(field.options),
            "unit": field.unit,
        }
        for field in fields
    ]


def field_quality(rows: list[dict[str, Any]], mapping: dict[str, str], fields: list[FieldDefinition] | None = None) -> dict[str, Any]:
    quality: dict[str, Any] = {}
    fields_by_key = {field.key: field for field in fields or []}
    for source_column, target_field in mapping.items():
        if target_field == "ignore":
            continue
        values = [row.get(source_column) for row in rows]
        present = [value for value in values if value not in (None, "")]
        missing_indices = [
            index + 1
            for index, value in enumerate(values)
            if value in (None, "")
        ]
        quality[source_column] = {
            "target_field": target_field,
            "filled_rows": len(present),
            "missing_rows": len(missing_indices),
            "total_rows": len(rows),
            "missing_row_numbers": missing_indices[:20],
            "typical_values": typical_values(present),
        }
        field = fields_by_key.get(target_field)
        if field and field.options:
            quality[source_column]["choice_quality"] = choice_quality(present, field)
    return quality


def choice_quality(values: list[Any], field: FieldDefinition) -> dict[str, Any]:
    options_by_key: dict[str, dict[str, Any]] = {}
    for option in field.options:
        for key in (option.get("label"), option.get("value"), option.get("id")):
            normalized = normalize(key)
            if normalized:
                options_by_key[normalized] = option
    matched: set[str] = set()
    unmatched: set[str] = set()
    for value in values:
        for part in choice_value_parts(value, multi=field.value_kind == "multi_choice"):
            option = options_by_key.get(normalize(part))
            if option:
                matched.add(str(option.get("label") or part))
            else:
                unmatched.add(str(part))
    return {
        "value_kind": field.value_kind,
        "option_count": len(field.options),
        "matched_values": sorted(matched)[:20],
        "unmatched_values": sorted(unmatched)[:20],
    }


def choice_value_parts(value: Any, *, multi: bool) -> list[str]:
    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value or "").strip()
    if not text:
        return []
    if not multi:
        return [text]
    return [part.strip() for part in re.split(r"[;\n|,]+", text) if part.strip()]


def column_samples(rows: list[dict[str, Any]], columns: list[str], limit: int = 20) -> dict[str, list[dict[str, Any]]]:
    samples: dict[str, list[dict[str, Any]]] = {}
    for column in columns:
        values = []
        for index, row in enumerate(rows):
            value = row.get(column)
            if value in (None, ""):
                continue
            values.append({"row": index + 1, "value": value})
            if len(values) >= limit:
                break
        samples[column] = values
    return samples


def typical_values(values: list[Any], limit: int = 8) -> list[dict[str, Any]]:
    counts: dict[str, int] = {}
    for value in values:
        text = str(value).strip()
        if not text:
            continue
        counts[text] = counts.get(text, 0) + 1
    return [
        {"value": value, "count": count}
        for value, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]
    ]


def apply_column_mapping(row: dict[str, Any], mapping: dict[str, str]) -> dict[str, Any]:
    mapped: dict[str, Any] = {}
    for source_column, value in row.items():
        target = mapping.get(source_column)
        if target == "ignore":
            continue
        if not target:
            target = source_column
        mapped[target] = value
    return mapped


def apply_cleanup(value: Any, cleanup: dict[str, Any] | None, row: dict[str, Any] | None = None) -> Any:
    if not cleanup:
        return value
    if isinstance(value, (dict, list)) and cleanup_is_noop(cleanup):
        return value
    current = "" if value is None else str(value)
    if cleanup.get("trim", True):
        current = current.strip()
    remove_text = cleanup.get("removeText") or cleanup.get("remove_text")
    if remove_text:
        current = current.replace(str(remove_text), "")
    replace_from = cleanup.get("replaceFrom") or cleanup.get("replace_from")
    if replace_from:
        replace_to = cleanup.get("replaceTo") or cleanup.get("replace_to") or ""
        current = current.replace(str(replace_from), str(replace_to))
    split_by = cleanup.get("splitBy") or cleanup.get("split_by")
    if split_by:
        parts = current.split(str(split_by))
        try:
            split_part = int(cleanup.get("splitPart") or cleanup.get("split_part") or 1)
        except (TypeError, ValueError):
            split_part = 1
        if 1 <= split_part <= len(parts):
            current = parts[split_part - 1].strip()
        else:
            current = ""
    if cleanup.get("decimalComma") or cleanup.get("decimal_comma"):
        current = current.replace(",", ".")
    if cleanup.get("parseNumber") or cleanup.get("parse_number"):
        match = re.search(r"[-+]?\d*\.?\d+", current)
        current = match.group(0) if match else ""
    conversion_factor = cleanup.get("unitConversionFactor") or cleanup.get("unit_conversion_factor")
    if conversion_factor not in (None, "") and current:
        try:
            factor = float(str(conversion_factor).replace(",", "."))
            number_match = re.search(r"[-+]?\d*\.?\d+", current.replace(",", "."))
            if number_match:
                converted = float(number_match.group(0)) * factor
                current = format_converted_number(converted)
        except (TypeError, ValueError):
            pass
    source_unit = cleanup.get("unit") or ""
    unit_source_column = cleanup.get("unitSourceColumn") or cleanup.get("unit_source_column")
    if not source_unit and unit_source_column and row:
        source_unit = row.get(unit_source_column) or ""
    unit = cleanup.get("targetUnit") or cleanup.get("target_unit") or source_unit
    if unit and current:
        current = f"{current} {unit}"
    return current


def format_converted_number(value: float) -> str:
    text = f"{value:.12g}"
    return text.replace("-0", "0") if text.startswith("-0") and value == 0 else text


def cleanup_is_noop(cleanup: dict[str, Any]) -> bool:
    meaningful_keys = {
        "removeText",
        "remove_text",
        "replaceFrom",
        "replace_from",
        "replaceTo",
        "replace_to",
        "splitBy",
        "split_by",
        "splitPart",
        "split_part",
        "decimalComma",
        "decimal_comma",
        "parseNumber",
        "parse_number",
        "unit",
        "unitSourceColumn",
        "unit_source_column",
        "targetUnit",
        "target_unit",
        "unitConversionFactor",
        "unit_conversion_factor",
    }
    return all(not cleanup.get(key) for key in meaningful_keys) and cleanup.get("trim", True) is True


def apply_column_mapping_profile(row: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    mapped: dict[str, Any] = {}
    for profile_key, item in profile.items():
        if str(profile_key).startswith("_"):
            continue
        source_column = item.get("source_column") or source_column_from_profile_key(profile_key)
        value = row.get(source_column)
        target = item.get("target_path")
        if target == "ignore":
            continue
        if not target:
            target = source_column
        if target in {"custom_attribute", "type_series[].additional_properties[]"}:
            continue
        cleaned_value = apply_cleanup(value, item.get("cleanup"), row)
        options = item.get("target_options") or item.get("options") or []
        if options:
            cleaned_value = normalize_choice_mapping(
                cleaned_value,
                item.get("target_value_kind") or item.get("value_kind") or "single_choice",
                options,
                item.get("choice_map") or item.get("value_map") or {},
            )
        mapped[target] = cleaned_value
    return mapped


def mapping_profile_for_scope(profile: dict[str, Any], *, type_series: bool) -> dict[str, Any]:
    scoped: dict[str, Any] = {}
    for profile_key, item in profile.items():
        if str(profile_key).startswith("_") or not isinstance(item, dict):
            continue
        item_is_type_series = mapping_item_is_type_series(item)
        if item_is_type_series == type_series:
            scoped[profile_key] = item
    return scoped


def mapping_item_is_type_series(item: dict[str, Any]) -> bool:
    target = str(item.get("target_path") or "")
    target_group = normalize(str(item.get("target_group") or item.get("group") or ""))
    return target.startswith("type_series[]") or "type series" in target_group or "typoszereg" in target_group


def normalize_choice_mapping(value: Any, value_kind: Any, options: list[dict[str, Any]], choice_map: dict[str, Any] | None = None) -> Any:
    multi = normalize_value_kind(value_kind) == "multi_choice"
    normalized_choice_map = {normalize(key): mapped for key, mapped in (choice_map or {}).items()}
    options_by_key: dict[str, dict[str, Any]] = {}
    for option in options:
        if not isinstance(option, dict):
            continue
        for key in (option.get("label"), option.get("value"), option.get("id")):
            normalized = normalize(key)
            if normalized:
                options_by_key[normalized] = option
    selected: list[dict[str, Any]] = []
    for part in choice_value_parts(value, multi=multi):
        lookup = normalize(normalized_choice_map.get(normalize(part)) or part)
        option = options_by_key.get(lookup)
        if option:
            selected.append(
                {
                    "id": option.get("id"),
                    "label": option.get("label"),
                    "value": option.get("value"),
                    "raw": part,
                }
            )
    if multi:
        return selected
    if selected:
        return selected[0]
    return ""


def source_column_from_profile_key(profile_key: Any) -> str:
    return str(profile_key).split("::extract::", 1)[0]


def apply_mapping_profile_to_rows(rows: list[dict[str, Any]], profile: dict[str, Any]) -> list[dict[str, Any]]:
    rules = row_rule_list(profile.get("_row_rules") or {})
    if not rules:
        return [apply_column_mapping_profile(row, profile) for row in rows]

    variant_rule = next((rule for rule in rules if rule.get("row_mode") == "product_variants"), None)
    if variant_rule:
        return apply_product_variant_rule(rows, profile, variant_rule)

    contexts = [build_rule_context(rows, rule) for rule in rules]
    mapped_rows: list[dict[str, Any]] = []
    has_product_filters = any(rule_has_product_filter(rule) for rule in rules)

    for row in rows:
        group_matches = [
            index
            for index, rule in enumerate(rules)
            if is_group_row_for_rule(row, rule)
        ]
        if group_matches:
            continue
        if has_product_filters and not any(is_product_row_for_rule(row, rule) for rule in rules):
            continue

        mapped = apply_column_mapping_profile(row, profile)
        for index, rule in enumerate(rules):
            if not rule_has_product_filter(rule) or is_product_row_for_rule(row, rule):
                product_id_column = rule.get("product_id_column") or ""
                if product_id_column:
                    product_id = apply_cleanup(row.get(product_id_column), rule.get("product_id_cleanup") or {}, row)
                    if product_id not in (None, "") and mapped.get("product.code.value") in (None, ""):
                        mapped["product.code.value"] = product_id
                product_name_column = rule.get("product_name_column") or ""
                if product_name_column:
                    product_name = apply_cleanup(row.get(product_name_column), rule.get("product_name_cleanup") or {}, row)
                    if product_name not in (None, "") and mapped.get("product.name.value") in (None, ""):
                        mapped["product.name.value"] = product_name
            group_target_path = rule.get("group_target_path") or "product.category[].value"
            parent_id_column = rule.get("parent_id_column") or ""
            if parent_id_column:
                parent_context = contexts[index].get(normalize(row.get(parent_id_column)))
                if parent_context not in (None, "") and mapped.get(group_target_path) in (None, ""):
                    mapped[group_target_path] = parent_context
        mapped_rows.append(mapped)
    return mapped_rows


def apply_product_variant_rule(rows: list[dict[str, Any]], profile: dict[str, Any], rule: dict[str, Any]) -> list[dict[str, Any]]:
    products_by_id: dict[str, dict[str, Any]] = {}
    ordered_ids: list[str] = []
    id_column = rule.get("id_column") or ""
    parent_id_column = rule.get("parent_id_column") or ""
    product_profile = mapping_profile_for_scope(profile, type_series=False)
    variant_profile = mapping_profile_for_scope(profile, type_series=True)
    has_parent_reference = bool(id_column and parent_id_column)

    if has_parent_reference:
        for row in rows:
            if not is_parent_product_row_for_variant_rule(row, rule):
                continue
            product_id = normalize(row.get(id_column))
            if not product_id:
                continue
            mapped = apply_column_mapping_profile(row, product_profile)
            apply_rule_product_identity(mapped, row, rule)
            if product_id not in products_by_id:
                ordered_ids.append(product_id)
            products_by_id[product_id] = mapped

        for row in rows:
            if not is_variant_row_for_variant_rule(row, rule):
                continue
            parent_id = normalize(row.get(parent_id_column))
            if not parent_id:
                continue
            parent = products_by_id.get(parent_id)
            if parent is None:
                parent = {}
                products_by_id[parent_id] = parent
                ordered_ids.append(parent_id)
            variant = variant_mapping_from_rule(row, variant_profile, rule)
            apply_variant_to_product(parent, variant)
    else:
        current_product_id = ""
        for row in rows:
            if is_parent_product_row_for_variant_rule(row, rule):
                product_id = f"product-{len(ordered_ids) + 1}"
                mapped = apply_column_mapping_profile(row, product_profile)
                apply_rule_product_identity(mapped, row, rule)
                ordered_ids.append(product_id)
                products_by_id[product_id] = mapped
                current_product_id = product_id
                continue
            if is_variant_row_for_variant_rule(row, rule) and current_product_id:
                variant = variant_mapping_from_rule(row, variant_profile, rule)
                apply_variant_to_product(products_by_id[current_product_id], variant)

    return [products_by_id[product_id] for product_id in ordered_ids if products_by_id.get(product_id)]


def variant_mapping_from_rule(row: dict[str, Any], variant_profile: dict[str, Any], rule: dict[str, Any]) -> dict[str, Any]:
    variant = apply_column_mapping_profile(row, variant_profile)
    variant_id_column = rule.get("variant_id_column") or ""
    if variant_id_column and variant.get("type_series[].variant_code.value") in (None, ""):
        variant_code = apply_cleanup(row.get(variant_id_column), rule.get("variant_id_cleanup") or {}, row)
        if variant_code not in (None, ""):
            variant["type_series[].variant_code.value"] = variant_code
    variant_name_column = rule.get("variant_name_column") or ""
    if variant_name_column:
        variant_name = apply_cleanup(row.get(variant_name_column), rule.get("variant_name_cleanup") or {}, row)
        if variant_name not in (None, ""):
            variant["type_series[].variant_name.value"] = variant_name
    return variant


def apply_rule_product_identity(mapped: dict[str, Any], row: dict[str, Any], rule: dict[str, Any]) -> None:
    product_id_column = rule.get("product_id_column") or ""
    if product_id_column:
        product_id = apply_cleanup(row.get(product_id_column), rule.get("product_id_cleanup") or {}, row)
        if product_id not in (None, ""):
            mapped["product.code.value"] = product_id
    product_name_column = rule.get("product_name_column") or ""
    if product_name_column:
        product_name = apply_cleanup(row.get(product_name_column), rule.get("product_name_cleanup") or {}, row)
        if product_name not in (None, ""):
            mapped["product.name.value"] = product_name
    group_source_column = rule.get("group_source_column") or ""
    group_target_path = rule.get("group_target_path") or "product.category[].value"
    if group_source_column:
        group_value = apply_cleanup(row.get(group_source_column), rule.get("group_source_cleanup") or {}, row)
        if group_value not in (None, "") and mapped.get(group_target_path) in (None, ""):
            mapped[group_target_path] = group_value


def apply_variant_to_product(product: dict[str, Any], variant: dict[str, Any]) -> None:
    variant_data = {key: value for key, value in variant.items() if value not in (None, "")}
    rows = product.setdefault("_type_series_rows", [])
    if not variant_data.get("type_series[].variant_code.value"):
        variant_data["type_series[].variant_code.value"] = str(len(rows) + 1)
    rows.append(variant_data)


def row_rule_list(row_rules: dict[str, Any] | list[Any]) -> list[dict[str, Any]]:
    if isinstance(row_rules, list):
        return [rule for rule in row_rules if isinstance(rule, dict)]
    if not isinstance(row_rules, dict):
        return []
    rules = row_rules.get("rules")
    if isinstance(rules, list):
        return [rule for rule in rules if isinstance(rule, dict)]
    return [row_rules] if row_rules else []


def build_rule_context(rows: list[dict[str, Any]], rule: dict[str, Any]) -> dict[str, Any]:
    id_column = rule.get("id_column") or ""
    group_source_column = rule.get("group_source_column") or ""
    if not id_column or not group_source_column:
        return {}
    context: dict[str, Any] = {}
    for row in rows:
        if is_group_row_for_rule(row, rule):
            group_id = normalize(row.get(id_column))
            group_value = apply_cleanup(row.get(group_source_column), rule.get("group_cleanup") or {}, row)
            if group_id and group_value not in (None, ""):
                context[group_id] = group_value
    return context


def rule_has_product_filter(rule: dict[str, Any]) -> bool:
    return bool(normalized_set(rule.get("product_row_values") or []))


def is_group_row_for_rule(row: dict[str, Any], rule: dict[str, Any]) -> bool:
    row_type_column = rule.get("row_type_column") or ""
    group_values = normalized_set(rule.get("group_row_values") or [])
    return is_group_row(row, row_type_column, group_values)


def is_product_row_for_rule(row: dict[str, Any], rule: dict[str, Any]) -> bool:
    row_type_column = rule.get("row_type_column") or ""
    product_values = normalized_set(rule.get("product_row_values") or [])
    return is_product_row(row, row_type_column, product_values)


def is_parent_product_row_for_variant_rule(row: dict[str, Any], rule: dict[str, Any]) -> bool:
    return is_product_row_for_rule(row, rule)


def is_variant_row_for_variant_rule(row: dict[str, Any], rule: dict[str, Any]) -> bool:
    return is_group_row_for_rule(row, rule)


def is_group_row(
    row: dict[str, Any],
    row_type_column: str,
    group_values: set[str],
) -> bool:
    row_type = normalize(row.get(row_type_column)) if row_type_column else ""
    return bool(group_values and row_type in group_values)


def is_product_row(
    row: dict[str, Any],
    row_type_column: str,
    product_values: set[str],
) -> bool:
    row_type = normalize(row.get(row_type_column)) if row_type_column else ""
    return bool(product_values and row_type in product_values)


def normalized_set(values: list[Any] | str) -> set[str]:
    if isinstance(values, str):
        values = [item.strip() for item in re.split(r"[,;|\n]+", values)]
    return {normalize(value) for value in values if str(value).strip()}


def columns_for_rows(rows: list[dict[str, Any]]) -> list[str]:
    seen: list[str] = []
    for row in rows[:25]:
        for key in row.keys():
            if key not in seen:
                seen.append(key)
    return seen


def best_field_match(column: str, fields: list[FieldDefinition]) -> tuple[FieldDefinition | None, float]:
    normalized = normalize(column)
    best: tuple[FieldDefinition | None, float] = (None, 0.0)
    for field in fields:
        candidates = {field.key, field.label, *field.aliases}
        for candidate in candidates:
            score = similarity(normalized, normalize(candidate))
            if score > best[1]:
                best = (field, score)
    return best


def mapping_score(mapping: dict[str, str], fields: list[FieldDefinition]) -> float:
    if not mapping:
        return 0.0
    mapped = set(mapping.values())
    required = [field.key for field in fields if field.required]
    required_hits = sum(1 for key in required if key in mapped)
    optional_hits = sum(1 for field in fields if field.key in mapped and not field.required)
    return round(required_hits * 0.35 + min(optional_hits, 6) * 0.08, 3)


def similarity(left: str, right: str) -> float:
    if left == right:
        return 1.0
    if left in right or right in left:
        return min(len(left), len(right)) / max(len(left), len(right))
    left_tokens = set(left.split())
    right_tokens = set(right.split())
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def normalize(value: Any) -> str:
    text = str(value or "").strip().casefold()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    replacements = {
        "ą": "a",
        "ć": "c",
        "ę": "e",
        "ł": "l",
        "ń": "n",
        "ó": "o",
        "ś": "s",
        "ż": "z",
        "ź": "z",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    text = text.replace("µ", "mu").replace("μ", "mu").replace("λ", "lambda")
    text = re.sub(r"[_\-/]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text
