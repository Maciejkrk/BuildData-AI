from __future__ import annotations

import json
from pathlib import Path

from mapping_studio.services.building_preview import convert_building_elements_from_tables, preview_building_elements, preview_building_elements_from_tables
from mapping_studio.services.pim_model_loader import load_building_element_model
from mapping_studio.services.product_reference import build_product_reference_index
from mapping_studio.services.source_reader import SourceTable


def test_building_preview_requires_resolved_product_reference() -> None:
    product_index = build_product_reference_index(
        b"""{
          "products": [
            {
              "Id": 10,
              "dataVersions": [{"productAttributes": [{"AttributeId": 225, "varcharValue": "FAST A"}]}]
            }
          ]
        }"""
    )
    rows = [
        {
            "Nazwa systemu": "System 1",
            "Wariant": "Wariant A",
            "Nazwa warstwy": "Warstwa 1",
            "Nazwa produktu": "FAST A",
        },
        {
            "Nazwa systemu": "System 1",
            "Wariant": "Wariant A",
            "Nazwa warstwy": "Warstwa 2",
            "Nazwa produktu": "Nieznany produkt",
        },
    ]

    preview = preview_building_elements(rows, {}, product_index)

    assert preview["quality"]["systems"] == 1
    assert preview["quality"]["unresolved_products_count"] == 1
    assert preview["systems"][0]["variants"][0]["layers"][0]["products"][0]["resolved"] is True


def test_building_preview_can_start_without_product_reference() -> None:
    rows = [
        {
            "Nazwa systemu": "System 1",
            "Wariant": "Wariant A",
            "Nazwa warstwy": "Warstwa 1",
            "Nazwa produktu": "Produkt do pozniejszego dopasowania",
        }
    ]

    preview = preview_building_elements(rows, {}, None)

    assert preview["quality"]["systems"] == 1
    assert preview["quality"]["product_reference_loaded"] is False
    assert preview["quality"]["unresolved_products_count"] == 1
    assert preview["systems"][0]["variants"][0]["layers"][0]["products"][0]["resolved"] is False


def test_building_preview_can_page_parent_systems() -> None:
    rows = [
        {"Nazwa systemu": "System 1", "Wariant": "A", "Warstwa": "L1", "Produkt": "P1"},
        {"Nazwa systemu": "System 2", "Wariant": "A", "Warstwa": "L1", "Produkt": "P2"},
        {"Nazwa systemu": "System 3", "Wariant": "A", "Warstwa": "L1", "Produkt": "P3"},
    ]

    preview = preview_building_elements(rows, {}, None, preview_offset=1, preview_limit=1)

    assert preview["quality"]["systems"] == 3
    assert preview["quality"]["preview_systems_count"] == 1
    assert preview["quality"]["has_previous"] is True
    assert preview["quality"]["has_next"] is True
    assert [system["name"] for system in preview["systems"]] == ["System 2"]


def test_building_preview_reads_profile_table_column_and_cleanup() -> None:
    tables = [
        SourceTable(
            "Systemy",
            [
                {
                    "System": "ETICS",
                    "Wariant": "Mineralny",
                    "Warstwa": "Izolacja",
                    "Produkt": "  SKU-1  ",
                }
            ],
        )
    ]
    profile = {
        "building_element.name.value": {"table": "Systemy", "column": "System", "cleanup": {"trim": True}},
        "building_element.variant_name.value": {"table": "Systemy", "column": "Wariant", "cleanup": {"trim": True}},
        "building_element.layer_name.value": {"table": "Systemy", "column": "Warstwa", "cleanup": {"trim": True}},
        "building_element.product.value": {"table": "Systemy", "column": "Produkt", "cleanup": {"trim": True}},
    }

    preview = preview_building_elements_from_tables(tables, profile, None)

    assert preview["systems"][0]["name"] == "ETICS"
    assert preview["systems"][0]["variants"][0]["name"] == "Mineralny"
    assert preview["systems"][0]["variants"][0]["layers"][0]["name"] == "Izolacja"
    assert preview["systems"][0]["variants"][0]["layers"][0]["products"][0]["raw"] == "SKU-1"


