from __future__ import annotations

from mapping_studio.models import FieldKind
from mapping_studio.services.pim_model_loader import load_building_element_model


def test_building_element_model_relations_are_read_from_export() -> None:
    files = {
        "buildingsElementsModels.json": b"""{
          "models": [
            {"Id": 74, "Name": "Building Element", "modelType": "Building_Element"},
            {"Id": 75, "Name": "Variant", "modelType": "Attribute"},
            {"Id": 76, "Name": "Layer", "modelType": "Attribute"},
            {"Id": 77, "Name": "Available Product", "modelType": "Attribute"}
          ]
        }""",
        "buildingsElementsAttributes.json": b"""{
          "attributes": [
            {"Id": 280, "ProductModelId": 74, "AttributeName": "name", "DispName": "Name", "AttributeType": "VarChar", "deleted": false},
            {"Id": 283, "ProductModelId": 74, "AttributeName": "variants", "DispName": "Variants", "AttributeType": "Model_Array", "TargetModelId": 75, "deleted": false},
            {"Id": 284, "ProductModelId": 75, "AttributeName": "variant_name", "DispName": "Variant Name", "AttributeType": "VarChar", "deleted": false},
            {"Id": 285, "ProductModelId": 75, "AttributeName": "layers", "DispName": "Layers", "AttributeType": "Model_Array", "TargetModelId": 76, "deleted": false},
            {"Id": 287, "ProductModelId": 76, "AttributeName": "layer_name", "DispName": "Layer name", "AttributeType": "VarChar", "deleted": false},
            {"Id": 289, "ProductModelId": 76, "AttributeName": "available_products", "DispName": "Available products", "AttributeType": "Model_Array", "TargetModelId": 77, "deleted": false},
            {"Id": 290, "ProductModelId": 77, "AttributeName": "product", "DispName": "Product", "AttributeType": "Product", "deleted": false}
          ]
        }""",
    }

    bundle = load_building_element_model(files)

    assert bundle.root_model_id == 74
    assert [relation.attribute_id for relation in bundle.relations] == [283, 285, 289]
    product_fields = [field for field in bundle.fields if field.attribute_id == 290]
    assert product_fields[0].kind == FieldKind.PRODUCT_REF


def test_deleted_attributes_are_not_exposed() -> None:
    files = {
        "buildingsElementsModels.json": b"""{
          "models": [{"Id": 74, "Name": "Building Element", "modelType": "Building_Element"}]
        }""",
        "buildingsElementsAttributes.json": b"""{
          "attributes": [
            {"Id": 280, "ProductModelId": 74, "AttributeName": "name", "DispName": "Name", "AttributeType": "VarChar", "deleted": false},
            {"Id": 293, "ProductModelId": 74, "AttributeName": "plaster_type", "DispName": "Rodzaj tynku", "AttributeType": "Select", "deleted": true}
          ]
        }""",
    }

    bundle = load_building_element_model(files)

    assert [field.attribute_id for field in bundle.fields] == [280]

