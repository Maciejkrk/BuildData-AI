# Architecture

## Boundary

BuildData AI is a mapper, not a model authoring tool.

PIM/database remains the source of truth for:

- model IDs,
- attribute IDs,
- nested relations,
- field types,
- dictionary options,
- required flags,
- product reference semantics.

The studio imports existing model exports and uses them as a contract. If a
field, dictionary option, or nested relation is missing from the export, the
studio must not invent it. The missing structure has to be added in PIM first
and then re-exported.

## Workflows

### Products

```text
existing product model export
  -> customer product file
  -> mapping profile
  -> product/type-series preview
  -> products.json
```

The product workflow is the required foundation for building elements because
building-element layers refer to existing products.

### Building Elements

```text
existing building-element model export
  -> completed products.json reference
  -> customer building-element file
  -> mapping profile
  -> tree preview + product resolution report
  -> building_elements.json
```

Nested building-element relations are read dynamically through `TargetModelId`.
For the current sample export this creates:

```text
Building Element Model no. 1
  Variants
    Layers
      Available products
        Product
```

The IDs are not treated as permanent application constants. They are read from
the uploaded model and attribute files.

## Modules

```text
mapping_studio/
  main.py                         FastAPI endpoints
  web.py                          simple studio UI
  models.py                       shared domain objects
  services/
    pim_model_loader.py           reads existing PIM model exports
    source_reader.py              reads xlsx/json/csv/tsv customer files
    mapping_analyzer.py           suggests mappings and exposes target fields
    product_reference.py          indexes completed products.json
    building_preview.py           builds initial building-element tree preview

data_master_app/
  canonical_model.py              migrated product canonical model
  mapping_model.py                migrated mapping/enrichment profile model
  mapping.py                      migrated product/PIM mapping logic
  converter.py                    migrated product conversion and enrichment
  main.py                         legacy product app endpoints
  web_ui.py                       legacy product UI reference
```

The new `/api/products/analyze` and `/api/products/convert` endpoints in
`mapping_studio.main` call the migrated product converter. That keeps product
behavior regression-tested while the new UI is cleaned up incrementally.

## Next Implementation Steps

1. Split the migrated product workflow into `mapping_engine`,
   `product_builder`, and `pim_exporter` services behind the studio API.
2. Replace the legacy product UI with focused studio screens while keeping the
   regression tests green.
3. Add project save/load as a single JSON mapping project.
4. Add full building-element export that preserves nested hashes and parent
   relations from the loaded model.
5. Add manual product resolution UI for unresolved layer products.
