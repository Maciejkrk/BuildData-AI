from __future__ import annotations

from mapping_studio.services.product_reference import build_product_reference_index


def test_product_reference_indexes_exported_products_by_id_name_and_code() -> None:
    payload = b"""{
      "productsCount": 1,
      "products": [
        {
          "Id": 6076,
          "dataVersions": [
            {
              "productAttributes": [
                {"AttributeId": 225, "varcharValue": "FAST AQUA"},
                {"AttributeId": 226, "varcharValue": "SKU-1"}
              ]
            }
          ]
        }
      ]
    }"""

    index = build_product_reference_index(payload)

    assert index.products_count == 1
    assert index.by_id["6076"]["Id"] == 6076
    assert index.by_name["fastaqua"]["Id"] == 6076
    assert index.by_code["sku1"]["Id"] == 6076


def test_product_reference_indexes_current_export_and_type_series_aliases() -> None:
    payload = b"""{
      "productsCount": 1,
      "products": [
        {
          "Id": 900001,
          "dataVersions": [
            {
              "productAttributes": [
                {"AttributeId": 116, "varcharValue": "Rigips PRO"},
                {"AttributeId": 318, "varcharValue": "PR00058890"},
                {"ParentAttributeId": 135, "AttributeId": 319, "RowI": 0, "varcharValue": "11620533", "hash": "variant-hash-1"},
                {"ParentAttributeId": 135, "AttributeId": 321, "RowI": 0, "varcharValue": "AR00233378", "hash": "variant-hash-1"}
              ]
            }
          ]
        }
      ]
    }"""

    index = build_product_reference_index(payload)

    assert index.by_name["rigipspro"]["Id"] == 900001
    assert index.by_code["pr00058890"]["Id"] == 900001
    assert index.by_name["11620533"]["Id"] == 900001
    assert index.by_code["ar00233378"]["Id"] == 900001
    assert index.by_variant["11620533"]["product"]["Id"] == 900001
    assert index.by_variant["ar00233378"]["product"]["Id"] == 900001

