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

