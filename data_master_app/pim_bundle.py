"""Portable, offline-validated catalog and attachment transfer contract."""
import hashlib
import io
import json
import shutil
from pathlib import Path, PurePosixPath
from uuid import UUID, uuid4
from zipfile import ZipFile, ZIP_DEFLATED

FORMAT = 'pim-transfer.v1'
MAX_BYTES = 512 * 1024 * 1024
DATA_FILES = {
    'products.json', 'productsAttributes.json', 'productsModels.json',
    'building_elements.json', 'buildingsElementsAttributes.json', 'buildingsElementsModels.json',
    'colors.json', 'colorParameters.json', 'colorGroups.json', 'colorGroupParameters.json',
}
MODULES = {
    'products': ('products.json', 'products', 'productsAttributes.json'),
    'buildingelements': ('building_elements.json', 'buildingElements', 'buildingsElementsAttributes.json'),
    'colors': ('colors.json', 'colors', None),
    'colorgroups': ('colorGroups.json', 'colorGroups', None),
}
TYPES = {'.pdf': 'application/pdf', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
         '.png': 'image/png', '.gif': 'image/gif', '.bmp': 'image/bmp', '.tiff': 'image/tiff'}
PARAMETERS = {'colors': {'MainTexture', 'Thumbnail', 'base_color_map', 'normal_map',
                         'displacement_map', 'opacity_map', 'roughness_map'}, 'colorgroups': {'Cover'}}


def safe_path(value):
    if not isinstance(value, str) or not value or '\\' in value or ':' in value:
        raise ValueError('Invalid package path')
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in ('', '.', '..') for part in value.split('/')):
        raise ValueError('Unsafe package path')
    return value


def digest(data):
    return hashlib.sha256(data).hexdigest()


def items(data, key):
    result = data if isinstance(data, list) else data.get(key, [])
    if not isinstance(result, list):
        raise ValueError(f'Expected list: {key}')
    return result


def positive(value):
    if type(value) is not int or value < 1:
        raise ValueError('Owner, attribute and version IDs must be positive integers')
    return value


def check_file(name, data):
    ext = PurePosixPath(name).suffix.lower()
    if ext not in TYPES:
        raise ValueError(f'Unsupported attachment extension: {ext}')
    signatures = {'.pdf': b'%PDF-', '.png': b'\x89PNG\r\n\x1a\n', '.jpg': b'\xff\xd8\xff',
                  '.jpeg': b'\xff\xd8\xff', '.gif': b'GIF8', '.bmp': b'BM'}
    if ext in signatures and not data.startswith(signatures[ext]):
        raise ValueError(f'Attachment content does not match its extension: {name}')
    if ext == '.tiff' and not data.startswith((b'II*\x00', b'MM\x00*')):
        raise ValueError('Invalid TIFF signature')
    return TYPES[ext]


