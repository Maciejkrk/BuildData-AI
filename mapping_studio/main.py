from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse

from data_master_app.converter import analyze_uploaded_file as legacy_analyze_products_file
from data_master_app.converter import convert_products_file as legacy_convert_products_file
from mapping_studio.services.building_preview import preview_building_elements_from_tables
from mapping_studio.services.mapping_analyzer import analyze_source_tables, bundle_payload
from mapping_studio.services.pim_model_loader import load_building_element_model, load_product_model
from mapping_studio.services.product_reference import build_product_reference_index
from mapping_studio.services.source_reader import read_source_tables
from data_master_app.web_ui import render_home

app = FastAPI(title="BuildData AI", version="0.1.0")
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs"


@app.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    return HTMLResponse(render_home(), media_type="text/html; charset=utf-8")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "app": "BuildData AI"}


@app.post("/api/products/model")
async def products_model(files: list[UploadFile] = File(...)) -> dict[str, Any]:
    try:
        model_files = await files_payload(files)
        return {"model": bundle_payload(load_product_model(model_files))}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/building-elements/model")
async def building_elements_model(files: list[UploadFile] = File(...)) -> dict[str, Any]:
    try:
        model_files = await files_payload(files)
        return {"model": bundle_payload(load_building_element_model(model_files))}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/products/analyze")
async def analyze_products(file: UploadFile = File(...), model_files: list[UploadFile] = File(...)) -> dict[str, Any]:
    try:
        content = await file.read()
        if not content:
            raise ValueError("Uploaded product file is empty.")
        return legacy_analyze_products_file(
            file.filename or "products",
            content,
            product_model_files=await files_payload(model_files),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/products/convert")
async def convert_products(
    file: UploadFile = File(...),
    model_files: list[UploadFile] = File(...),
    typical_data_file: UploadFile | None = File(None),
    product_mapping: str | None = Form(None),
    product_mapping_profile: str | None = Form(None),
    enrichment_session: str | None = Form(None),
) -> dict[str, Any]:
    try:
        content = await file.read()
        if not content:
            raise ValueError("Uploaded product file is empty.")
        typical_payload = None
        if typical_data_file is not None:
            typical_content = await typical_data_file.read()
            if typical_content:
                typical_payload = json.loads(typical_content)
        return legacy_convert_products_file(
            file.filename or "products",
            content,
            OUTPUT_DIR,
            product_mapping=json.loads(product_mapping) if product_mapping else None,
            product_mapping_profile=json.loads(product_mapping_profile) if product_mapping_profile else None,
            enrichment_session=json.loads(enrichment_session) if enrichment_session else None,
            typical_products_payload=typical_payload,
            product_model_files=await files_payload(model_files),
        )
    except (ValueError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/building-elements/analyze")
async def analyze_building_elements(
    file: UploadFile = File(...),
    model_files: list[UploadFile] = File(...),
    products_reference: UploadFile | None = File(None),
) -> dict[str, Any]:
    try:
        model = load_building_element_model(await files_payload(model_files))
        product_index = None
        if products_reference is not None:
            reference_content = await products_reference.read()
            if reference_content:
                product_index = build_product_reference_index(reference_content)
        tables = read_source_tables(file.filename or "building-elements", await file.read())
        analysis = analyze_source_tables(tables, model)
        analysis["product_reference"] = {
            "loaded": product_index is not None,
            "products_count": product_index.products_count if product_index else 0,
            "duplicates": product_index.duplicates if product_index else {},
            "message": "Referencja products.json nie jest jeszcze wczytana. Produkty w warstwach będzie można dopasować później."
            if product_index is None
            else "Referencja products.json jest wczytana.",
        }
        return analysis
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/building-elements/preview")
async def building_elements_preview(
    file: UploadFile = File(...),
    products_reference: UploadFile | None = File(None),
    mapping_json: str = Form("{}"),
    preview_offset: int = Form(0),
    preview_limit: int = Form(1),
) -> dict[str, Any]:
    import json

    try:
        tables = read_source_tables(file.filename or "building-elements", await file.read())
        rows = tables[0].rows if tables else []
        product_index = None
        if products_reference is not None:
            reference_content = await products_reference.read()
            if reference_content:
                product_index = build_product_reference_index(reference_content)
        mapping = json.loads(mapping_json or "{}")
        return preview_building_elements_from_tables(
            tables,
            mapping,
            product_index,
            preview_offset=preview_offset,
            preview_limit=preview_limit,
        )
    except (ValueError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


async def files_payload(files: list[UploadFile]) -> dict[str, bytes]:
    payload: dict[str, bytes] = {}
    for upload in files:
        content = await upload.read()
        if content:
            payload[upload.filename or "file.json"] = content
    if not payload:
        raise ValueError("Model files are required.")
    return payload
