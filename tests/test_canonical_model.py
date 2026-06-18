from __future__ import annotations

import unittest

from data_master_app.canonical_model import (
    Confidence,
    DataSource,
    FieldValue,
    Product,
    TypeSeriesRow,
    inferred_normative_measurement,
    measurement,
    missing_field,
)


class CanonicalProductModelTests(unittest.TestCase):
    def test_product_keeps_source_metadata_on_fields(self):
        product = Product(
            pim_product_id=FieldValue(value=6076, source=DataSource.PIM_REFERENCE),
            code=FieldValue(value="SKU-1", source=DataSource.CLIENT),
            name=FieldValue(value="FAST TEST", source=DataSource.CLIENT),
            product_url=FieldValue(value="https://example.com/fast-test", source=DataSource.CLIENT),
            type_series=[
                TypeSeriesRow(
                    thickness=measurement(0.05, unit="m", source=DataSource.CLIENT),
                    lambda_value=inferred_normative_measurement(
                        0.035,
                        unit="W/mK",
                        rule_id="mineral_wool_default_lambda",
                        reason="Brak lambda w danych klienta.",
                    ),
                    specific_heat=inferred_normative_measurement(
                        1030,
                        unit="J/kgK",
                        rule_id="mineral_wool_default_specific_heat",
                        reason="Brak ciepla wlasciwego w danych klienta.",
                    ),
                )
            ],
        )

        self.assertEqual(product.model_version, "product.v1")
        self.assertEqual(product.name.source, DataSource.CLIENT)
        self.assertEqual(product.pim_product_id.source, DataSource.PIM_REFERENCE)
        self.assertEqual(product.type_series[0].lambda_value.value.source, DataSource.NORMATIVE_MODEL)
        self.assertEqual(product.type_series[0].lambda_value.unit.value, "W/mK")
        self.assertTrue(product.type_series[0].lambda_value.value.requires_review)
        self.assertEqual(product.type_series[0].specific_heat.unit.value, "J/kgK")

    def test_missing_field_is_explicit(self):
        field = missing_field("Klient nie podal producenta.")

        self.assertIsNone(field.value)
        self.assertEqual(field.confidence, Confidence.MISSING)
        self.assertTrue(field.requires_review)


if __name__ == "__main__":
    unittest.main()