def validate_links(documents, links):
    def portable(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key.lower() == 'databaseid' and child not in (None, ''):
                    raise ValueError('Transfer data must not contain a tenant DatabaseId')
                portable(child)
        elif isinstance(value, list):
            for child in value:
                portable(child)
    portable(documents)
    seen = set()
    for link in links:
        module = link['module']
        if module not in MODULES:
            raise ValueError(f'Unsupported module: {module}')
        filename, root_key, attr_file = MODULES[module]
        owner_id, version_id = positive(link['owner_id']), positive(link['version_id'])
        owners = [obj for obj in items(documents.get(filename, {}), root_key) if obj.get('Id') == owner_id]
        if len(owners) != 1:
            raise ValueError(f'Missing or ambiguous owner: {module}/{owner_id}')
        versions = [v for v in owners[0].get('dataVersions', []) if v.get('VersionId') == version_id]
        if len(versions) != 1:
            raise ValueError(f'Missing or ambiguous version: {module}/{owner_id}/{version_id}')
        if attr_file:
            attribute_id = positive(link['attribute_id'])
            attrs = items(documents.get(attr_file, {}), 'attributes')
            attributes = [a for a in attrs if a.get('Id') == attribute_id and a.get('AttributeType') == 'Files' and not a.get('deleted') and not a.get('toDelete')]
            if len(attributes) != 1:
                raise ValueError(f'Missing Files attribute definition: {attribute_id}')
            if link.get('parent_hash'):
                positive(link.get('parent_attribute_id'))
                positive(link.get('row_i'))
                positive(link.get('main_attribute_id'))
                parents = [a for a in attrs if a.get('Id') == link['parent_attribute_id']]
                if len(parents) != 1 or parents[0].get('TargetModelId') != attributes[0].get('ProductModelId'):
                    raise ValueError('File attribute does not belong to its nested model')
                if not any(a.get('hash') == link['parent_hash'] and a.get('RowI') == link['row_i'] for a in versions[0].get('productAttributes', [])):
                    raise ValueError('Missing nested document row for attachment')
            elif attributes[0].get('ProductModelId') != owners[0].get('ModelType'):
                raise ValueError('Nested attachment needs parent_hash and row metadata')
            elif any(link.get(k) for k in ('parent_attribute_id', 'main_attribute_id', 'row_i')):
                raise ValueError('Incomplete nested file metadata')
        elif link.get('parameter_name') not in PARAMETERS[module]:
            raise ValueError('Unsupported file parameter')
        identity = (module, owner_id, version_id, link.get('attribute_id'), link.get('parameter_name'),
                    link.get('parent_hash'), link.get('row_i'), link.get('order', 0))
        if identity in seen:
            raise ValueError('Duplicate file slot; use distinct order values for multiple files')
        seen.add(identity)
        if type(link.get('order', 0)) is not int or link.get('order', 0) < 0:
            raise ValueError('File order must be a non-negative integer')


def build_bundle(data_files, attachments, links):
    if not data_files or set(data_files) - DATA_FILES:
        raise ValueError('Use canonical PIM JSON filenames only')
    documents = {name: json.loads(content.decode('utf-8-sig')) for name, content in data_files.items()}
    normalized, assets = [], {}
    allowed = {'file', 'module', 'owner_id', 'version_id', 'attribute_id', 'parameter_name',
               'parent_hash', 'parent_attribute_id', 'main_attribute_id', 'row_i', 'order', 'display_name'}
    for source in links:
        if set(source) - allowed:
            raise ValueError('Unknown file link fields')
        name = safe_path(source['file'])
        if name not in attachments:
            raise ValueError(f'Missing attachment: {name}')
        content = attachments[name]
        mime = check_file(name, content)
        asset = f'assets/{digest(content)}{PurePosixPath(name).suffix.lower()}'
        assets[asset] = content
        normalized.append({**{k: v for k, v in source.items() if k != 'file'}, 'asset': asset,
                           'original_name': PurePosixPath(name).name, 'content_type': mime,
                           'sha256': digest(content), 'size': len(content)})
    validate_links(documents, normalized)
    members = {**{f'data/{name}': value for name, value in data_files.items()}, **assets}
    members['file-links.json'] = json.dumps(normalized, ensure_ascii=False).encode()
    manifest = {'format': FORMAT, 'package_id': str(uuid4()), 'members': {
        name: {'sha256': digest(content), 'size': len(content)} for name, content in members.items()}}
    members['manifest.json'] = json.dumps(manifest).encode()
    if sum(map(len, members.values())) > MAX_BYTES:
        raise ValueError('Package exceeds size limit')
    stream = io.BytesIO()
    with ZipFile(stream, 'w', ZIP_DEFLATED) as archive:
        for name, content in members.items():
            archive.writestr(name, content)
    return stream.getvalue()


def product_file_links_from_documents(documents):
    products = items(documents.get('products.json', {}), 'products')
    links = []
    for product in products:
        owner_id = product.get('Id')
        for version in product.get('dataVersions', []) or []:
            version_id = version.get('VersionId', 1)
            for order, file_attr in enumerate(version.get('filesAttributes', []) or []):
                source_path = file_attr.get('sourcePath') or ''
                if not source_path:
                    continue
                link = {
                    'file': safe_path(source_path),
                    'module': 'products',
                    'owner_id': owner_id,
                    'version_id': version_id,
                    'attribute_id': file_attr.get('AttributeId'),
                    'parent_hash': file_attr.get('parentHash') or '',
                    'parent_attribute_id': file_attr.get('ParentAttributeId') or 0,
                    'main_attribute_id': file_attr.get('MainAttributeId'),
                    'row_i': file_attr.get('RowI') or 0,
                    'order': file_attr.get('OrderDisplayOrder', order),
                    'display_name': file_attr.get('uploadedfileName') or PurePosixPath(source_path).name,
                }
                if not link['parent_hash']:
                    link = {k: v for k, v in link.items() if k not in {'parent_hash', 'parent_attribute_id', 'main_attribute_id', 'row_i'}}
                links.append(link)
    return links


def build_transfer_folder(data_files, source_root, output_dir, links=None):
    if output_dir.exists():
        raise ValueError('Output directory already exists; choose a new folder')
    if not data_files or set(data_files) - DATA_FILES:
        raise ValueError('Use canonical PIM JSON filenames only')
    documents = {name: json.loads(content.decode('utf-8-sig')) for name, content in data_files.items()}
    links = links if links is not None else product_file_links_from_documents(documents)
    normalized = []
    source_root = Path(source_root).resolve()
    output_dir.mkdir(parents=True)
    try:
        for name, content in data_files.items():
            target = output_dir / 'data' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        asset_members = {}
        for source in links:
            allowed = {'file', 'module', 'owner_id', 'version_id', 'attribute_id', 'parameter_name',
                       'parent_hash', 'parent_attribute_id', 'main_attribute_id', 'row_i', 'order', 'display_name'}
            if set(source) - allowed:
                raise ValueError('Unknown file link fields')
            relative = safe_path(source['file'])
            source_path = (source_root / Path(*PurePosixPath(relative).parts)).resolve()
            if not source_path.is_relative_to(source_root) or not source_path.is_file():
                raise ValueError(f'Attachment must exist within the selected root: {relative}')
            size = source_path.stat().st_size
            name_digest = hashlib.sha256(f'{relative}:{size}'.encode('utf-8')).hexdigest()
            asset = f'assets/{name_digest}{PurePosixPath(relative).suffix.lower()}'
            target = output_dir / PurePosixPath(asset)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target)
            with source_path.open('rb') as stream:
                sha256 = digest_stream(stream)
            with target.open('rb') as stream:
                header = stream.read(16)
            mime = check_file(relative, header)
            asset_members[asset] = {'sha256': sha256, 'size': size}
            normalized.append({**{k: v for k, v in source.items() if k != 'file'}, 'asset': asset,
                               'original_name': PurePosixPath(relative).name, 'content_type': mime,
                               'sha256': sha256, 'size': size})
        validate_links(documents, normalized)
        file_links = json.dumps(normalized, ensure_ascii=False).encode()
        (output_dir / 'file-links.json').write_bytes(file_links)
        members = {**{f'data/{name}': {'sha256': digest(content), 'size': len(content)}
                     for name, content in data_files.items()},
                   **asset_members,
                   'file-links.json': {'sha256': digest(file_links), 'size': len(file_links)}}
        manifest = {'format': FORMAT, 'package_id': str(uuid4()), 'members': members}
        (output_dir / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    except Exception:
        shutil.rmtree(output_dir, ignore_errors=True)
        raise
    return {'data_files': sorted(data_files), 'assets': len(normalized), 'links': len(normalized)}


def digest_stream(stream):
    sha = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1024 * 1024), b''):
        sha.update(chunk)
    return sha.hexdigest()


