# BuildData AI

Advanced local web tool for mapping customer product data into existing
BuildData/PIM product export structures.

The application does not create PIM models. Product models are generated in the
existing database/PIM and imported here as JSON model exports. The tool reads
those models, exposes valid target fields, validates dictionary values, builds
live previews, supports row rules for product/type-series files, enriches mapped
data, and exports `products.json`.

The interface is available in Polish and English. Use the language selector in
the top right corner of the application.

## Workflows

1. Products
   - Load existing `productsModels.json` and `productsAttributes.json`.
   - Load a customer product file.
   - Map columns to fields from the accepted product model.
   - Review product and type-series preview.
   - Export `products.json`.
   - Save/load a mapping project.

2. Building elements, next tool scope
   - Load existing `buildingsElementsModels.json` and
     `buildingsElementsAttributes.json`.
   - Load a completed product reference, usually `products.json`.
   - Load customer building-element/system data.
   - Map system, variant, layer, and layer-product fields.
   - Resolve products against the product reference.
   - Review tree preview and quality report.
   - Export `building_elements.json`.

Building-element mapping is intentionally gated by a product reference. The
studio can suggest product matches, but exported product relations must resolve
to existing products.

The current Docker entrypoint runs the advanced product mapper. Building-element
mapping is documented as the next tool scope and should reuse the same model
driven principles.

## Local Run

### Docker

```powershell
docker compose up --build -d
```

Open:

```text
http://localhost:8020
```

Stop:

```powershell
docker compose down
```

### Python

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn data_master_app.main:app --host 127.0.0.1 --port 8010
```

Open:

```text
http://127.0.0.1:8010
```

## Deployment on the Docker machine

```powershell
cd C:\projects
git clone https://github.com/Maciejkrk/BuildData-AI.git
cd BuildData-AI
docker compose up --build -d
```

The application listens on container port `8010` and is exposed by Docker on
host port `8020`. If the server firewall allows access,
open it from another computer with:

```text
http://SERVER_IP:8020
```

## Initial Scope

This repository contains two layers:

- `data_master_app/` - migrated product workflow from the previous
  `ai-data-master` prototype, including product mapping, type-series handling,
  enrichment, export and regression tests.
- `mapping_studio/` - the new studio shell where products and building elements
  will be professionalized into one mapper application.

The product workflow now reuses the proven prototype implementation through the
new studio API. The building-element workflow reads nested model relations
dynamically from the model export:

```text
Building Element -> Variants -> Layers -> Available Products -> Product
```

The relation names and IDs come from the loaded model files, not from hardcoded
prototype constants.

## Migrated Product Functionality

The previous product tool has been brought into this repository so that the next
work can build from the full tested behavior rather than from notes only.

Migrated areas:

- product canonical model,
- mapping profile model,
- PIM model field extraction,
- source readers for `.xlsx`, `.json`, `.csv` and `.tsv`,
- product mapping suggestions,
- type-series row rules,
- value cleanup and unit conversion helpers,
- dictionary value mapping,
- product enrichment from manual and typical-data sessions,
- `products.json` export,
- legacy FastAPI endpoints and server-rendered UI,
- regression tests from the previous project.

The old UI is kept as a working reference, not as the final studio interface.
