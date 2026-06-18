from __future__ import annotations

import unittest

from data_master_app.mapping_model import (
    ColumnMappingRule,
    MappingTargetKind,
    TypicalDataAction,
    TypicalDataProfile,
    TypicalDataRule,
    ValueTransform,
    ValueTransformKind,
    apply_text_transforms,
)


class MappingModelTests(unittest.TestCase):
    def test_model_field_rule_keeps_unit(self):
        rule = ColumnMappingRule(
            source_column="Wytrzymalosc",
            target_kind=MappingTargetKind.TYPE_SERIES_FIELD,
            target_path="pim.attribute.501.value",
            unit="kPa",
        )

        self.assertEqual(rule.target_path, "pim.attribute.501.value")
        self.assertEqual(rule.unit, "kPa")

    def test_value_transforms_clean_descriptive_number(self):
        result = apply_text_transforms(
            "okolo 0,035 W/mK",
            [
                ValueTransform(kind=ValueTransformKind.REMOVE_TEXT, search="okolo"),
                ValueTransform(kind=ValueTransformKind.REMOVE_TEXT, search="W/mK"),
                ValueTransform(kind=ValueTransformKind.DECIMAL_COMMA_TO_DOT),
                ValueTransform(kind=ValueTransformKind.PARSE_NUMBER),
            ],
        )

        self.assertEqual(result, 0.035)

    def test_typical_data_rule_can_fill_missing_type_series_field(self):
        profile = TypicalDataProfile(
            name="Dane typowe izolacji",
            rules=[
                TypicalDataRule(
                    rule_id="mineral_wool_specific_heat",
                    action=TypicalDataAction.FILL_IF_MISSING,
                    target_path="type_series[].specific_heat.value",
                    typical_source_path="materials.mineral_wool.specific_heat",
                    condition_path="product.category[].value",
                    condition_value="Welna mineralna",
                    reason="Brak ciepla wlasciwego w danych klienta.",
                )
            ],
        )

        self.assertEqual(profile.rules[0].action, TypicalDataAction.FILL_IF_MISSING)
        self.assertTrue(profile.rules[0].requires_review)


if __name__ == "__main__":
    unittest.main()
