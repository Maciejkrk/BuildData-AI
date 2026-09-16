import asyncio
import io
import json
from pathlib import Path
import sys
from zipfile import ZipFile, ZIP_DEFLATED

import pytest
from fastapi import UploadFile

from data_master_app.pim_bundle import build_bundle, read_bundle, safe_path
from data_master_app.main import transfer_package


def fixture():
    data = {
        'products.json': {'products': [{'Id': 101, 'ModelType': 5, 'dataVersions': [{'VersionId': 1, 'productAttributes': []}]}]},
        'productsModels.json': {'models': [{'Id': 5, 'modelType': 'Product'}]},
        'productsAttributes.json': {'attributes': [{'Id': 17, 'ProductModelId': 5, 'AttributeType': 'Files'}]},
    }
    data = {name: json.dumps(value).encode() for name, value in data.items()}
    attachments = {'manual.pdf': b'%PDF-1.4\nfixture'}
    links = [{'file': 'manual.pdf', 'module': 'products', 'owner_id': 101, 'version_id': 1, 'attribute_id': 17}]
    return data, attachments, links


def test_package_roundtrip_and_shared_importer_contract():
    package = build_bundle(*fixture())
    manifest, members, documents, links = read_bundle(package)
    assert manifest['format'] == 'pim-transfer.v1'
    assert len(links) == 1
    assert members[links[0]['asset']] == b'%PDF-1.4\nfixture'
    assert documents['products.json']['products'][0]['Id'] == 101
    root = Path(__file__).parents[2]
    assert (root / 'PIM-Data-Importer-next/pim_importer/pim_bundle.py').read_bytes() == (root / 'BuildData-AI/data_master_app/pim_bundle.py').read_bytes()


@pytest.mark.parametrize('path', ['../a.pdf', '/a.pdf', 'C:/a.pdf', 'a\\b.pdf', 'a/../b.pdf', 'a//b.pdf'])
def test_unsafe_paths_rejected(path):
    with pytest.raises(ValueError):
        safe_path(path)


@pytest.mark.parametrize('field,value', [('owner_id', 999), ('version_id', 2), ('attribute_id', 99), ('module', 'unknown')])
def test_unresolved_file_links_rejected(field, value):
    data, attachments, links = fixture()
    links[0][field] = value
    with pytest.raises(ValueError):
        build_bundle(data, attachments, links)


def test_missing_attachment_and_fake_pdf_rejected():
    data, attachments, links = fixture()
    with pytest.raises(ValueError, match='Missing attachment'):
        build_bundle(data, {}, links)
    with pytest.raises(ValueError, match='content does not match'):
        build_bundle(data, {'manual.pdf': b'MZ executable'}, links)


def test_corruption_is_detected():
    package = build_bundle(*fixture())
    target = io.BytesIO()
    with ZipFile(io.BytesIO(package)) as source, ZipFile(target, 'w', ZIP_DEFLATED) as output:
        for name in source.namelist():
            output.writestr(name, b'bad' if name.startswith('assets/') else source.read(name))
    with pytest.raises(ValueError, match='Checksum mismatch'):
        read_bundle(target.getvalue())


def test_portable_package_rejects_embedded_tenant():
    data, assets, links = fixture()
    payload = json.loads(data['products.json'])
    payload['products'][0]['DatabaseId'] = 'other-tenant'
    data['products.json'] = json.dumps(payload).encode()
    with pytest.raises(ValueError, match='tenant'):
        build_bundle(data, assets, links)


def test_nested_file_preserves_row_link():
    data, assets, links = fixture()
    payload = json.loads(data['products.json'])
    payload['products'][0]['dataVersions'][0]['productAttributes'] = [{'hash': 'row-A', 'RowI': 1, 'ParentAttributeId': 20}]
    data['products.json'] = json.dumps(payload).encode()
    data['productsAttributes.json'] = json.dumps({'attributes': [
        {'Id': 17, 'ProductModelId': 6, 'AttributeType': 'Files'},
        {'Id': 20, 'ProductModelId': 5, 'AttributeType': 'Model_Array', 'TargetModelId': 6}]}).encode()
    links[0].update(parent_hash='row-A', row_i=1, parent_attribute_id=20, main_attribute_id=6)
    assert read_bundle(build_bundle(data, assets, links))[3][0]['parent_hash'] == 'row-A'
    links[0]['parent_hash'] = 'wrong'
    with pytest.raises(ValueError, match='Missing nested'):
        build_bundle(data, assets, links)


def test_web_package_endpoint():
    data, assets, links = fixture()
    upload = lambda name, content: UploadFile(io.BytesIO(content), filename=name)
    response = asyncio.run(transfer_package(
        data_files=[upload(name, content) for name, content in data.items()],
        links_file=upload('links.json', json.dumps(links).encode()),
        attachments=[upload(name, content) for name, content in assets.items()]))
    assert response.media_type == 'application/zip'
    assert len(read_bundle(response.body)[3]) == 1


def test_file_import_is_explicit_and_can_resume_after_sql_failure(tmp_path, monkeypatch):
    sys.path.insert(0, str(Path(__file__).parents[2] / 'PIM-Data-Importer-next'))
    from pim_importer import transfer
    from pim_importer.config import AppConfig
    config = AppConfig('', '', 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee')
    bundle = tmp_path / 'bundle.zip'
    bundle.write_bytes(build_bundle(*fixture()))
    journal = tmp_path / 'journal.json'
    with pytest.raises(PermissionError):
        transfer.transfer_files(config, bundle, journal)
    link = read_bundle(bundle.read_bytes())[3][0]
    monkeypatch.setattr(transfer, 'preflight', lambda *args: [(link, '[dbo].[Files]', transfer.file_row(config.database_id, link, '', True))])
    for name, value in {'PIM_AZURE_URL': 'https://example.blob.core.windows.net', 'PIM_AZURE_CONTAINER': 'files',
                        'Storage__AzureBlobStorage__AzureConnectionString': 'test-secret'}.items():
        monkeypatch.setenv(name, value)
    class Service:
        url = 'https://example.blob.core.windows.net'
        def get_container_client(self, name): return self
        def get_container_properties(self): return {}
        def close(self): pass
    uploads = set()
    def blob(container, name, content, content_type):
        uploads.add(name)
        return f'https://example.blob.core.windows.net/files/{name}'
    monkeypatch.setattr(transfer, 'ensure_blob', blob)
    def fail(*args): raise RuntimeError('simulated SQL failure')
    monkeypatch.setattr(transfer, 'insert_metadata', fail)
    with pytest.raises(RuntimeError):
        transfer.transfer_files(config, bundle, journal, True, lambda value: Service())
    assert json.loads(journal.read_text())['files'][0]['status'] == 'sql_pending'
    assert 'test-secret' not in journal.read_text()
    monkeypatch.setattr(transfer, 'insert_metadata', lambda *args: None)
    transfer.transfer_files(config, bundle, journal, True, lambda value: Service())
    assert len(uploads) == 1
    assert json.loads(journal.read_text())['files'][0]['status'] == 'complete'
