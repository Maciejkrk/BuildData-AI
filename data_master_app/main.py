from __future__ import annotations

from pathlib import Path
from typing import Any
import base64
import hashlib
import json

from fastapi import Body, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse

from .converter import analyze_product_model_files, analyze_uploaded_file, convert_products_file
from .web_ui import render_building_elements_home, render_home
from mapping_studio.services.building_preview import preview_building_elements
from mapping_studio.services.mapping_analyzer import analyze_source_tables, bundle_payload
from mapping_studio.services.pim_model_loader import load_building_element_model, load_product_model
from mapping_studio.services.product_reference import build_product_reference_index
from mapping_studio.services.source_reader import read_source_tables


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"
PROJECTS_DIR = OUTPUT_DIR / "mapping-projects"
MODEL_SESSIONS_DIR = OUTPUT_DIR / "model-sessions"
SOURCE_SESSIONS_DIR = OUTPUT_DIR / "source-sessions"

app = FastAPI(title="BuildData AI", version="0.1.0")


@app.get("/", response_class=HTMLResponse)
def home(product_model_id: str | None = None) -> HTMLResponse:
    if product_model_id:
        try:
            model_files = load_product_model_session(product_model_id)
            result = analyze_product_model_files(model_files)
            result["model_id"] = product_model_id
            result["files"] = list(model_files)
            return html_response(render_home(result))
        except ValueError as exc:
            return html_response(render_home({"error": str(exc)}))
    return html_response(render_home())


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok"}


@app.get("/building-elements", response_class=HTMLResponse)
def building_elements_home() -> HTMLResponse:
    return html_response(render_building_elements_home())


@app.get("/elements")
def elements_redirect() -> RedirectResponse:
    return redirect_response("/building-elements")


@app.post("/convert")
async def convert(file: UploadFile = File(...)) -> dict[str, Any]:
    try:
        content = await file.read()
        if not content:
            raise ValueError("Uploaded file is empty.")
        return convert_products_file(file.filename or "products", content, OUTPUT_DIR)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/convert-products")
