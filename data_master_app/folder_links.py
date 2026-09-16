"""Deterministic folder-to-product matching; never fuzzy-match identifiers."""
import unicodedata
import argparse
import json
from collections import defaultdict
from pathlib import Path, PurePosixPath

from .pim_bundle import MODULES, TYPES, items, safe_path, validate_links


def normalized(value):
    return unicodedata.normalize('NFC', str(value)).strip().casefold()


def scalar_fields(obj, prefix):
    return {prefix + key: value for key, value in obj.items()
            if isinstance(value, (str, int, float)) and not isinstance(value, bool)}


def folder_options(documents, module='products'):
    if module not in ('products', 'buildingelements'):
        raise ValueError('Nieobslugiwany rodzaj danych')
    filename, root_key, attr_file = MODULES[module]
    keys, versions = set(), set()
    for product in items(documents.get(filename, {}), root_key):
        keys.update(scalar_fields(product, 'product.'))
        for version in product.get('dataVersions', []):
            keys.update(scalar_fields(version, 'version.'))
            versions.add(version['VersionId'])
    attrs = [a for a in items(documents.get(attr_file, {}), 'attributes')
             if a.get('AttributeType') == 'Files' and not a.get('deleted') and not a.get('toDelete')]
    return {'keys': sorted(keys), 'versions': sorted(versions),
            'attributes': [{'id': a['Id'], 'name': a.get('Name') or a.get('name') or str(a['Id'])} for a in attrs]}


def scan_folders(documents, paths, key, version_id, attribute_id, module='products', owner_depth=1, rules=None):
    if key not in folder_options(documents, module)['keys']:
        raise ValueError('Wybierz pole identyfikujace produkt')
    if type(owner_depth) is not int or not 1 <= owner_depth <= 20:
        raise ValueError('Poziom katalogu musi wynosic od 1 do 20')
    routes = {}
    for rule in rules or []:
        folder_key = normalized(safe_path(rule['folder']))
        if folder_key in routes:
            raise ValueError('Powtorzona regula katalogu')
        routes[folder_key] = rule['attribute_id']
    if len(paths) > 10000 or len(set(paths)) != len(paths):
        raise ValueError('Za duzo plikow lub powtorzone sciezki')
    scope, field = key.split('.', 1)
    index = defaultdict(list)
    filename, root_key, _ = MODULES[module]
    for product in items(documents.get(filename, {}), root_key):
        versions = [v for v in product.get('dataVersions', []) if v.get('VersionId') == version_id]
        for version in versions:
            value = (product if scope == 'product' else version).get(field)
            if value is not None and normalized(value):
                index[normalized(value)].append(product)
    rows, links, orders = [], [], defaultdict(int)
    for name in sorted(paths):
        safe_path(name)
        path = PurePosixPath(name)
        folder = path.parts[owner_depth - 1] if len(path.parts) > owner_depth else ''
        subfolder = '/'.join(path.parts[owner_depth:-1])
        applicable = [r for r in routes if normalized(subfolder) == r or normalized(subfolder).startswith(r + '/')]
        route = max(applicable, key=len) if applicable else None
        target_attribute = routes[route] if route else attribute_id
        matches = index.get(normalized(folder), []) if folder else []
        row = {'file': name, 'name': path.name, 'folder': folder, 'document_type': subfolder,
               'attribute_id': target_attribute, 'status': '', 'owner_id': None}
        if path.suffix.lower() not in TYPES:
            row['status'] = 'Nieobslugiwany format'
        elif not folder:
            row['status'] = 'Plik poza katalogiem produktu'
        elif not matches:
            row['status'] = 'Brak produktu'
        elif len(matches) != 1:
            row['status'] = 'Niejednoznaczny identyfikator'
        elif routes and route is None:
            row['status'] = 'Brak reguly dla typu dokumentu'
        else:
            owner = matches[0]['Id']
            slot = (owner, target_attribute)
            link = {'file': name, 'module': module, 'owner_id': owner,
                    'version_id': version_id, 'attribute_id': target_attribute, 'order': orders[slot],
                    'display_name': path.stem}
            try:
                validate_links(documents, [link])
            except (ValueError, KeyError, TypeError) as exc:
                row['status'] = 'Niezgodny atrybut lub wymagany wiersz podmodelu: ' + str(exc)
            else:
                row.update(status='Dopasowano', owner_id=owner)
                links.append(link)
                orders[slot] += 1
        rows.append(row)
    return {'rows': rows, 'links': links, 'matched': len(links), 'unresolved': len(rows) - len(links)}


def main():
    parser = argparse.ArgumentParser(description='Scan attachment folders without copying their contents')
    parser.add_argument('--data', type=Path, required=True)
    parser.add_argument('--files', type=Path, required=True)
    parser.add_argument('--key', required=True)
    parser.add_argument('--module', choices=['products', 'buildingelements'], default='products')
    parser.add_argument('--version', type=int, required=True)
    parser.add_argument('--attribute', type=int, required=True)
    parser.add_argument('--owner-depth', type=int, default=1)
    parser.add_argument('--rules', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    from .pim_bundle import DATA_FILES
    root = args.files.resolve(strict=True)
    if not root.is_dir():
        parser.error('Source must be a directory')
    paths = []
    for file in root.rglob('*'):
        if file.is_file():
            if not file.resolve().is_relative_to(root):
                raise ValueError('File points outside the source directory')
            paths.append(file.relative_to(root).as_posix())
    documents = {n: json.loads((args.data / n).read_text(encoding='utf-8-sig'))
                 for n in DATA_FILES if (args.data / n).is_file()}
    rules = json.loads(args.rules.read_text(encoding='utf-8-sig')) if args.rules else []
    result = scan_folders(documents, paths, args.key, args.version, args.attribute,
                          args.module, args.owner_depth, rules)
    plan = {'format': 'pim-folder-plan.v1', 'source_root': str(root),
            'settings': {'module': args.module, 'key': args.key, 'version_id': args.version,
                         'attribute_id': args.attribute, 'owner_depth': args.owner_depth, 'rules': rules}, **result}
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(plan, stream, ensure_ascii=False, indent=2)
    print(f"Matched: {result['matched']}; unresolved: {result['unresolved']}; plan: {args.output}")


if __name__ == '__main__':
    main()
