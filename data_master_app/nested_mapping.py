"""Model-driven joins between product rows and repeatable child records."""


from .mapping import (
    load_json_content, pim_bundle_file_key, pim_items, is_deleted,
    int_value, pim_field_definition, is_nested_attribute, is_type_series_parent,
    apply_cleanup, normalize_choice_mapping, choice_value_parts,
)


def nested_models(files, root_model_id=None):
    bundle = {pim_bundle_file_key(name): load_json_content(value) for name, value in (files or {}).items() if pim_bundle_file_key(name) in {'productsmodels', 'productsattributes'}}
    models = pim_items(bundle.get('productsmodels'), 'models')
    attrs = [a for a in pim_items(bundle.get('productsattributes'), 'attributes') if not is_deleted(a)]
    roots = {int_value(root_model_id)} if root_model_id else {int_value(m.get('Id')) for m in models if m.get('modelType') == 'Product'}
    by_id = {int_value(m.get('Id')): m for m in models}
    result = []
    for parent in attrs:
        if int_value(parent.get('ProductModelId')) not in roots or parent.get('AttributeType') not in {'Model', 'Model_Array', 'Table_Model'}:
            continue
        target = int_value(parent.get('TargetModelId'))
        children = [a for a in attrs if int_value(a.get('ProductModelId')) == target]
        label = parent.get('DispName') or parent.get('AttributeName') or str(parent['Id'])
        fields = []
        for child in children:
            if is_nested_attribute(child):
                continue
            field = pim_field_definition(child, label, parent_attribute=parent, parent_model=by_id.get(target), parent_is_type_series=is_type_series_parent(parent, by_id.get(target), children))
            if field:
                fields.append({'attribute_id': child['Id'], 'attribute_type': child.get('AttributeType'), 'label': field.label, 'path': field.key, 'value_kind': field.value_kind, 'options': list(field.options), 'unit': field.unit})
        result.append({'parent_attribute_id': parent['Id'], 'model_id': target, 'label': label, 'multiple': parent.get('AttributeType') != 'Model', 'type_series': is_type_series_parent(parent, by_id.get(target), children), 'fields': fields, 'available': target in by_id and bool(fields)})
    return result


def join_key(value):
    if value is None:
        return ''
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def compile_relations(tables, definitions, profile, product_columns):
    """Validate once and index each child table once, before mapping products."""
    result = {}
    definitions = {str(d['parent_attribute_id']): d for d in definitions}
    by_name = {table.name: table for table in tables}
    for parent, config in (profile.get('_nested_relations') or {}).items():
        if not config.get('enabled'):
            continue
        config = dict(config)
        if config.get('use_primary_key'):
            config['product_key'] = profile.get('_product_key')
            if not config['product_key']:
                raise ValueError('Choose the primary product identifier before linking another file.')
        definition = definitions.get(str(parent))
        if not definition or not definition['available']:
            raise ValueError(f'Incomplete nested model: {parent}')
        if config.get('source_mode') == 'external':
            table = next((table for table in (config.get('source') or {}).get('tables', []) if table.get('name') == config.get('table')), None)
            if table is None:
                raise ValueError(f"Missing child table: {config.get('table')}")
            rows = table.get('sample_rows') or []
            columns = set(table.get('columns') or [])
        else:
            table = by_name.get(config.get('table'))
            if table is None:
                raise ValueError(f"Missing child table: {config.get('table')}")
            rows = table.rows
            columns = {column for row in rows for column in row}
        if config.get('product_key') not in product_columns or config.get('child_key') not in columns:
            raise ValueError(f"Choose both join columns for {definition['label']}.")
        fields = {str(f['attribute_id']): f for f in definition['fields']}
        bindings = config.get('fields') or {}
        selected = {key: column for key, column in bindings.items() if column}
        if (config.get('source') or {}).get('kind') == 'documents':
            file_fields = [key for key, field in fields.items() if field.get('attribute_type') == 'Files']
            if len(file_fields) == 1:
                selected[file_fields[0]] = 'Sciezka pliku'
        if not selected or any(str(key) not in fields or column not in columns for key, column in selected.items()):
            raise ValueError(f"Invalid field mapping for {definition['label']}.")
        index = {}
        record_keys = {}
        record_column = config.get('record_key')
        if record_column and record_column not in columns:
            raise ValueError(f"Missing record key column: {record_column}")
        for row in rows:
            key = join_key(row.get(config['child_key']))
            if not key:
                continue
            values = {}
            for attribute_id, column in selected.items():
                field = fields[str(attribute_id)]
                value = apply_cleanup(row.get(column), {'trim': True})
                if field['options']:
                    choice_map = (config.get('choice_maps') or {}).get(str(attribute_id), {})
                    if (config.get('source') or {}).get('kind') == 'documents' and value not in (None, '', []):
                        for part in choice_value_parts(value, multi=field['value_kind'] == 'multi_choice'):
                            if not normalize_choice_mapping(part, 'single_choice', field['options'], choice_map):
                                raise ValueError(f"Unrecognized model dictionary value for {field['label']}: {part}. Assign it to a model option before export.")
                    value = normalize_choice_mapping(value, field['value_kind'], field['options'], choice_map)
                if value not in (None, '', []):
                    values[int(attribute_id)] = value
            if values:
                record_key = join_key(row.get(record_column)) if record_column else ''
                if record_column and not record_key:
                    raise ValueError(f"Empty record key for {definition['label']}: {key}")
                if record_key:
                    identity = (key, record_key)
                    if identity in record_keys:
                        if record_keys[identity] != values:
                            raise ValueError(f"Conflicting record key for {definition['label']}: {key} / {record_key}")
                        continue
                    record_keys[identity] = values
                if not definition.get('multiple', True) and key in index:
                    if index[key][0] == values:
                        continue
                    raise ValueError(f"Multiple objects for single model {definition['label']}: {key}")
                index.setdefault(key, []).append(values)
        result[str(parent)] = {'definition': definition, 'config': config, 'index': index}
    return result
