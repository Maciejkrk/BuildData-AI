import json
import pytest
import shutil
import subprocess
from pathlib import Path
from data_master_app.document_source import directory_table
from data_master_app.converter import convert_products_file
from test_nested_relations import bundle, profile


def test_document_dictionary_requires_known_value_or_explicit_model_mapping():
    from data_master_app.nested_mapping import compile_relations
    table = directory_table(['P1/Deklaracje/a.pdf'])
    definitions = [{'parent_attribute_id': 1, 'available': True, 'label': 'Documents', 'multiple': True,
                    'fields': [{'attribute_id': 2, 'label': 'Type', 'value_kind': 'single_choice',
                                'options': [{'id': 11, 'label': 'Declaration', 'value': 'Declaration'}]}]}]
    config = {'enabled': True, 'source_mode': 'external', 'source': {'kind': 'documents', 'tables': [table]},
              'table': table['name'], 'product_key': 'Name', 'child_key': 'Katalog 1',
              'fields': {'2': 'Katalog 2'}}
    profile = {'_nested_relations': {'1': config}}
    with pytest.raises(ValueError, match='Unrecognized model dictionary'):
        compile_relations([], definitions, profile, {'Name'})
    config['choice_maps'] = {'2': {'Deklaracje': 11}}
    result = compile_relations([], definitions, profile, {'Name'})
    assert result['1']['index']['P1'][0][2]['id'] == 11
    config['choice_maps'] = {'2': {'Deklaracje': 999}}
    with pytest.raises(ValueError, match='Unrecognized model dictionary'):
        compile_relations([], definitions, profile, {'Name'})


def test_directory_change_refreshes_fields_before_collecting_mapping():
    from data_master_app.products_ui import render_home
    node = shutil.which('node')
    if not node:
        pytest.skip('Node.js is needed for the UI event regression test')
    result = subprocess.run([node, str(Path(__file__).with_name('document_directory_event.cjs'))],
                            input=render_home(), text=True, encoding='utf-8', capture_output=True)
    assert result.returncode == 0, result.stderr


def test_directory_levels_and_missing_optional_level():
    table = directory_table(['P1/Karty/pl/a.pdf', 'P2/b.pdf'])
    assert table['sample_rows'][0]['Katalog 3'] == 'pl'
    assert 'Katalog 2' not in table['sample_rows'][1]
    assert table['sample_rows'][0]['Nazwa bez rozszerzenia'] == 'a'


@pytest.mark.parametrize('paths', [['../x.pdf'], ['A/x.pdf', 'A/x.pdf'], ['C:/x.pdf']])
def test_bad_directory_paths(paths):
    with pytest.raises(ValueError):
        directory_table(paths)


def test_project_directory_source_exports_one_products_json_with_document_records(tmp_path):
    model = bundle()
    attrs = json.loads(model['productsAttributes.json'])
    attrs['attributes'].append({'Id': 5104, 'ProductModelId': 5020, 'DispName': 'File', 'AttributeType': 'Files'})
    model['productsAttributes.json'] = json.dumps(attrs)
    table = directory_table(['P1/Karty/pl/a.pdf', 'P1/Karty/en/b.pdf'])
    mapping = profile()
    mapping['_product_key'] = 'Key'
    mapping['_nested_relations']['5101'].update(source_mode='external', source={'kind': 'documents', 'filename': 'Docs', 'tables': [table]},
        table=table['name'], child_key='Katalog 1', record_key='Sciezka pliku',
        fields={'5102': 'Nazwa bez rozszerzenia', '5103': ''})
    mapping = json.loads(json.dumps(mapping))
    source = json.dumps({'Products': [{'Name': 'Product A', 'Key': 'P1'}]}).encode()
    result = convert_products_file('source.json', source, tmp_path, product_model_files=model, product_mapping_profile=mapping)
    payload = json.loads((tmp_path / result['job_id'] / 'products.json').read_text(encoding='utf-8'))
    version = payload['products'][0]['dataVersions'][0]
    docs = [a for a in version['productAttributes'] if a['ParentAttributeId'] == 5101]
    assert len(docs) == 2
    assert {a['AttributeId'] for a in docs} == {5102}
    assert len(version['filesAttributes']) == 2
    assert {a['sourcePath'] for a in version['filesAttributes']} == {'P1/Karty/pl/a.pdf', 'P1/Karty/en/b.pdf'}
    assert {a['parentHash'] for a in version['filesAttributes']} == {a['hash'] for a in docs}
    assert all(a['fileUrl'] is None for a in version['filesAttributes'])