def test_building_preview_from_tables_keeps_exact_system_count() -> None:
    tables = [
        SourceTable(
            "Systemy",
            [
                {"System": "S1", "Wariant": "A", "Warstwa": "L1", "Produkt": "P1"},
                {"System": "S2", "Wariant": "A", "Warstwa": "L1", "Produkt": "P2"},
                {"System": "S3", "Wariant": "A", "Warstwa": "L1", "Produkt": "P3"},
            ],
        )
    ]
    profile = {
        "building_element.name.value": {"table": "Systemy", "column": "System"},
        "building_element.variant_name.value": {"table": "Systemy", "column": "Wariant"},
        "building_element.layer_name.value": {"table": "Systemy", "column": "Warstwa"},
        "building_element.product.value": {"table": "Systemy", "column": "Produkt"},
    }

    preview = preview_building_elements_from_tables(tables, profile, None, preview_offset=0, preview_limit=1)

    assert preview["quality"]["systems"] == 3
    assert preview["quality"]["systems_count_is_exact"] is True
    assert preview["quality"]["has_next"] is True
    assert [system["name"] for system in preview["systems"]] == ["S1"]


def test_building_preview_joins_parent_element_with_many_layer_rows() -> None:
    tables = [
        SourceTable(
            "Elementy",
            [
                {"Element": "ETICS-1", "Wariant": "Mineralny", "Typ": "ETICS"},
                {"Element": "ETICS-2", "Wariant": "EPS", "Typ": "ETICS"},
            ],
        ),
        SourceTable(
            "Warstwy",
            [
                {"Element": "ETICS-1", "Pozycja": 1, "Warstwa": "Klej", "Produkt": "P1"},
                {"Element": "ETICS-1", "Pozycja": 2, "Warstwa": "Izolacja", "Produkt": "P2"},
                {"Element": "ETICS-2", "Pozycja": 1, "Warstwa": "Izolacja", "Produkt": "P3"},
            ],
        ),
    ]
    profile = {
        "_levels": {
            "model.74": {"table": "Elementy", "level_name_field": "building_element.name.value"},
            "model.74.attribute.285": {"table": "Warstwy", "parent_id_column": "Element"},
        },
        "building_element.name.value": {"level": "model.74", "table": "Elementy", "column": "Element"},
        "building_element.variant_name.value": {"level": "model.74", "table": "Elementy", "column": "Wariant"},
        "building_element.typ_systemu.value": {"level": "model.74", "table": "Elementy", "column": "Typ"},
        "building_element.layer_position.value": {"level": "model.74.attribute.285", "table": "Warstwy", "column": "Pozycja"},
        "building_element.layer_name.value": {"level": "model.74.attribute.285", "table": "Warstwy", "column": "Warstwa"},
        "building_element.product.value": {"level": "model.74.attribute.285", "table": "Warstwy", "column": "Produkt"},
    }

    preview = preview_building_elements_from_tables(tables, profile, None, preview_offset=0, preview_limit=1)

    system = preview["systems"][0]
    layers = system["variants"][0]["layers"]
    assert system["name"] == "ETICS-1"
    assert [layer["name"] for layer in layers] == ["Klej", "Izolacja"]
    assert [layer["products"][0]["raw"] for layer in layers] == ["P1", "P2"]
    assert preview["quality"]["systems"] == 2


