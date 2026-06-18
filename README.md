# BuildData AI Mapping Studio

Local studio for mapping customer data into existing BuildData/PIM export
structures.

The studio does not create PIM models. Product and building-element models are
generated in the existing database/PIM and imported here as JSON model exports.
This tool only reads those models, exposes valid target fields, validates
dictionary values, builds previews, and exports mapped payloads.

## Workflows

1. Products
   - Load existing `productsModels.json` and `productsAttributes.json`.
   - Load a customer product file.
   - Map columns to fields from the accepted product model.
   - Review product and type-series preview.
   - Export `products.json`.
   - Save/load a mapping project.

2. Building elements
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

## Local Run

### Docker

```powershell
docker compose up --build -d
```

Open:

```text
http://localhost:8010
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
uvicorn mapping_studio.main:app --host 127.0.0.1 --port 8010
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

The application listens on port `8010`. If the server firewall allows access,
open it from another computer with:

```text
http://SERVER_IP:8010
```

## Initial Scope

This repository starts with a modular FastAPI backend and a simple studio UI.
The product workflow reuses proven ideas from the previous prototype, while the
building-element workflow reads nested model relations dynamically from the
model export:

```text
Building Element -> Variants -> Layers -> Available Products -> Product
```

The relation names and IDs come from the loaded model files, not from hardcoded
prototype constants.
