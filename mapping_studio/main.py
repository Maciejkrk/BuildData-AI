from __future__ import annotations

from typing import Any

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse

from mapping_studio.services.building_preview import preview_building_elements
from mapping_studio.services.mapping_analyzer import analyze_source_tables, bundle_payload
from mapping_studio.services.pim_model_loader import load_building_element_model, load_product_model
from mapping_studio.services.product_reference import build_product_reference_index
from mapping_studio.services.source_reader import read_source_tables
from data_master_app.web_ui import render_home

app = FastAPI(title="BuildData AI Products", version="0.1.0")


@app.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    return HTMLResponse(render_home(), media_type="text/html; charset=utf-8")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "app": "BuildData AI Products"}


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
        model = load_product_model(await files_payload(model_files))
        tables = read_source_tables(file.filename or "products", await file.read())
        return analyze_source_tables(tables, model)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/building-elements/analyze")
async def analyze_building_elements(
    file: UploadFile = File(...),
    model_files: list[UploadFile] = File(...),
    products_reference: UploadFile = File(...),
) -> dict[str, Any]:
    try:
        model = load_building_element_model(await files_payload(model_files))
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
async def building_elements_preview(
    file: UploadFile = File(...),
    products_reference: UploadFile = File(...),
    mapping_json: str = Form("{}"),
) -> dict[str, Any]:
    import json

    try:
        tables = read_source_tables(file.filename or "building-elements", await file.read())
        rows = tables[0].rows if tables else []
        product_index = build_product_reference_index(await products_reference.read())
        mapping = json.loads(mapping_json or "{}")
        return preview_building_elements(rows, mapping, product_index)
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

