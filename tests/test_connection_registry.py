from __future__ import annotations

from mapping_studio.services.connection_registry import build_connection_registry


def test_product_connection_registry_normalizes_mapping_profile() -> None:
    registry = build_connection_registry(
        scope="products",
        source_file="client.xlsx",
        root_model_id=41,
        mapping_profile={
            "Nazwa": {
                "source_column": "Nazwa",
                "target_path": "product.name.value",
                "target_label": "Nazwa produktu",
                "target_group": "Product identity",
                "cleanup": {"trim": True},
            },
            "Typ": {"target_path": "ignore"},
        },
    )

    assert registry["schema"] == "builddata.connection_registry.v1"
    assert registry["scope"] == "products"
    assert registry["source"]["file"] == "client.xlsx"
    assert registry["target"]["root_model_id"] == 41
    assert registry["summary"] == {
        "connections": 2,
        "active_connections": 1,
        "ignored_connections": 1,
        "levels": 0,
    }
    assert registry["connections"][0]["source"]["column"] == "Nazwa"
    assert registry["connections"][0]["target"]["path"] == "product.name.value"


def test_building_connection_registry_keeps_levels() -> None:
    registry = build_connection_registry(
        scope="building_elements",
        source_file="systems.xlsx",
        root_model_id=74,
        mapping_profile={
            "_levels": {
                "model.74": {"table": "Systems", "id_column": "SystemId"},
                "model.74.attribute.283": {
                    "table": "Variants",
                    "id_column": "VariantId",
                    "parent_id_column": "SystemId",
                },
            },
            "building_element.name.value": {"table": "Systems", "column": "System"},
            "building_element.variant.value": {
                "table": "Variants",
                "column": "Variant",
                "level": "model.74.attribute.283",
            },
        },
    )

    assert registry["summary"]["active_connections"] == 2
    assert registry["summary"]["levels"] == 2
    assert registry["levels"][1]["parent_id_column"] == "SystemId"
    assert registry["connections"][1]["level"] == "model.74.attribute.283"