def read_bundle(content):
    if len(content) > MAX_BYTES:
        raise ValueError('Archive exceeds size limit')
    with ZipFile(io.BytesIO(content)) as archive:
        infos = archive.infolist()
        names = [safe_path(info.filename) for info in infos]
        if len(names) > 10000 or len(set(names)) != len(names) or sum(i.file_size for i in infos) > MAX_BYTES:
            raise ValueError('Archive duplicate entries or size limit exceeded')
        members = {name: archive.read(name) for name in names}
    manifest = json.loads(members.pop('manifest.json'))
    if manifest.get('format') != FORMAT:
        raise ValueError('Unsupported transfer format')
    UUID(manifest['package_id'])
    if set(members) != set(manifest['members']):
        raise ValueError('Archive manifest mismatch')
    for name, payload in members.items():
        if manifest['members'][name] != {'sha256': digest(payload), 'size': len(payload)}:
            raise ValueError(f'Checksum mismatch: {name}')
        if name != 'file-links.json' and not name.startswith('assets/') and name not in {f'data/{n}' for n in DATA_FILES}:
            raise ValueError('Unexpected bundle entry')
    documents = {name[5:]: json.loads(payload.decode('utf-8-sig')) for name, payload in members.items() if name.startswith('data/')}
    links = json.loads(members['file-links.json'])
    for link in links:
        asset = safe_path(link['asset'])
        if not asset.startswith('assets/') or asset not in members:
            raise ValueError('Missing package attachment')
        if '/' in link['original_name'] or '\\' in link['original_name']:
            raise ValueError('Original name must not contain a path')
        payload = members[asset]
        if link['sha256'] != digest(payload) or link['size'] != len(payload) or link['content_type'] != check_file(link['original_name'], payload):
            raise ValueError('Attachment metadata mismatch')
    validate_links(documents, links)
    return manifest, members, documents, links
