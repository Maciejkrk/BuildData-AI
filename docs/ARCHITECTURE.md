# Architecture

## Boundary

BuildData AI Mapping Studio is a mapper, not a model authoring tool.

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
```

## Next Implementation Steps

1. Split the product workflow into `mapping_engine`, `product_builder`, and
   `pim_exporter` services.
2. Port the proven product tests from the previous prototype, minus UI history.
3. Add project save/load as a single JSON mapping project.
4. Add full building-element export that preserves nested hashes and parent
   relations from the loaded model.
5. Add manual product resolution UI for unresolved layer products.

