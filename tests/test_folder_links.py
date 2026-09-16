import pytest
from data_master_app.folder_links import scan_folders, folder_options


def docs(module='products'):
    root = 'products' if module == 'products' else 'buildingElements'
    filename = 'products.json' if module == 'products' else 'building_elements.json'
    attr = 'productsAttributes.json' if module == 'products' else 'buildingsElementsAttributes.json'
    return {filename: {root: [{'Id': 101, 'Name': 'PROD-A', 'ModelType': 5,
                               'dataVersions': [{'VersionId': 1, 'Code': '001'}]}]},
            attr: {'attributes': [{'Id': 17, 'AttributeType': 'Files', 'ProductModelId': 5}]}}


@pytest.mark.parametrize('module', ['products', 'buildingelements'])
def test_deep_tree_and_document_type(module):
    result = scan_folders(docs(module), ['Brand/prod-a/Karty/PL/manual.pdf'],
                          'product.Name', 1, 17, module, 2, [{'folder': 'Karty', 'attribute_id': 17}])
    assert result['matched'] == 1
    assert result['links'][0]['module'] == module
    assert result['rows'][0]['document_type'] == 'Karty/PL'
    assert result['rows'][0]['name'] == 'manual.pdf'


def test_ambiguous_missing_unsupported_and_outside():
    documents = docs()
    documents['products.json']['products'].append({**documents['products.json']['products'][0], 'Id': 102})
    result = scan_folders(documents, ['PROD-A/a.pdf', 'missing/b.pdf', 'loose.pdf', 'PROD-A/a.exe'], 'product.Name', 1, 17)
    assert result['matched'] == 0
    assert result['unresolved'] == 4


def test_version_key_and_rule_gaps():
    result = scan_folders(docs(), ['001/Karty/a.pdf', '001/Other/a.pdf', '001/Karty/b.pdf'],
                          'version.Code', 1, 17, rules=[{'folder': 'Karty', 'attribute_id': 17}])
    assert result['matched'] == 2
    assert result['unresolved'] == 1
    assert [l['order'] for l in result['links']] == [0, 1]


def test_nested_files_require_explicit_row():
    documents = docs()
    documents['productsAttributes.json']['attributes'][0]['ProductModelId'] = 6
    assert scan_folders(documents, ['PROD-A/a.pdf'], 'product.Name', 1, 17)['unresolved'] == 1


def test_invalid_paths_and_duplicate_rules():
    with pytest.raises(ValueError):
        scan_folders(docs(), ['../a.pdf'], 'product.Name', 1, 17)
    with pytest.raises(ValueError):
        scan_folders(docs(), [], 'product.Name', 1, 17, rules=[{'folder': 'a', 'attribute_id': 17}, {'folder': 'A', 'attribute_id': 17}])
    assert 'version.Code' in folder_options(docs())['keys']
