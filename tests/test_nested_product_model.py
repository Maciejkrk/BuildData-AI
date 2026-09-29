import json

import pytest

from data_master_app.converter import (
    convert_products_file,
    export_schema_from_pim_bundle,
    normalize_nested_product_attribute_hashes,
)
from data_master_app.mapping import product_fields_from_pim_bundle


@pytest.mark.parametrize('relation_type', ['Model', 'Model_Array', 'Table_Model'])
def test_nested_product_fields_are_mappable_and_export_with_parent(relation_type, tmp_path):
    files = {
        'productsModels.json': json.dumps({'models': [
            {'Id': 146, 'Name': 'Product', 'modelType': 'Product'},
            {'Id': 150, 'Name': 'Packaging', 'modelType': 'Attribute'},
        ]}),
        'productsAttributes.json': json.dumps({'attributes': [
            {'Id': 660, 'ProductModelId': 146, 'DispName': 'Name', 'AttributeType': 'VarChar'},
            {'Id': 733, 'ProductModelId': 146, 'DispName': 'Packaging', 'AttributeType': relation_type, 'TargetModelId': 150},
            {'Id': 734, 'ProductModelId': 150, 'DispName': 'Package label', 'AttributeType': 'Text'},
            {'Id': 739, 'ProductModelId': 150, 'DispName': 'Package count', 'AttributeType': 'Number'},
        ]}),
    }
    fields = {field.key: field for field in product_fields_from_pim_bundle(files)}
    assert set(fields) == {'product.name.value', 'pim.attribute.734.value', 'pim.attribute.739.value'}
    assert fields['pim.attribute.734.value'].group == 'Packaging'
    assert fields['pim.attribute.739.value'].value_kind == 'number'
    schema = export_schema_from_pim_bundle(files)
    assert schema.product_parent_by_attribute_id[734] == 733
    assert schema.product_parent_by_attribute_id[739] == 733
    assert schema.product_main_model_for_attribute(734) == 150
    assert schema.product_main_model_for_attribute(739) == 150
    convert_products_file(
        'source.json', json.dumps([{'name': 'Panel', 'pack': 'Box', 'count': 12}]).encode(), tmp_path,
        product_mapping={'name': 'product.name.value', 'pack': 'pim.attribute.734.value', 'count': 'pim.attribute.739.value'},
        product_model_files=files,
    )
    payload = json.loads(next(tmp_path.rglob('products.json')).read_text(encoding='utf-8'))
    attrs = payload['products'][0]['dataVersions'][0]['productAttributes']
    assert any(a['AttributeId'] == 734 and a['ParentAttributeId'] == 733 and a['MainAttributeId'] == 150 for a in attrs)
    assert any(a['AttributeId'] == 739 and a['ParentAttributeId'] == 733 and a['MainAttributeId'] == 150 for a in attrs)
    nested = [a for a in attrs if a['ParentAttributeId'] == 733]
    assert len({a['hash'] for a in nested}) == 1


def test_nested_product_row_hashes_are_repaired_after_enrichment():
    attrs = [
        {'AttributeId': 799, 'ParentAttributeId': 836, 'MainAttributeId': 162, 'RowI': 0, 'hash': None},
        {'AttributeId': 800, 'ParentAttributeId': 836, 'MainAttributeId': 162, 'RowI': 0, 'hash': 'existing-row'},
        {'AttributeId': 801, 'ParentAttributeId': 836, 'MainAttributeId': 162, 'RowI': 1, 'hash': None},
    ]
    products = [{'Id': 10, 'dataVersions': [{'VersionId': 20, 'productAttributes': attrs}]}]

    normalize_nested_product_attribute_hashes(products)

    assert attrs[0]['hash'] == attrs[1]['hash'] == 'existing-row'
    assert attrs[2]['hash'] != 'existing-row'
