from __future__ import annotations

from mapping_studio.services.building_preview import preview_building_elements
from mapping_studio.services.product_reference import build_product_reference_index


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