async def convert_products(
    file: UploadFile | None = File(None),
    typical_data_file: UploadFile | None = File(None),
    products_source_id: str | None = Form(None),
    product_model_id: str | None = Form(None),
    product_mapping: str | None = Form(None),
    product_mapping_profile: str | None = Form(None),
    enrichment_session: str | None = Form(None),
) -> dict[str, Any]:
    try:
        filename = file.filename if file is not None else "products"
        content = await file.read() if file is not None else b""
        if not content and products_source_id:
            filename, content = load_source_file_session(products_source_id)
        if not content:
            raise ValueError("Uploaded file is empty.")
        mapping = json.loads(product_mapping) if product_mapping else None
        mapping_profile = json.loads(product_mapping_profile) if product_mapping_profile else None
        enrichment = json.loads(enrichment_session) if enrichment_session else None
        typical_payload = None
        if typical_data_file is not None:
            typical_content = await typical_data_file.read()
            if typical_content:
                typical_payload = json.loads(typical_content)
        model_files = load_product_model_session(product_model_id) if product_model_id else None
        return convert_products_file(
            filename or "products",
            content,
            OUTPUT_DIR,
            product_mapping=mapping,
            product_mapping_profile=mapping_profile,
            enrichment_session=enrichment,
            typical_products_payload=typical_payload,
            product_model_files=model_files,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    product_model: UploadFile | None = File(None),
    product_model_files: list[UploadFile] | None = File(None),
    product_model_id: str | None = Form(None),
) -> dict[str, Any]:
    try:
        content = await file.read()
        if not content:
            raise ValueError("Uploaded file is empty.")
        product_model_content = await product_model.read() if product_model is not None else None
        model_files: dict[str, bytes] = {}
        for model_file in product_model_files or []:
            model_content = await model_file.read()
            if model_content:
                model_files[model_file.filename or "model.json"] = model_content
        if not model_files and product_model_id:
            model_files = load_product_model_session(product_model_id)
        return analyze_uploaded_file(
            file.filename or "input",
            content,
            product_model_content=product_model_content,
            product_model_files=model_files or None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/product-model")
async def product_model(product_model_files: list[UploadFile] = File(...)) -> dict[str, Any]:
    try:
        model_files = await model_files_from_uploads(product_model_files=product_model_files)
        if not model_files:
            raise ValueError("Product model files are required.")
        result = analyze_product_model_files(model_files)
        result["model_id"] = save_product_model_session(model_files)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/products/model")
async def products_model_api(files: list[UploadFile] = File(...)) -> dict[str, Any]:
    try:
        model_files = await api_files_payload(files)
        return {"model": bundle_payload(load_product_model(model_files))}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/building-elements/model")
async def building_elements_model_api(files: list[UploadFile] = File(...)) -> dict[str, Any]:
    try:
        model_files = await api_files_payload(files)
        return {"model": bundle_payload(load_building_element_model(model_files))}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/building-elements/analyze")
async def analyze_building_elements_api(
    file: UploadFile = File(...),
    model_files: list[UploadFile] = File(...),
    products_reference: UploadFile = File(...),
) -> dict[str, Any]:
    try:
        model = load_building_element_model(await api_files_payload(model_files))
        product_index = build_product_reference_index(await products_reference.read())
        tables = read_source_tables(file.filename or "building-elements", await file.read())
        analysis = analyze_source_tables(tables, model)
        analysis["product_reference"] = {
            "products_count": product_index.products_count,
            "duplicates": product_index.duplicates,
        }
        return analysis
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/building-elements/preview")
async def building_elements_preview_api(
    file: UploadFile = File(...),
    products_reference: UploadFile = File(...),
    mapping_json: str = Form("{}"),
) -> dict[str, Any]:
    try:
        tables = read_source_tables(file.filename or "building-elements", await file.read())
        rows = tables[0].rows if tables else []
        product_index = build_product_reference_index(await products_reference.read())
        mapping = json.loads(mapping_json or "{}")
        return preview_building_elements(rows, mapping, product_index)
    except (ValueError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/product-model-files/{model_id}")
def product_model_files(model_id: str) -> dict[str, Any]:
    try:
        model_files = load_product_model_session(model_id)
        files = []
        safe_id = "".join(char for char in str(model_id or "") if char.isalnum() or char in "-_")
        model_dir = MODEL_SESSIONS_DIR / safe_id
        for filename, content in model_files.items():
            path = model_dir / Path(filename).name
            files.append(
                {
                    "name": filename,
                    "type": "application/json",
                    "size": len(content),
                    "lastModified": int(path.stat().st_mtime * 1000) if path.exists() else 0,
                    "dataUrl": f"data:application/json;base64,{base64.b64encode(content).decode('ascii')}",
                }
            )
        return {"files": files}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/product-model-accept", response_class=HTMLResponse)
async def product_model_accept(
    products_models_file: UploadFile = File(...),
    products_attributes_file: UploadFile = File(...),
    products_file: UploadFile | None = File(None),
) -> Any:
    try:
        model_files = await model_files_from_uploads(
            products_models_file=products_models_file,
            products_attributes_file=products_attributes_file,
            products_file=products_file,
        )
        model_id = save_product_model_session(model_files)
        return redirect_response(f"/?product_model_id={model_id}")
    except ValueError as exc:
        files = [
            products_models_file.filename or "productsModels.json",
            products_attributes_file.filename or "productsAttributes.json",
        ]
        if products_file is not None:
            files.append(products_file.filename or "products.json")
        return html_response(
            render_home(
                {
                    "error": str(exc),
                    "files": files,
                }
            )
        )


@app.post("/analyze-products-page", response_class=HTMLResponse)
async def analyze_products_page(
    file: UploadFile = File(...),
    product_model_id: str | None = Form(None),
) -> HTMLResponse:
    try:
        content = await file.read()
        if not content:
            raise ValueError("Uploaded file is empty.")
        model_files = load_product_model_session(product_model_id or "")
        model_result = analyze_product_model_files(model_files)
        model_result["model_id"] = product_model_id
        model_result["files"] = list(model_files)
        source_id = save_source_file_session(file.filename or "products", content)
        analysis = analyze_uploaded_file(
            file.filename or "products",
            content,
            product_model_files=model_files,
        )
        return html_response(
            render_home(
                model_result,
                {
                    "mode": "products",
                    "analysis": analysis,
                    "source_id": source_id,
                    "filename": file.filename or "products",
                },
            )
        )
    except ValueError as exc:
        return html_response(render_home({"error": str(exc)}))


@app.post("/mapping-projects")
async def save_mapping_project(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    project_name = str(payload.get("name") or "mapping-project").strip()
    if not project_name:
        raise HTTPException(status_code=400, detail="Project name is required.")
    safe_name = safe_project_name(project_name)
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    path = PROJECTS_DIR / f"{safe_name}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "status": "saved",
        "name": project_name,
        "project_id": safe_name,
        "file": f"/mapping-projects/{safe_name}.json",
    }


@app.get("/mapping-projects")
def list_mapping_projects() -> dict[str, Any]:
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    projects = []
    for path in sorted(PROJECTS_DIR.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            payload = {}
        projects.append(
            {
                "project_id": path.stem,
                "name": payload.get("name") or path.stem,
                "file": f"/mapping-projects/{path.name}",
            }
        )
    return {"projects": projects}


@app.get("/mapping-projects/{filename}")
def mapping_project_file(filename: str) -> FileResponse:
    safe_file = Path(filename).name
    if not safe_file.endswith(".json"):
        raise HTTPException(status_code=404, detail="Mapping project not found.")
    path = PROJECTS_DIR / safe_file
    if not path.exists():
        raise HTTPException(status_code=404, detail="Mapping project not found.")
    return FileResponse(path, media_type="application/json", filename=safe_file)


async def model_files_from_uploads(
    *,
    product_model_files: list[UploadFile] | None = None,
    products_models_file: UploadFile | None = None,
    products_attributes_file: UploadFile | None = None,
    products_file: UploadFile | None = None,
) -> dict[str, bytes]:
    model_files: dict[str, bytes] = {}
    canonical_uploads = [
        ("productsModels.json", products_models_file),
        ("productsAttributes.json", products_attributes_file),
        ("products.json", products_file),
    ]
    for filename, upload in canonical_uploads:
        if upload is None or not hasattr(upload, "read"):
            continue
        content = await upload.read()
        if content:
            model_files[filename] = content
    for upload in product_model_files or []:
        content = await upload.read()
        if content:
            model_files[upload.filename or "model.json"] = content
    return model_files


async def api_files_payload(files: list[UploadFile]) -> dict[str, bytes]:
    payload: dict[str, bytes] = {}
    for upload in files:
        content = await upload.read()
        if content:
            payload[upload.filename or "file.json"] = content
    if not payload:
        raise ValueError("Model files are required.")
    return payload


def save_product_model_session(model_files: dict[str, bytes]) -> str:
    digest = hashlib.sha256()
    for filename in sorted(model_files):
        digest.update(filename.encode("utf-8"))
        digest.update(model_files[filename])
    model_id = digest.hexdigest()[:16]
    model_dir = MODEL_SESSIONS_DIR / model_id
    model_dir.mkdir(parents=True, exist_ok=True)
    for filename, content in model_files.items():
        (model_dir / Path(filename).name).write_bytes(content)
    return model_id


def load_product_model_session(model_id: str) -> dict[str, bytes]:
    safe_id = "".join(char for char in str(model_id or "") if char.isalnum() or char in "-_")
    model_dir = MODEL_SESSIONS_DIR / safe_id
    if not model_dir.exists():
        raise ValueError("Accepted product model was not found on the server.")
    return {path.name: path.read_bytes() for path in model_dir.glob("*.json")}


def save_source_file_session(filename: str, content: bytes) -> str:
    digest = hashlib.sha256()
    digest.update(filename.encode("utf-8"))
    digest.update(content)
    source_id = digest.hexdigest()[:16]
    source_dir = SOURCE_SESSIONS_DIR / source_id
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "source.bin").write_bytes(content)
    (source_dir / "meta.json").write_text(json.dumps({"filename": filename}, ensure_ascii=False), encoding="utf-8")
    return source_id


def load_source_file_session(source_id: str) -> tuple[str, bytes]:
    safe_id = "".join(char for char in str(source_id or "") if char.isalnum() or char in "-_")
    source_dir = SOURCE_SESSIONS_DIR / safe_id
    source_path = source_dir / "source.bin"
    meta_path = source_dir / "meta.json"
    if not source_path.exists():
        raise ValueError("Saved customer data file was not found on the server.")
    filename = "products"
    if meta_path.exists():
        try:
            filename = json.loads(meta_path.read_text(encoding="utf-8")).get("filename") or filename
        except json.JSONDecodeError:
            pass
    return filename, source_path.read_bytes()


def html_response(content: str, status_code: int = 200) -> HTMLResponse:
    return HTMLResponse(
        content,
        status_code=status_code,
        media_type="text/html; charset=utf-8",
        headers={
            "Cache-Control": "no-store, max-age=0",
            "Pragma": "no-cache",
        },
    )


def redirect_response(url: str) -> RedirectResponse:
    return RedirectResponse(
        url=url,
        status_code=303,
        headers={
            "Cache-Control": "no-store, max-age=0",
            "Pragma": "no-cache",
        },
    )


@app.get("/outputs/{job_id}/{filename}")
def output_file(job_id: str, filename: str) -> FileResponse:
    safe_job = Path(job_id).name
    safe_file = Path(filename).name
    path = OUTPUT_DIR / safe_job / safe_file
    if not path.exists():
        raise HTTPException(status_code=404, detail="Output file not found.")
    return FileResponse(path, media_type="application/json", filename=safe_file)


def safe_project_name(value: str) -> str:
    safe = "".join(char if char.isalnum() or char in "-_" else "-" for char in value.strip().lower())
    safe = "-".join(part for part in safe.split("-") if part)
    return safe or "mapping-project"