def test_building_elements_convert_writes_json_from_profile(tmp_path: Path) -> None:
    model = load_building_element_model(
        {
            "buildingElementsModels.json": b"""{
              "models": [
                {"Id": 74, "Name": "Building Element", "modelType": "Building_Element"},
                {"Id": 75, "Name": "Variant", "modelType": "Attribute"},
                {"Id": 76, "Name": "Layer", "modelType": "Attribute"}
              ]
            }""",
            "buildingElementsAttributes.json": b"""{
              "attributes": [
                {"Id": 280, "ProductModelId": 74, "AttributeName": "name", "DispName": "Name", "AttributeType": "VarChar", "deleted": false},
                {"Id": 283, "ProductModelId": 74, "AttributeName": "variants", "DispName": "Variants", "AttributeType": "Model_Array", "TargetModelId": 75, "deleted": false},
                {"Id": 284, "ProductModelId": 75, "AttributeName": "variant_name", "DispName": "Variant Name", "AttributeType": "VarChar", "deleted": false},
                {"Id": 285, "ProductModelId": 75, "AttributeName": "layers", "DispName": "Layers", "AttributeType": "Model_Array", "TargetModelId": 76, "deleted": false},
                {"Id": 287, "ProductModelId": 76, "AttributeName": "layer_name", "DispName": "Layer name", "AttributeType": "VarChar", "deleted": false}
              ]
            }""",
        }
    )
    tables = [SourceTable("Systemy", [{"System": "S1", "Wariant": "W1", "Warstwa": "L1"}])]
    profile = {
        "_levels": {"model.74": {"level_name_field": "building_element.name.value"}},
        "building_element.name.value": {"table": "Systemy", "column": "System", "cleanup": {"trim": True}},
        "building_element.variant_name.value": {"table": "Systemy", "column": "Wariant", "cleanup": {"trim": True}},
        "building_element.layer_name.value": {"table": "Systemy", "column": "Warstwa", "cleanup": {"trim": True}},
    }

    result = convert_building_elements_from_tables("systems.json", b"{}", tables, profile, model, None, tmp_path)
    payload = json.loads((tmp_path / result["job_id"] / "building_elements.json").read_text(encoding="utf-8"))

    assert result["building_elements_count"] == 1
    attrs = payload["buildingElements"][0]["dataVersions"][0]["productAttributes"]
    assert any(attr["AttributeId"] == 280 and attr["varcharValue"] == "S1" for attr in attrs)
    assert any(attr["AttributeId"] == 284 and attr["ParentAttributeId"] == 283 for attr in attrs)
    assert any(attr["AttributeId"] == 287 and attr["ParentAttributeId"] == 285 for attr in attrs)


