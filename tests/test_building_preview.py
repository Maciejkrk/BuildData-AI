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
