from __future__ import annotations

from mapping_studio.services.building_preview import preview_building_elements, preview_building_elements_from_tables
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