def test_building_elements_product_ref_can_point_to_product_variant_hash(tmp_path: Path) -> None:
    model = load_building_element_model(
        {
            "buildingElementsModels.json": b"""{
              "models": [
                {"Id": 46, "Name": "Struktura warstwowa", "modelType": "Building_Element"},
                {"Id": 48, "Name": "Model wariantu BE", "modelType": "Attribute"},
                {"Id": 47, "Name": "Model produktu BE", "modelType": "Attribute"},
                {"Id": 87, "Name": "Duzo produktow", "modelType": "Attribute"}
              ]
            }""",
            "buildingElementsAttributes.json": b"""{
              "attributes": [
                {"Id": 142, "ProductModelId": 46, "AttributeName": "Nazwa systemu", "DispName": "Nazwa systemu", "AttributeType": "VarChar", "deleted": false},
                {"Id": 145, "ProductModelId": 46, "AttributeName": "Warianty", "DispName": "Warianty", "AttributeType": "Model_Array", "TargetModelId": 48, "deleted": false},
                {"Id": 332, "ProductModelId": 48, "AttributeName": "Nazwa wariantu", "DispName": "Nazwa wariantu", "AttributeType": "VarChar", "deleted": false},
                {"Id": 144, "ProductModelId": 48, "AttributeName": "Warstwy", "DispName": "Warstwy", "AttributeType": "Model_Array", "TargetModelId": 47, "deleted": false},
                {"Id": 146, "ProductModelId": 47, "AttributeName": "Nazwa warstwy", "DispName": "Nazwa warstwy", "AttributeType": "Text", "deleted": false},
                {"Id": 143, "ProductModelId": 47, "AttributeName": "Produkty w warstwie", "DispName": "Produkty w warstwie", "AttributeType": "Model_Array", "TargetModelId": 87, "deleted": false},
                {"Id": 333, "ProductModelId": 87, "AttributeName": "Produkt", "DispName": "Produkt", "AttributeType": "Product", "deleted": false}
              ]
            }""",
        }
    )
    variant_hash = "227306e72ac7c4487916577c76d1d916"
    product_index = build_product_reference_index(
        f"""{{
          "products": [
            {{
              "Id": 2945,
              "dataVersions": [{{"productAttributes": [
                {{"AttributeId": 225, "varcharValue": "ISOVER Fasoterm 35"}},
                {{"AttributeId": 321, "ParentAttributeId": 135, "RowI": 0, "varcharValue": "11111", "hash": "{variant_hash}"}}
              ]}}]
            }},
            {{
              "Id": 4469,
              "dataVersions": [{{"productAttributes": [
                {{"AttributeId": 225, "varcharValue": "ISOVER Super-Mata Plus"}}
              ]}}]
            }}
          ]
        }}""".encode("utf-8")
    )
    tables = [
        SourceTable(
            "Systemy",
            [
                {
                    "System": "S1",
                    "Wariant": "W1",
                    "Warstwa": "Izolacja",
                    "Produkty": "11111, ISOVER Super-Mata Plus",
                    "Typ": "ETICS",
                    "Grubosc": "200 mm",
                }
            ],
        )
    ]
    profile = {
        "_levels": {"model.46": {"level_name_field": "building_element.nazwa_systemu.value"}},
        "building_element.nazwa_systemu.value": {"table": "Systemy", "column": "System", "cleanup": {"trim": True}},
        "building_element.nazwa_wariantu.value": {"table": "Systemy", "column": "Wariant", "cleanup": {"trim": True}},
        "building_element.nazwa_warstwy.value": {"table": "Systemy", "column": "Warstwa", "cleanup": {"trim": True}},
        "building_element.produkt.value": {"table": "Systemy", "column": "Produkty", "cleanup": {"trim": True}},
        "building_element.typ_systemu.value": {"table": "Systemy", "column": "Typ", "cleanup": {"trim": True}},
        "building_element.grubosc.value": {"table": "Systemy", "column": "Grubosc", "cleanup": {"trim": True}},
    }

    preview = preview_building_elements_from_tables(tables, profile, product_index)

    preview_products = preview["systems"][0]["variants"][0]["layers"][0]["products"]
    assert preview["systems"][0]["name"] == "S1"
    assert preview["systems"][0]["variants"][0]["name"] == "W1"
    assert preview["systems"][0]["variants"][0]["layers"][0]["name"] == "Izolacja"
    preview_features = preview["systems"][0]["variants"][0]["layers"][0]["features"]
    assert [(item["key"], item["value"]) for item in preview_features] == [
        ("building_element.typ_systemu.value", "ETICS"),
        ("building_element.grubosc.value", "200 mm"),
    ]
    assert [(item["product_id"], item["variant_hash"], item["identity_source"]) for item in preview_products] == [
        (2945, variant_hash, "variant"),
        (4469, "", "name"),
    ]
    assert [(item["variant_scope"], item["variant_scope_label"]) for item in preview_products] == [
        ("specific_variant", "tylko wskazany wariant"),
        ("all_variants", "wszystkie warianty produktu"),
    ]

    result = convert_building_elements_from_tables("systems.xlsx", b"{}", tables, profile, model, product_index, tmp_path)
    payload = json.loads((tmp_path / result["job_id"] / "building_elements.json").read_text(encoding="utf-8"))

    product_attrs = [
        attr
        for attr in payload["buildingElements"][0]["dataVersions"][0]["productAttributes"]
        if attr["AttributeId"] == 333
    ]
    assert [(attr["IntValue"], attr["varcharValue"]) for attr in product_attrs] == [
        (2945, variant_hash),
        (4469, ""),
    ]
