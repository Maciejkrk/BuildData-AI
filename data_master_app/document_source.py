"""Directory metadata as a source table; no binary file access during mapping."""
from pathlib import PurePosixPath
from .pim_bundle import safe_path


def directory_table(paths):
    if not isinstance(paths, list) or len(paths) > 10000:
        raise ValueError('Select at most 10000 document paths')
    rows, seen, depth = [], set(), 0
    for value in sorted(paths):
        safe_path(value)
        if value in seen:
            raise ValueError('Duplicate document path')
        seen.add(value)
        path = PurePosixPath(value)
        folders = path.parts[:-1]
        depth = max(depth, len(folders))
        row = {'Sciezka pliku': value, 'Nazwa pliku': path.name,
               'Nazwa bez rozszerzenia': path.stem, 'Rozszerzenie': path.suffix.lower(),
               **{f'Katalog {i}': name for i, name in enumerate(folders, 1)}}
        rows.append(row)
    columns = ['Sciezka pliku', 'Nazwa pliku', 'Nazwa bez rozszerzenia', 'Rozszerzenie'] + [f'Katalog {i}' for i in range(1, depth + 1)]
    return {'name': 'Dokumenty zewnetrzne', 'columns': columns, 'sample_rows': rows, 'rows': len(rows)}
