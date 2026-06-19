from __future__ import annotations

import json
import html

def render_main_menu() -> str:
    return """<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>BuildData AI</title>
  <style>
    :root { --bg:#f3f5f7; --panel:#fff; --line:#d8dde6; --text:#182230; --muted:#667085; --accent:#0f766e; --secondary:#344054; font-family:Arial,sans-serif; }
    * { box-sizing:border-box; }
    body { margin:0; background:var(--bg); color:var(--text); }
    header { min-height:64px; display:flex; align-items:center; justify-content:space-between; padding:14px 24px; border-bottom:1px solid var(--line); background:var(--panel); }
    h1 { margin:0; font-size:22px; }
    main { max-width:980px; margin:0 auto; padding:28px 18px; }
    .intro { margin-bottom:18px; color:var(--muted); line-height:1.45; }
    .choice-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:16px; }
    .choice { display:block; min-height:190px; padding:20px; border:1px solid var(--line); border-radius:6px; background:var(--panel); color:inherit; text-decoration:none; }
    .choice:hover { border-color:var(--accent); box-shadow:0 8px 22px rgba(15,23,42,.08); }
    .choice strong { display:block; margin-bottom:8px; font-size:20px; color:var(--text); }
    .choice span { display:block; color:var(--muted); line-height:1.45; }
    .choice .badge { display:inline-block; margin-top:18px; padding:6px 9px; border-radius:999px; background:#f0fdfa; color:var(--accent); font-weight:700; font-size:12px; }
  </style>
</head>
<body>
  <header>
    <h1>BuildData AI</h1>
  </header>
  <main>
    <p class="intro">Wybierz niezależną sekcję pracy. Projekty produktów i elementów budowlanych są prowadzone osobno.</p>
    <div class="choice-grid">
      <a class="choice" href="/products">
        <strong>Mapowanie Produktów</strong>
        <span>Import pliku klienta, mapowanie cech produktu i typoszeregu, czyszczenie danych oraz generowanie products.json.</span>
        <span class="badge">BuildData AI Products</span>
      </a>
      <a class="choice" href="/building-elements">
        <strong>Mapowanie Building Elementów</strong>
        <span>Mapowanie hierarchii systemów, wariantów, warstw i relacji odczytanej z modelu PIM elementów budowlanych.</span>
        <span class="badge">BuildData AI Building Elements</span>
      </a>
    </div>
  </main>
</body>
</html>"""

def render_home(initial_product_model: dict | None = None, initial_analysis: dict | None = None) -> str:
    initial_model = initial_product_model or {}
    initial_model_accepted = bool(initial_model.get("model_id") and initial_model.get("target_fields"))
    initial_model_json = json.dumps(initial_model, ensure_ascii=False)
    initial_analysis_json = json.dumps(initial_analysis or {}, ensure_ascii=False)
    initial_report_html = render_initial_model_report(initial_model) if initial_model_accepted or initial_model.get("error") else ""
    if initial_analysis:
        initial_report_html = render_initial_analysis_report(initial_analysis)
    report_empty_hidden = " hidden" if initial_report_html else ""
    initial_summary = "Mapping: products" if initial_analysis else ("Model produktu" if initial_model_accepted else ("BĹ‚Ä…d modelu" if initial_model.get("error") else "Brak akcji"))
    initial_status = "Wczytaj i zaakceptuj wymagane pliki modelu PIM."
    model_ready_disabled = "" if initial_model_accepted else " disabled"
    product_model_id_value = html.escape(str(initial_model.get("model_id") or "")) if initial_model_accepted else ""
    products_status = "Gotowe do importu produktĂłw." if initial_model_accepted else "Najpierw zaakceptuj model produktu PIM."
    if initial_model.get("error"):
        initial_status = f"Nie udaĹ‚o siÄ™ zaakceptowaÄ‡ modelu: {html.escape(str(initial_model['error']))}"
    elif initial_model_accepted:
        files = ", ".join(html.escape(str(file)) for file in (initial_model.get("files") or []))
        initial_status = f"Model produktu został zaakceptowany. Wczytane pola modelu: {len(initial_model.get('target_fields') or [])}. Pliki: {files}"
    return """<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>BuildData AI Products</title>
  <style>
    :root {
      --bg: #f3f5f7;
      --panel: #ffffff;
      --soft: #f8fafc;
      --line: #d8dde6;
      --text: #182230;
      --muted: #667085;
      --accent: #0f766e;
      --accent-dark: #0b5f59;
      --secondary: #344054;
      --warn: #9a3412;
      --danger-bg: #fff7ed;
      --danger-line: #fed7aa;
      --ok: #047857;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Arial, sans-serif;
      font-size: 14px;
    }
    header {
      min-height: 58px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 12px 22px;
      border-bottom: 1px solid var(--line);
      background: var(--panel);
    }
    .header-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .top-nav {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .top-nav a {
      display: inline-block;
      padding: 8px 11px;
      border: 1px solid var(--line);
      border-radius: 4px;
      background: #fff;
      color: var(--secondary);
      text-decoration: none;
      font-weight: 700;
      font-size: 13px;
    }
    .top-nav a.active {
      border-color: var(--accent);
      background: #f0fdfa;
      color: var(--accent);
    }
    .model-file-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 6px;
    }
    .language-select {
      width: auto;
      min-width: 140px;
      margin-top: 0;
      padding: 7px 9px;
    }
    h1 { margin: 0; font-size: 20px; }
    h2, .title {
      margin: 0 0 8px;
      font-size: 16px;
      font-weight: 700;
    }
    main {
      display: grid;
      grid-template-columns: 1fr;
      gap: 16px;
      padding: 16px;
    }
    aside, section {
      min-width: 0;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: var(--panel);
    }
    aside {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 14px;
      padding: 14px;
      align-self: start;
    }
    section { overflow: hidden; }
    .panel {
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: var(--soft);
      margin-bottom: 14px;
    }
    aside .panel { margin-bottom: 0; }
    .muted { color: var(--muted); line-height: 1.45; }
    label {
      display: block;
      margin-top: 12px;
      color: #344054;
      font-weight: 700;
      font-size: 12px;
    }
    input[type=file], input[type=text], select, textarea {
      width: 100%;
      margin-top: 6px;
      padding: 9px 10px;
      border: 1px solid var(--line);
      border-radius: 4px;
      background: #fff;
      color: var(--text);
      font: inherit;
    }
    textarea {
      min-height: 76px;
      resize: vertical;
      line-height: 1.35;
    }
    input[type=checkbox] {
      width: 16px;
      height: 16px;
      margin: 0 6px 0 0;
      vertical-align: middle;
    }
    button {
      width: 100%;
      margin-top: 12px;
      padding: 11px 14px;
      border: 0;
      border-radius: 4px;
      background: var(--accent);
      color: #fff;
      font-weight: 700;
      cursor: pointer;
    }
    button.secondary { background: var(--secondary); }
    button:hover { background: var(--accent-dark); }
    button.secondary:hover { background: #1f2937; }
    button:disabled { opacity: .65; cursor: not-allowed; }
    input:disabled, select:disabled, textarea:disabled {
      opacity: .65;
      cursor: not-allowed;
      background: #eef2f6;
    }
    .toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      padding: 13px 16px;
      border-bottom: 1px solid var(--line);
    }
    .content { padding: 16px; }
    .status { margin: 10px 0 0; color: var(--muted); line-height: 1.45; }
    .ok { color: var(--ok); font-weight: 700; }
    .gate-warning {
      margin-top: 12px;
      padding: 10px;
      border: 1px solid var(--danger-line);
      border-radius: 4px;
      background: var(--danger-bg);
      color: var(--warn);
      line-height: 1.45;
    }
    .links {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 12px 0 0;
    }
    .links a {
      display: inline-block;
      padding: 8px 10px;
      border-radius: 4px;
      background: var(--secondary);
      color: #fff;
      text-decoration: none;
      font-weight: 700;
      font-size: 12px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
    }
    th, td {
      border: 1px solid var(--line);
      padding: 8px;
      text-align: left;
      vertical-align: top;
    }
    th { background: #f8fafc; color: #344054; }
    .target-structure {
      display: block;
      gap: 10px;
      margin: 12px 0 18px;
    }
    .structure-group {
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fff;
      margin-bottom: 12px;
      overflow: hidden;
    }
    .structure-group strong {
      display: block;
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      background: #f8fafc;
      color: #344054;
    }
    .structure-field {
      display: grid;
      grid-template-columns: minmax(220px, 300px) minmax(150px, 220px) minmax(220px, 300px) minmax(260px, 1fr);
      gap: 12px;
      padding: 10px 12px;
      border-top: 1px solid #eef2f6;
      color: var(--muted);
      font-size: 12px;
    }
    .structure-field:first-of-type { border-top: 0; }
    .structure-field.is-mapped .structure-field-label { color: var(--text); }
    .structure-field-label {
      font-weight: 700;
      color: #344054;
    }
    .structure-field-key {
      margin-top: 2px;
      color: var(--muted);
      word-break: break-word;
    }
    .structure-field-options:empty::before,
    .structure-field-value:empty::before {
      content: "-";
      color: var(--muted);
    }
    .structure-field-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      margin-top: 5px;
    }
    .mapped-source {
      margin-top: 3px;
      color: var(--muted);
      font-size: 11px;
      font-weight: 700;
      line-height: 1.35;
    }
    .mapped-source-list {
      flex-basis: 100%;
    }
    .mapped-source strong {
      display: block;
      color: #344054;
      font-size: 12px;
      font-weight: 700;
    }
    .structure-value {
      padding: 5px 6px;
      border-radius: 4px;
      background: #f8fafc;
      color: var(--text);
      word-break: break-word;
    }
    .structure-status {
      display: inline-block;
      padding: 3px 6px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: #fff;
      color: var(--muted);
      font-size: 11px;
      font-weight: 700;
    }
    .structure-status.mapped {
      border-color: #99f6e4;
      background: #f0fdfa;
      color: var(--accent);
    }
    .mapping-state {
      color: var(--muted);
      font-weight: 700;
      font-size: 12px;
    }
    .mapping-state.mapped {
      color: var(--accent);
    }
    .type-series-structure {
      grid-column: 1 / -1;
    }
    .type-series-structure table {
      margin-top: 8px;
      table-layout: fixed;
    }
    .type-series-structure th,
    .type-series-structure td {
      font-size: 12px;
      word-break: break-word;
    }
    .mapping-card {
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fff;
      margin-top: 10px;
      overflow: hidden;
    }
    .mapping-section-title {
      margin: 0;
      padding: 12px 14px;
      border-bottom: 1px solid var(--line);
      background: #ffffff;
      font-size: 16px;
      color: #101828;
    }
    .mapping-tools {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
      margin: 12px 0;
    }
    .mapping-tools button {
      width: auto;
      margin-top: 0;
    }
    .rule-summary {
      color: var(--muted);
      font-size: 12px;
    }
    .rule-menu {
      margin: 8px 0 12px;
    }
    .rule-menu[hidden] { display: none; }
    .rule-menu-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
    }
    .rule-menu-header button {
      width: auto;
      margin-top: 0;
    }
    .mapping-row.rule-owned-row { display: none; }
    .mapping-head {
      display: grid;
      grid-template-columns: minmax(170px, 230px) 1fr minmax(260px, 360px);
      gap: 10px;
      padding: 10px;
      background: #f8fafc;
      border-bottom: 1px solid var(--line);
      font-weight: 700;
      color: #344054;
    }
    .mapping-row {
      display: grid;
      grid-template-columns: minmax(170px, 230px) 1fr minmax(260px, 360px);
      gap: 10px;
      padding: 10px;
      border-bottom: 1px solid var(--line);
    }
    .mapping-row.has-conflict {
      background: #fff7ed;
      box-shadow: inset 3px 0 0 var(--warn);
    }
    .mapping-row.has-conflict [data-validation="duplicateTarget"] {
      color: var(--warn);
      font-weight: 700;
    }
    .mapping-row:last-child { border-bottom: 0; }
    .source-name {
      font-weight: 700;
      word-break: break-word;
    }
    .source-meta {
      margin-top: 8px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.4;
    }
    .rule-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(280px, 1fr));
      gap: 12px;
    }
    .rule-grid label { margin-top: 0; }
    .cleanup-details {
      margin-top: 10px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fff;
      overflow: hidden;
    }
    .cleanup-details summary {
      padding: 10px 12px;
      cursor: pointer;
      font-weight: 700;
      color: #344054;
      background: #f8fafc;
    }
    .cleanup-details[open] summary {
      border-bottom: 1px solid var(--line);
    }
    .cleanup-details .rule-grid {
      padding: 12px;
    }
    .readonly-unit {
      margin-top: 6px;
      padding: 9px 10px;
      border: 1px solid var(--line);
      border-radius: 4px;
      background: #f8fafc;
      color: var(--text);
      min-height: 38px;
    }
    .readonly-value {
      border: 1px solid var(--border);
      border-radius: 6px;
      background: #f8fafc;
      padding: 10px 12px;
      min-height: 39px;
      color: var(--ink);
      font-weight: 700;
    }
    .helper {
      display: block;
      margin-top: 5px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 400;
      line-height: 1.35;
    }
    .checkbox-row {
      display: flex;
      align-items: center;
      min-height: 35px;
      color: #344054;
      font-size: 12px;
      font-weight: 700;
    }
    .preview-box {
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #f8fafc;
      overflow: hidden;
    }
    .preview-line {
      display: grid;
      grid-template-columns: 74px 1fr;
      gap: 8px;
      padding: 8px;
      border-bottom: 1px solid var(--line);
      font-size: 12px;
    }
    .preview-line:last-child { border-bottom: 0; }
    .preview-label {
      color: var(--muted);
      font-weight: 700;
    }
    .preview-value {
      overflow-wrap: anywhere;
      white-space: pre-wrap;
      max-height: 150px;
      overflow: auto;
    }
    .after-value {
      color: var(--ok);
      font-weight: 700;
    }
    .warn {
      margin-top: 14px;
      padding: 10px;
      border: 1px solid var(--danger-line);
      border-radius: 4px;
      background: var(--danger-bg);
      color: var(--warn);
    }
    .notice {
      margin: 10px 0;
      padding: 10px;
      border: 1px solid #99f6e4;
      border-radius: 4px;
      background: #f0fdfa;
      color: var(--accent);
      font-weight: 700;
    }
    .mapping-check-panel {
      margin: 12px 0 14px;
      border: 2px solid var(--accent);
    }
    .mapping-check-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 10px 0 0;
    }
    .mapping-check-meta .pill {
      background: #f8fafc;
      font-weight: 700;
    }
    .pill {
      display: inline-block;
      margin: 4px 4px 0 0;
      padding: 4px 7px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: #fff;
      color: #344054;
      font-size: 12px;
    }
    .value-text {
      overflow-wrap: anywhere;
      word-break: break-word;
      white-space: pre-wrap;
    }
    .value-text.compact {
      display: block;
      max-height: 120px;
      overflow: auto;
    }
    .value-link {
      display: inline-block;
      max-width: 100%;
      overflow: hidden;
      text-overflow: ellipsis;
      vertical-align: bottom;
      color: #075985;
      text-decoration: underline;
      overflow-wrap: anywhere;
    }
    .column-samples summary {
      margin-top: 8px;
      color: var(--accent);
      cursor: pointer;
      font-weight: 700;
      font-size: 12px;
    }
    .column-samples table {
      table-layout: fixed;
      font-size: 12px;
    }
    .choice-map-editor {
      grid-column: 1 / -1;
    }
    .choice-map-options {
      max-height: 84px;
      overflow: auto;
      padding: 6px;
      border: 1px solid var(--line);
      border-radius: 4px;
      background: #f8fafc;
    }
    .choice-map-table {
      margin-top: 8px;
      table-layout: fixed;
      font-size: 12px;
    }
    .choice-map-table select {
      margin-top: 0;
    }
    .choice-map-value {
      overflow-wrap: anywhere;
      white-space: pre-wrap;
    }
    .column-samples td:first-child,
    .column-samples th:first-child {
      width: 64px;
    }
    .json-sample {
      max-height: 360px;
      overflow: auto;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 4px;
      background: #0f172a;
      color: #e5e7eb;
      font-family: Consolas, "Courier New", monospace;
      font-size: 12px;
      line-height: 1.45;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
    }
    .split {
      display: grid;
      grid-template-columns: minmax(260px, 360px) 1fr;
      gap: 14px;
      align-items: start;
    }
    .live-preview-panel {
      margin: 12px 0 14px;
      padding: 14px;
      border: 2px solid var(--accent);
      border-radius: 6px;
      background: #ffffff;
      box-shadow: 0 8px 20px rgba(15, 23, 42, .08);
    }
    .live-preview-header {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      margin-bottom: 8px;
    }
    .live-badge {
      display: inline-block;
      padding: 4px 8px;
      border-radius: 999px;
      background: #ecfdf3;
      color: var(--ok);
      font-weight: 700;
      font-size: 12px;
      white-space: nowrap;
    }
    .preview-columns {
      display: grid;
      grid-template-columns: 1fr;
      gap: 14px;
    }
    .enrichment-added {
      background: #fff1f2;
      box-shadow: inset 4px 0 0 #dc2626;
    }
    .enrichment-added td:first-child::after {
      content: " zmienione";
      color: #b91c1c;
      font-weight: 800;
    }
    .enrichment-added-cell {
      background: #fff1f2;
      box-shadow: inset 4px 0 0 #dc2626;
    }
    .manual-edit-table input {
      width: 100%;
    }
    .editable-value-input {
      width: 100%;
      min-width: 0;
      max-width: 100%;
      margin-top: 0;
    }
    .type-series-preview-scroll {
      width: 100%;
      max-width: 100%;
      overflow-x: auto;
      border: 1px solid var(--line);
      border-radius: 4px;
    }
    .type-series-preview-table {
      min-width: 100%;
      width: max-content;
      table-layout: auto;
      margin-top: 0;
    }
    .type-series-preview-table th,
    .type-series-preview-table td {
      min-width: 96px;
      max-width: 220px;
      overflow-wrap: anywhere;
    }
    .type-series-preview-table th:first-child,
    .type-series-preview-table td:first-child {
      min-width: 42px;
      width: 42px;
      max-width: 42px;
      text-align: center;
    }
    .type-series-preview-table .editable-value-input {
      min-width: 64px;
      width: 100%;
    }
    .manual-edit-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 8px 0 12px;
    }
    .manual-edit-actions button {
      width: auto;
      margin-top: 0;
    }
    .collapsed-mapping-list {
      display: grid;
      gap: 8px;
      margin-top: 8px;
    }
    .collapsed-mapping-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding: 9px 10px;
      border: 1px solid var(--line);
      border-radius: 4px;
      background: #f8fafc;
    }
    .collapsed-mapping-item button {
      width: auto;
      margin-top: 0;
    }
    .enrichment-preview-options {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px 16px;
      margin: 10px 0;
    }
    .enrichment-actions-row {
      display: grid;
      grid-template-columns: repeat(3, minmax(220px, 1fr));
      gap: 24px;
      margin: 22px 0 8px;
      align-items: start;
    }
    .enrichment-actions-row button {
      width: 100%;
      min-height: 58px;
      margin-top: 0;
    }
    .enrichment-automation-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(240px, 1fr));
      gap: 12px;
      align-items: end;
    }
    .enrichment-grid {
      display: grid;
      grid-template-columns: minmax(220px, 1fr) minmax(220px, 1fr);
      gap: 12px;
      align-items: end;
    }
    .enrichment-section {
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 12px;
      margin: 12px 0;
      background: #fff;
    }
    .product-checkbox-list {
      max-height: 260px;
      overflow: auto;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 8px;
      background: #f8fafc;
      display: grid;
      gap: 6px;
    }
    .product-checkbox-list label {
      display: flex;
      align-items: flex-start;
      gap: 8px;
      margin: 0;
      font-weight: 500;
    }
    .product-checkbox-list input {
      width: auto;
      margin-top: 2px;
    }
    .enrichment-session-list {
      display: grid;
      gap: 8px;
      margin-top: 10px;
    }
    .enrichment-entry {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 10px;
      padding: 10px;
      border: 1px solid var(--line);
      border-radius: 4px;
      background: #fff;
    }
    .workspace-switcher {
      display: flex;
      gap: 0;
      width: 100%;
      margin: 12px 0;
      border: 1px solid var(--line);
      border-radius: 6px;
      overflow: hidden;
      background: #fff;
    }
    .workspace-switcher button {
      flex: 1 1 0;
      border: 0;
      border-radius: 0;
      padding: 14px 18px;
      background: #f8fafc;
      color: var(--muted);
      font-size: 15px;
      font-weight: 800;
    }
    .workspace-switcher button + button {
      border-left: 1px solid var(--line);
    }
    .workspace-switcher button[aria-pressed="true"] {
      background: var(--accent);
      color: #fff;
      border-color: var(--accent);
    }
    .workflow-step {
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fff;
      padding: 14px;
      margin-top: 12px;
    }
    .workflow-step h3 {
      margin-top: 0;
    }
    .workflow-step.is-secondary {
      background: #f8fafc;
    }
    .inline-check {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-top: 8px;
      font-weight: 700;
    }
    .inline-check input {
      width: auto;
    }
    .file-status-list {
      display: grid;
      gap: 8px;
      margin: 10px 0;
    }
    .file-status {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      padding: 8px 10px;
      border: 1px solid var(--line);
      border-radius: 4px;
      background: #f8fafc;
      font-size: 13px;
    }
    .file-status strong {
      color: var(--text);
    }
    .file-status .ok {
      color: var(--ok);
      font-weight: 800;
    }
    .source-mode-panel[hidden] {
      display: none;
    }
    .workspace-pane[hidden] {
      display: none;
    }
    pre {
      max-height: 320px;
      overflow: auto;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 4px;
      background: #0f172a;
      color: #e5e7eb;
      white-space: pre-wrap;
    }
    @media (max-width: 1100px) {
      .mapping-head, .mapping-row {
        grid-template-columns: 1fr;
      }
      .mapping-head { display: none; }
      .split { grid-template-columns: 1fr; }
      .preview-columns { grid-template-columns: 1fr; }
      .enrichment-grid { grid-template-columns: 1fr; }
      .enrichment-actions-row { grid-template-columns: 1fr; }
      .enrichment-automation-grid { grid-template-columns: 1fr; }
      .structure-field { grid-template-columns: 1fr; }
      .rule-grid { grid-template-columns: 1fr; }
    }
    @media (max-width: 900px) {
      main { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <header>
    <h1>BuildData AI Products</h1>
    <nav class="top-nav" aria-label="Workspace">
      <a href="/" data-i18n="nav.menu">Wróć do menu głównego</a>
      <a class="active" href="/products" data-i18n="nav.products">Produkty</a>
      <a href="/building-elements" data-i18n="nav.buildingElements">Elementy budowlane</a>
    </nav>
    <div class="header-actions">
      <span class="muted" data-i18n="app.subtitle">Import, mapowanie, czyszczenie i eksport PIM JSON</span>
      <select id="languageSelect" class="language-select" aria-label="Language">
        <option value="pl">Polski</option>
        <option value="en">English</option>
      </select>
    </div>
  </header>
  <main>
    <aside>
      <form id="productModelPanel" class="panel" action="/product-model-accept" method="post" enctype="multipart/form-data">
        <h2 data-i18n="model.title">Model produktu PIM</h2>
        <div class="muted" data-i18n="model.help">Najpierw wczytaj dwa pliki z PIM: productsModels.json i productsAttributes.json. One tworzÄ… obowiÄ…zujÄ…cy model produktu dla caĹ‚ego procesu.</div>
        <input id="productModelId" type="hidden" name="product_model_id" value="__PRODUCT_MODEL_ID_VALUE__">
        <div class="model-file-grid">
          <label><span data-i18n="model.modelsFile">productsModels.json</span>
            <input id="productModelsFile" name="products_models_file" type="file" accept=".json" required onchange="window.productModelFileChanged && window.productModelFileChanged()">
          </label>
          <label><span data-i18n="model.attributesFile">productsAttributes.json</span>
            <input id="productAttributesFile" name="products_attributes_file" type="file" accept=".json" required onchange="window.productModelFileChanged && window.productModelFileChanged()">
          </label>
        </div>
        <div class="gate-warning" data-i18n="model.warning">Zmiana tych plikĂłw kasuje aktualnÄ… strukturÄ™ mapowania, podglÄ…d i wygenerowany products.json. Dalsze funkcje sÄ… dostÄ™pne dopiero po zaakceptowaniu modelu.</div>
        <button type="submit" id="acceptProductModelBtn" data-i18n="model.accept" disabled>Zaakceptuj model produktu</button>
        <div id="productModelStatus" class="status">__INITIAL_PRODUCT_MODEL_STATUS__</div>
      </form>

      <div id="productsPanel" class="panel">
        <h2 data-i18n="products.title">1. Produkty</h2>
        <div class="muted" data-i18n="products.help">Analizuj plik, przypisz kolumny do modelu produktu i typoszeregu, ustaw czyszczenie wartoĹ›ci, potem generuj products.json.</div>
        <form id="productsForm" action="/analyze-products-page" method="post" enctype="multipart/form-data">
          <input id="productsProductModelId" type="hidden" name="product_model_id" value="__PRODUCT_MODEL_ID_VALUE__">
          <input id="productsSourceId" type="hidden" name="products_source_id" value="__PRODUCTS_SOURCE_ID__">
          <label><span data-i18n="products.file">Plik produktĂłw</span>
            <input id="productsFile" name="file" type="file" accept=".xlsx,.xlsm,.json,.csv,.tsv"__MODEL_READY_DISABLED__>
          </label>
          <button type="submit" class="secondary" id="analyzeProductsBtn" name="_action" value="analyze" data-i18n="products.analyze"__MODEL_READY_DISABLED__>Analizuj i mapuj produkty</button>
          <button type="button" id="generateProductsBtn" name="_action" value="convert" data-i18n="products.generate" onclick="window.generateProductsFromButton && window.generateProductsFromButton(); return false;"__MODEL_READY_DISABLED__>Generuj products.json z mapowania</button>
        </form>
        <div id="productsStatus" class="status" data-i18n="products.ready">__PRODUCTS_STATUS__</div>
        <div id="productsLinks" class="links"></div>
      </div>

      <div id="projectPanel" class="panel">
        <h2 data-i18n="project.title">Projekt mapowania</h2>
        <div class="muted" data-i18n="project.help">Zapisuje decyzje mapowania, czyszczenia i reguĹ‚y wierszy, ĹĽeby moĹĽna byĹ‚o wrĂłciÄ‡ do tej samej pracy dla kolejnych plikĂłw klienta.</div>
        <label><span data-i18n="project.name">Nazwa projektu</span>
          <input id="projectName" type="text" value="import-produktow"__MODEL_READY_DISABLED__>
        </label>
        <button type="button" class="secondary" id="saveProjectBtn" data-i18n="project.save"__MODEL_READY_DISABLED__>Zapisz projekt mapowania na dysku</button>
        <button type="button" class="secondary" id="generateEnrichedProductsMenuBtn" data-i18n="enrichment.saveEnriched"__MODEL_READY_DISABLED__>Zapisz uzupeĹ‚niony products.json</button>
        <label><span data-i18n="project.load">OtwĂłrz projekt mapowania z dysku</span>
          <input id="loadProjectFile" type="file" accept=".json">
        </label>
        <div id="projectStatus" class="status" data-i18n="project.notSaved">Projekt nie jest jeszcze zapisany.</div>
        <div id="projectLinks" class="links"></div>
      </div>

      <input id="typicalFile" type="file" accept=".json" hidden>
      <input id="typicalModelsFile" type="file" accept=".json" hidden>
      <input id="typicalAttributesFile" type="file" accept=".json" hidden>
      <input id="typicalRawFile" type="file" accept=".xlsx,.xlsm,.json,.csv,.tsv" hidden>

    </aside>

    <section>
      <div class="toolbar">
        <strong data-i18n="report.title">Mapowanie i podglÄ…d</strong>
        <span id="summary" class="muted" data-i18n="report.idle">__INITIAL_SUMMARY__</span>
      </div>
      <div class="content">
        <div id="reportEmpty" class="muted" data-i18n="report.empty"__REPORT_EMPTY_HIDDEN__>Po analizie pojawi siÄ™ docelowa struktura modelu. Dla kaĹĽdej cechy PIM wybierz kolumnÄ™ z pliku importowanego, czyszczenie, jednostkÄ™ albo mapÄ™ odpowiedzi sĹ‚ownikowych.</div>
        <div id="report">__INITIAL_REPORT_HTML__</div>
      </div>
    </section>
  </main>
  <script>
    window.productModelFileChanged = function() {
      var fields = [
        ["productModelsFile", "productsModels.json"],
        ["productAttributesFile", "productsAttributes.json"]
      ];
      var selected = [];
      var missing = [];
      for (var index = 0; index < fields.length; index += 1) {
        var input = document.getElementById(fields[index][0]);
        if (input && input.files && input.files.length) selected.push(fields[index][1] + ": " + input.files[0].name);
        else missing.push(fields[index][1]);
      }
      var button = document.getElementById("acceptProductModelBtn");
      if (button) button.disabled = missing.length > 0;
      var status = document.getElementById("productModelStatus");
      if (status) {
        status.innerHTML = missing.length
          ? "Wybrane pliki: " + (selected.length ? selected.join(", ") : "brak") + "<br>Brakuje: " + missing.join(", ")
          : "Wybrane pliki: " + selected.join(", ") + ". MoĹĽesz zaakceptowaÄ‡ model.";
      }
    };
  </script>

  <script>
    const $ = (id) => document.getElementById(id);
    let productMapping = null;
    let productMappingProfile = null;
    let generatedProductsJobId = null;
    let generatedProductsUrl = "";
    let mainProductTable = null;
    let supplementFileForMapping = null;
    let supplementAnalysisTable = null;
    let supplementMapping = null;
    let supplementMappingProfile = null;
    let supplementProductsPayload = null;
    let supplementProductsUrl = "";
    let activeTable = null;
    let activeMode = null;
    let loadedProject = null;
    let loadedProjectFiles = { productModelFiles: [], productsFile: null, typicalDataFile: null };
    let enrichmentSession = { manual_entries: [], typical_sources: [], typical_matches: [] };
    let typicalProductsForEnrichment = [];
    let typicalProductsPayloadForEnrichment = [];
    let typicalSourceAttributes = [];
    let typicalSourceMode = "raw_file";
    let mappingWorkspaceTab = "mapping";
    let productPreviewIndex = 0;
    let manualEditEnabled = false;
    let showMainMappingOnly = false;
    let collapsedSupplementMappings = [];
    const INITIAL_PRODUCT_MODEL = __INITIAL_PRODUCT_MODEL_JSON__;
    const INITIAL_ANALYSIS = __INITIAL_ANALYSIS_JSON__;
    const INITIAL_PRODUCT_MODEL_ACCEPTED = Boolean(INITIAL_PRODUCT_MODEL.model_id && (INITIAL_PRODUCT_MODEL.target_fields || []).length);
    let activeProductModelFields = INITIAL_PRODUCT_MODEL_ACCEPTED ? (INITIAL_PRODUCT_MODEL.target_fields || []) : [];
    let activeProductModelId = INITIAL_PRODUCT_MODEL_ACCEPTED ? INITIAL_PRODUCT_MODEL.model_id : "";
    let acceptingProductModel = false;
    let currentLang = localStorage.getItem("aiDataMasterLang") || "pl";
    let lastElementAnalysis = null;
    let pimModelAccepted = INITIAL_PRODUCT_MODEL_ACCEPTED;
    let acceptedProductModelSignature = "";
    const REQUIRED_PRODUCT_MODEL_FILES = [
      { key: "productsmodels", label: "productsModels.json" },
      { key: "productsattributes", label: "productsAttributes.json" }
    ];
    const PRODUCT_MODEL_DEFINITION_FILE_KEYS = new Set(["productsmodels", "productsattributes"]);

    const I18N = {
      pl: {
        "nav.products": "Produkty",
        "nav.menu": "Wróć do menu głównego",
        "nav.buildingElements": "Elementy budowlane",
        "app.subtitle": "Mapowanie danych produktowych i eksport products.json",
        "model.title": "Model produktu PIM",
        "model.help": "Najpierw wczytaj dwa pliki z PIM: productsModels.json i productsAttributes.json. One tworzÄ… obowiÄ…zujÄ…cy model produktu dla caĹ‚ego procesu.",
        "model.file": "Pliki modelu produktu PIM JSON",
        "model.modelsFile": "Plik productsModels.json",
        "model.attributesFile": "Plik productsAttributes.json",
        "model.productsFile": "Plik products.json",
        "model.default": "Wczytaj i zaakceptuj wymagane pliki modelu PIM.",
        "model.required": "Wczytaj i zaakceptuj wymagane pliki modelu PIM.",
        "model.selected": "Wybrano pliki modelu produktu",
        "model.warning": "Zmiana tych plikĂłw kasuje aktualnÄ… strukturÄ™ mapowania, podglÄ…d i wygenerowany products.json. Dalsze funkcje sÄ… dostÄ™pne dopiero po zaakceptowaniu modelu.",
        "model.accept": "Zaakceptuj model produktu",
        "model.accepted": "Model produktu został zaakceptowany. Możesz rozpocząć import danych klienta.",
        "model.previewTitle": "Model produktu PIM",
        "model.previewHelp": "To jest docelowa struktura produktu odczytana z plikĂłw modelu PIM. ReguĹ‚y i mapowanie pojawiÄ… siÄ™ po wczytaniu pliku danych klienta.",
        "model.previewSummary": "Model produktu",
        "model.fieldsLoaded": "Wczytane pola modelu",
        "model.missingFiles": "Brakuje wymaganych plikĂłw: ",
        "model.changed": "Pliki modelu zostaĹ‚y zmienione. Dotychczasowe mapowanie i wygenerowane dane zostaĹ‚y wyczyszczone. Zaakceptuj model ponownie.",
        "gate.locked": "Najpierw zaakceptuj model produktu PIM.",
        "products.title": "1. Produkty",
        "products.help": "Analizuj plik, przypisz kolumny do modelu produktu i typoszeregu, ustaw czyszczenie wartoĹ›ci, potem generuj products.json.",
        "products.file": "Plik produktĂłw",
        "products.analyze": "Analizuj i mapuj produkty",
        "products.generate": "Generuj products.json z mapowania",
        "products.outputTitle": "Wynik products.json",
        "products.outputHelp": "To zapisuje wĹ‚aĹ›ciwy plik danych produktu. Projekt mapowania zapisuje tylko ustawienia pracy.",
        "products.saveAs": "Zapisz products.json jako...",
        "products.saveMissing": "Najpierw wygeneruj products.json z aktualnego mapowania.",
        "products.saveFailed": "Nie udaĹ‚o siÄ™ zapisaÄ‡ products.json.",
        "products.saved": "Zapisano products.json:",
        "products.ready": "Gotowe do importu produktĂłw.",
        "project.title": "Projekt mapowania",
        "project.help": "Zapisuje decyzje mapowania, czyszczenia i reguĹ‚y wierszy, ĹĽeby moĹĽna byĹ‚o wrĂłciÄ‡ do tej samej pracy dla kolejnych plikĂłw klienta.",
        "project.name": "Nazwa projektu",
        "project.save": "Zapisz projekt mapowania na dysku",
        "project.load": "OtwĂłrz projekt mapowania z dysku",
        "project.notSaved": "Projekt nie jest jeszcze zapisany.",
        "typical.title": "UzupeĹ‚nianie zmapowanych danych",
        "typical.help": "Wczytaj dane typowe w formacie wynikowego products.json albo dopisz brakujÄ…ce wartoĹ›ci rÄ™cznie. Sesja uzupeĹ‚niania jest zapisywana razem z projektem mapowania.",
        "typical.file": "Plik danych typowych",
        "typical.optional": "Opcjonalnie: wybierz plik z danymi typowymi.",
        "typical.waitForMapping": "Najpierw wczytaj plik importowany i utwĂłrz mapowanie produktĂłw.",
        "enrichment.title": "UzupeĹ‚nianie zmapowanych danych",
        "enrichment.help": "Tu zapisujesz dodatkowÄ… sesjÄ™ uzupeĹ‚niania. WartoĹ›ci rÄ™czne i ĹşrĂłdĹ‚a typowe sÄ… pamiÄ™tane osobno od mapowania kolumn.",
        "enrichment.typicalLoaded": "Plik danych typowych poprawny",
        "enrichment.typicalInvalid": "Plik danych typowych musi byÄ‡ JSON-em w formacie wynikowego products.json.",
        "enrichment.productsFound": "produkty",
        "enrichment.attributesFound": "atrybuty",
        "enrichment.manualTitle": "Dopisz wartoĹ›Ä‡ rÄ™cznie",
        "enrichment.targetField": "Cecha z modelu PIM",
        "enrichment.value": "WartoĹ›Ä‡ do wpisania",
        "enrichment.scope": "Zakres",
        "enrichment.scopeCurrent": "Aktualnie oglÄ…dany produkt",
        "enrichment.scopeAll": "Wszystkie produkty",
        "enrichment.scopeSelectedProducts": "Wybrane produkty z listy",
        "enrichment.scopeMatchByFeature": "Dopasuj produkty po tej samej cesze",
        "enrichment.mode": "Tryb",
        "enrichment.missingOnly": "UzupeĹ‚nij tylko puste",
        "enrichment.replace": "ZastÄ…p istniejÄ…ce wartoĹ›ci",
        "enrichment.addManual": "Dodaj do sesji rÄ™cznej",
        "enrichment.session": "Sesja uzupeĹ‚niania",
        "enrichment.noEntries": "Brak rÄ™cznych uzupeĹ‚nieĹ„.",
        "enrichment.noTypical": "Nie wczytano danych typowych.",
        "enrichment.remove": "UsuĹ„",
        "enrichment.savedWithProject": "Sesja zostanie zapisana z projektem mapowania i przekazana do generowania products.json.",
        "enrichment.mappingTab": "Mapowanie produktu",
        "enrichment.enrichmentTab": "UzupeĹ‚nianie danych",
        "enrichment.workflowTabs": "Etap pracy",
        "enrichment.fileMappingStep": "1. Plik uzupeĹ‚nieĹ„ i mapowanie",
        "enrichment.applyStep": "2. Zastosowanie uzupeĹ‚nieĹ„",
        "enrichment.fileSelector": "Lista plikĂłw uzupeĹ‚nieĹ„",
        "enrichment.loadExternalFile": "Wczytaj plik uzupeĹ‚nieĹ„",
        "enrichment.sourceMode": "Typ ĹşrĂłdĹ‚a uzupeĹ‚nieĹ„",
        "enrichment.sourceMapped": "Zmapowany products.json z modelem ĹşrĂłdĹ‚owym",
        "enrichment.sourceRaw": "Surowy plik do mapowania od nowa",
        "enrichment.supplementFile": "Plik uzupeĹ‚nieĹ„ do mapowania",
        "enrichment.supplementMapLater": "Ten plik musi zostaÄ‡ zmapowany do aktualnego modelu produktu. Mapowanie uzupeĹ‚nieĹ„ jest osobnym etapem i nie nadpisuje gĹ‚Ăłwnego mapowania produktĂłw.",
        "enrichment.mapSupplement": "Mapuj plik uzupeĹ‚nieĹ„",
        "enrichment.prepareSupplement": "Zaakceptuj mapowanie uzupeĹ‚nieĹ„",
        "enrichment.supplementReady": "Dane uzupeĹ‚nieĹ„ sÄ… przygotowane do wyboru produktu wzorcowego.",
        "enrichment.supplementMappingTitle": "Mapowanie pliku uzupeĹ‚nieĹ„",
        "enrichment.backToProducts": "WrĂłÄ‡ do mapowania produktĂłw",
        "enrichment.noSupplementMapping": "Najpierw zmapuj plik uzupeĹ‚nieĹ„.",
        "enrichment.noSupplementFile": "Najpierw wybierz plik uzupeĹ‚nieĹ„.",
        "enrichment.supplementPrepared": "Mapowanie uzupeĹ‚nieĹ„ zostaĹ‚o zaakceptowane. Wybierz produkt wzorcowy i cechy do dopisania.",
        "enrichment.sourceModels": "Model ĹşrĂłdĹ‚owy danych typowych",
        "enrichment.loadSourceModels": "Wczytaj productsModels.json ĹşrĂłdĹ‚a",
        "enrichment.loadSourceAttributes": "Wczytaj productsAttributes.json ĹşrĂłdĹ‚a",
        "enrichment.loadRawFile": "Wczytaj surowy plik",
        "enrichment.loaded": "wczytano",
        "enrichment.notLoaded": "nie wczytano",
        "enrichment.mappedProductsFile": "Zmapowany products.json",
        "enrichment.rawFile": "Surowy plik",
        "enrichment.rawModeHelp": "Surowy plik wymaga osobnego mapowania do aktualnego modelu przed uĹĽyciem jako dane typowe.",
        "enrichment.sourceModelMissing": "Dodaj model ĹşrĂłdĹ‚owy, jeĹ›li plik pochodzi z innego modelu niĹĽ aktualny.",
        "enrichment.sourceModelLoaded": "Wczytano model ĹşrĂłdĹ‚owy danych typowych.",
        "enrichment.attributeMap": "Mapowanie cech ĹşrĂłdĹ‚owych do aktualnego modelu",
        "enrichment.sourceAttribute": "Cecha ĹşrĂłdĹ‚owa",
        "enrichment.targetAttribute": "Cecha w aktualnym modelu",
        "enrichment.noAttributeMap": "Brak cech do mapowania albo plik uzupeĹ‚nieĹ„ nie zostaĹ‚ jeszcze wczytany.",
        "enrichment.preserveExisting": "Nie zmieniaj istniejÄ…cych danych",
        "enrichment.noVariantFill": "UzupeĹ‚nianie dotyczy cech produktu. Warianty typoszeregu nie sÄ… uzupeĹ‚niane osobno.",
        "enrichment.clearSession": "UsuĹ„ dopisane dane",
        "enrichment.sessionCleared": "Sesja uzupeĹ‚nieĹ„ zostaĹ‚a wyczyszczona.",
        "enrichment.typicalSection": "Mapowanie pliku uzupeĹ‚nieĹ„",
        "enrichment.manualSection": "UzupeĹ‚nianie rÄ™czne",
        "enrichment.chooseTypicalFile": "Wczytaj plik uzupeĹ‚nieĹ„",
        "enrichment.currentProduct": "Aktualny produkt importowany",
        "enrichment.typicalProduct": "Rekord z pliku uzupeĹ‚nieĹ„",
        "enrichment.supplementMatchField": "Taka sama cecha w pliku uzupeĹ‚nieĹ„",
        "enrichment.addTypicalMatch": "Zastosuj zmianÄ™ dla wskazanych produktĂłw",
        "enrichment.saveEnriched": "Zapisz uzupeĹ‚niony products.json",
        "enrichment.plannedTitle": "Zaplanowane uzupeĹ‚nienia dla tego produktu",
        "enrichment.plannedEmpty": "Brak zaplanowanych uzupeĹ‚nieĹ„ dla aktualnego produktu.",
        "enrichment.manualCurrentProduct": "Edycja rÄ™czna aktualnego produktu",
        "enrichment.applyTypeSeriesAll": "Dopisz cechy typoszeregu do wszystkich wariantĂłw produktu",
        "enrichment.askTypeSeriesAll": "Dla cech typoszeregu wybierz, czy dopisa\u0107 warto\u015b\u0107 do wszystkich wariant\u00f3w produktu.",
        "enrichment.enableManualEdit": "W\u0142\u0105cz edycj\u0119 r\u0119czn\u0105",
        "enrichment.disableManualEdit": "Wy\u0142\u0105cz edycj\u0119 r\u0119czn\u0105",
        "enrichment.saveManualEdits": "Zapisz r\u0119czne zmiany produktu",
        "enrichment.undoProductChanges": "Cofnij zmiany tego produktu",
        "enrichment.editingDisabled": "W\u0142\u0105cz edycj\u0119 r\u0119czn\u0105, aby zmienia\u0107 warto\u015bci w polach danych.",
        "enrichment.editingEnabled": "Edytujesz warto\u015bci aktualnego produktu bezpo\u015brednio w podgl\u0105dzie. Zapis zmian doda je do sesji r\u0119cznej.",
        "enrichment.manualSaved": "R\u0119czne zmiany produktu zosta\u0142y zapisane w sesji.",
        "enrichment.manualNoValues": "Nie wpisano \u017cadnych warto\u015bci do zapisania.",
        "enrichment.productChangesUndone": "Zmiany dla aktualnego produktu zosta\u0142y cofni\u0119te.",
        "enrichment.collapsedMapping": "Zaakceptowane mapowanie uzupe\u0142nie\u0144",
        "enrichment.editSupplementMapping": "Popraw mapowanie",
        "enrichment.noTypicalProducts": "Najpierw wczytaj poprawny plik danych typowych.",
        "enrichment.noMatches": "Brak przypisanych produktĂłw typowych.",
        "enrichment.matchSaved": "Produkt typowy zostaĹ‚ przypisany do aktualnego produktu.",
        "enrichment.modelCheckOk": "Dane typowe pasujÄ… do struktury modelu PIM.",
        "enrichment.modelCheckWarn": "Uwaga: czÄ™Ĺ›Ä‡ atrybutĂłw danych typowych nie wystÄ™puje w aktualnym modelu PIM.",
        "enrichment.manualModeHelp": "Wybierz produkt w podglÄ…dzie powyĹĽej, wpisz wartoĹ›Ä‡ i dodaj jÄ… do sesji rÄ™cznej. Przy generowaniu zostanie zapamiÄ™tane, ĹĽe ta wartoĹ›Ä‡ pochodzi z uzupeĹ‚nienia rÄ™cznego.",
        "report.title": "Mapowanie i podglÄ…d",
        "report.idle": "Brak akcji",
        "report.empty": "Po analizie pojawi siÄ™ docelowa struktura modelu. Dla kaĹĽdej cechy PIM wybierz kolumnÄ™ z pliku importowanego, czyszczenie, jednostkÄ™ albo mapÄ™ odpowiedzi sĹ‚ownikowych.",
        "mapping.ignore": "PomiĹ„ kolumnÄ™",
        "mapping.targetField": "Docelowe pole modelu",
        "mapping.unitManual": "Jednostka ĹşrĂłdĹ‚owa wpisana rÄ™cznie",
        "mapping.unitColumn": "Jednostka ĹşrĂłdĹ‚owa z kolumny",
        "mapping.targetUnit": "Jednostka w modelu",
        "mapping.noTargetUnit": "Brak jednostki w modelu",
        "mapping.unitConversionFactor": "FormuĹ‚a przeliczenia do jednostki modelu",
        "mapping.unitConversionHelp": "Wynik = wartoĹ›Ä‡ * mnoĹĽnik. Np. 0.001 dla mm -> m. Zostaw 1 albo puste, jeĹ›li wartoĹ›Ä‡ jest juĹĽ w jednostce modelu.",
        "mapping.removeText": "UsuĹ„ tekst z wartoĹ›ci",
        "mapping.replaceText": "ZamieĹ„ tekst",
        "mapping.replaceWith": "Na tekst",
        "mapping.splitBy": "Podziel wartoĹ›Ä‡ po tekĹ›cie",
        "mapping.splitPart": "WeĹş czÄ™Ĺ›Ä‡ nr",
        "mapping.addExtraction": "Dodaj kolejnÄ… wartoĹ›Ä‡ z tej kolumny",
        "mapping.extraction": "Ekstrakcja",
        "mapping.trim": "UsuĹ„ spacje z poczÄ…tku i koĹ„ca",
        "mapping.decimalComma": "ZamieĹ„ przecinek dziesiÄ™tny na kropkÄ™",
        "mapping.parseNumber": "Zostaw tylko liczbÄ™",
        "mapping.before": "Przed",
        "mapping.after": "Po",
        "mapping.confidence": "PewnoĹ›Ä‡",
        "mapping.missing": "Braki",
        "mapping.clientColumn": "Kolumna klienta",
        "mapping.modelField": "Cecha modelu PIM",
        "mapping.productSection": "Mapowanie cech ogĂłlnych produktu",
        "mapping.typeSeriesSection": "Mapowanie typoszeregu",
        "mapping.emptySection": "Brak pĂłl modelu w tej sekcji.",
        "mapping.sourceColumn": "Kolumna z pliku importowanego",
        "mapping.mappedColumn": "zmapowana kolumna",
        "mapping.noSource": "Nie importuj tej cechy",
        "mapping.mappingCleanup": "Mapowanie i czyszczenie",
        "mapping.valuePreview": "PodglÄ…d wartoĹ›ci",
        "mapping.moreRecords": "PokaĹĽ kolejne rekordy",
        "mapping.rowNumber": "Wiersz",
        "mapping.rowValue": "WartoĹ›Ä‡",
        "mapping.usedByRules": "Kolumny i pola modelu obsĹ‚ugiwane przez reguĹ‚y sÄ… ukryte z rÄ™cznego mapowania",
        "mapping.checkApplied": "Struktura modelu zostaĹ‚a przeliczona dla aktualnych reguĹ‚ i mapowania.",
        "model.mapped": "zmapowane",
        "model.empty": "puste",
        "model.status": "Status",
        "model.sourceColumn": "kolumna",
        "model.sourceRule": "reguĹ‚a",
        "model.moreValues": "wiÄ™cej wartoĹ›ci",
        "model.singleChoice": "jedna z wielu",
        "model.multiChoice": "wiele z wielu",
        "model.options": "opcje",
        "rows.title": "Reguły wierszy i hierarchii",
        "rows.help": "UĹĽyj tego, gdy plik ma osobne wiersze produktĂłw i osobne wiersze wariantĂłw. WskaĹĽ typ wiersza oraz relacjÄ™ ID produktu -> Parent ID wariantu.",
        "rows.openMenu": "Reguły wierszy i hierarchii",
        "rows.closeMenu": "Zamknij reguĹ‚y",
        "rows.menuHint": "OtwĂłrz tylko wtedy, gdy import ma wiersze grup, produktĂłw albo relacje parent-child.",
        "rows.summaryEmpty": "Brak aktywnych reguĹ‚.",
        "rows.summary": "Aktywne reguĹ‚y",
        "rows.typeColumn": "Kolumna okreĹ›lajÄ…ca typ wiersza",
        "rows.typeColumnHelp": "Kolumna zawierajÄ…ca definicjÄ™ typu wiersza, np. Product albo Article.",
        "rows.mode": "Typ relacji wierszy",
        "rows.modeProductVariants": "Produkt -> warianty typoszeregu",
        "rows.modeHelp": "Wiersz oznaczony jako produkt tworzy produkt, a wiersz oznaczony jako wariant tworzy wiersz tabeli typoszeregu.",
        "rows.productValues": "WartoĹ›Ä‡ w kolumnie oznaczajÄ…ca produkt",
        "rows.productValuesHelp": "Wpisz albo wybierz wartoĹ›Ä‡ z kolumny typu wiersza, np. Product albo PR. Ten wiersz utworzy produkt.",
        "rows.groupValues": "WartoĹ›Ä‡ w kolumnie oznaczajÄ…ca wariant",
        "rows.groupValuesHelp": "Wpisz albo wybierz wartoĹ›Ä‡ z kolumny typu wiersza, np. Article albo AR. Ten wiersz utworzy wariant w tabeli typoszeregu.",
        "rows.productIdColumn": "Kolumna ID produktu",
        "rows.productIdColumnHelp": "WartoĹ›Ä‡ z tej kolumny identyfikuje wiersz produktu, do ktĂłrego majÄ… byÄ‡ przypiÄ™te warianty.",
        "rows.variantParentIdColumn": "Kolumna Parent ID wariantu",
        "rows.variantParentIdColumnHelp": "WartoĹ›Ä‡ z tej kolumny w wierszu wariantu musi wskazywaÄ‡ ID produktu nadrzÄ™dnego.",
        "rows.prefixColumn": "Kolumna z ID do rozpoznawania prefiksu",
        "rows.prefixColumnHelp": "UĹĽyj tego, gdy grupy i produkty odrĂłĹĽnia poczÄ…tek ID, np. PR dla grup i AR dla produktĂłw.",
        "rows.productPrefixes": "Prefiksy oznaczajÄ…ce produkt",
        "rows.productPrefixesHelp": "Np. AR. MoĹĽesz wpisaÄ‡ kilka wartoĹ›ci po przecinku.",
        "rows.groupPrefixes": "Prefiksy oznaczajÄ…ce wariant",
        "rows.groupPrefixesHelp": "Np. AR. MoĹĽesz wpisaÄ‡ kilka wartoĹ›ci po przecinku.",
        "rows.mappingHint": "NazwÄ™ produktu, kod produktu, nazwÄ™ wariantu i inne cechy przypisz niĹĽej w zwykĹ‚ym mapowaniu pĂłl modelu.",
        "rows.rule": "Reguła",
        "rows.addRule": "Dodaj reguĹ‚Ä™",
        "rows.applyRules": "Zastosuj reguĹ‚y",
        "rows.applied": "Reguły zostały zastosowane. Wskazane kolumny są teraz ukryte z ręcznego mapowania.",
        "rows.removeRule": "UsuĹ„ reguĹ‚Ä™",
        "rows.statsProductRows": "Wiersze produktu",
        "rows.statsVariantRows": "Wiersze wariantu",
        "rows.statsMatchedVariants": "Warianty dopiÄ™te po Parent ID",
        "rows.statsOrphanVariants": "Warianty bez pasujÄ…cego produktu",
        "mapping.check": "SprawdĹş aktualne mapowanie",
        "mapping.checkTitle": "Wynik aktualnego mapowania",
        "mapping.checkHelp": "To jest wynik dla prĂłbki danych po zastosowaniu aktualnych reguĹ‚ wierszy, mapowania kolumn i czyszczenia.",
        "mapping.detectedProducts": "Rozpoznane produkty z prĂłbki",
        "mapping.checkedAt": "Sprawdzono",
        "mapping.noPreviewRows": "Brak rozpoznanych produktĂłw w prĂłbce.",
        "mapping.rawPreview": "PodglÄ…d JSON",
        "mapping.duplicateTarget": "To pole docelowe jest przypisane wiÄ™cej niĹĽ raz. ZmieĹ„ jedno mapowanie albo ustaw je jako ignorowane.",
        "mapping.duplicateTargetBlocked": "Nie moĹĽna zapisaÄ‡ ani wygenerowaÄ‡ danych: usuĹ„ podwĂłjne mapowania pĂłl docelowych.",
        "mapping.choiceMatched": "Dopasowane opcje",
        "mapping.choiceUnmatched": "Poza sĹ‚ownikiem - nie zostanie zaimportowane bez mapy wartoĹ›ci",
        "mapping.choiceMap": "Mapa wartoĹ›ci klienta do opcji PIM",
        "mapping.choiceMapHelp": "Jedna para w linii, np. termo = Izolacja termiczna. Lewa strona to wartoĹ›Ä‡ z pliku importowanego, prawa strona to opcja z modelu PIM. WartoĹ›ci spoza sĹ‚ownika bez takiej mapy sÄ… pomijane w imporcie.",
        "mapping.choiceOptions": "Opcje PIM",
        "mapping.choiceClientValue": "WartoĹ›Ä‡ klienta",
        "mapping.choicePimOption": "Opcja PIM",
        "mapping.choiceDoNotImport": "Nie importuj bez mapy",
        "mapping.choicePickSource": "Wybierz kolumnÄ™, aby zobaczyÄ‡ wartoĹ›ci z danych klienta.",
        "preview.title": "Na ĹĽywo: wynik mapowania",
        "preview.help": "Pierwszy rozpoznany produkt po mapowaniu, czyszczeniu i dziedziczeniu kontekstu z wierszy grup.",
        "preview.sample": "z prĂłbki",
        "preview.productFields": "Pola produktu",
        "preview.typeSeries": "Tabela typoszeregu",
        "preview.field": "Pole",
        "preview.variantFeature": "Cecha wariantu",
        "preview.cleanedValue": "WartoĹ›Ä‡ po czyszczeniu",
        "preview.unit": "Jednostka",
        "preview.source": "ĹąrĂłdĹ‚o",
        "preview.context": "kontekst",
        "preview.fromGroupRow": "z wiersza grupy",
        "preview.previousProduct": "Poprzedni produkt",
        "preview.nextProduct": "NastÄ™pny produkt",
        "preview.productCounter": "Produkt",
        "preview.chooseProduct": "Wybierz produkt",
        "none": "Brak",
        "missing.productFields": "Brak przypisanych pĂłl produktu.",
        "missing.typeSeries": "Brak przypisanych pĂłl typoszeregu.",
        "analysis.running": "Analiza trwa.",
        "analysis.ready": "Analiza gotowa. SprawdĹş mapowanie i podglÄ…d po prawej.",
        "analysis.chooseFile": "Wybierz plik do analizy.",
        "analysis.noTables": "Brak tabel do analizy.",
        "status.error": "BĹ‚Ä…d",
        "project.analyzeFirst": "Najpierw przeanalizuj plik i ustaw mapowanie.",
        "project.saveFailed": "Nie udaĹ‚o siÄ™ zapisaÄ‡ projektu.",
        "project.saved": "Zapisano projekt na dysku:",
        "project.download": "pobierz projekt JSON",
        "project.downloaded": "Projekt zostaĹ‚ pobrany jako plik JSON. JeĹ›li przeglÄ…darka pyta o lokalizacjÄ™ pobierania, wybierz docelowy katalog.",
        "project.loaded": "Wczytano projekt:",
        "project.loadFailed": "Nie udaĹ‚o siÄ™ wczytaÄ‡ projektu mapowania.",
        "project.loadedComplete": "Projekt zawiera zapisane pliki modelu i dane klienta.",
        "project.legacyMissingFiles": "Ten projekt nie zawiera zapisanych plikĂłw. WskaĹĽ ponownie pliki modelu PIM i plik danych klienta.",
        "project.missingModelFiles": "W projekcie brakuje plikĂłw modelu PIM:",
        "project.missingProductsFile": "W projekcie brakuje pliku danych klienta. WskaĹĽ go ponownie.",
        "quality.title": "JakoĹ›Ä‡ danych",
        "quality.column": "Kolumna",
        "quality.filled": "UzupeĹ‚nione",
        "quality.missing": "Braki",
        "quality.missingRows": "Wiersze z brakami",
        "quality.typical": "Typowe wartoĹ›ci",
        "sample.title": "PrĂłbka danych z pliku"
      },
      en: {
        "nav.products": "Products",
        "nav.menu": "Back to main menu",
        "nav.buildingElements": "Building elements",
        "app.subtitle": "Product data mapping and products.json export",
        "model.title": "Product PIM Model",
        "model.help": "First load two files from PIM: productsModels.json and productsAttributes.json. They define the product model for the whole process.",
        "model.file": "Product PIM model JSON files",
        "model.modelsFile": "productsModels.json file",
        "model.attributesFile": "productsAttributes.json file",
        "model.productsFile": "products.json file",
        "model.default": "Load and accept the required PIM model files.",
        "model.required": "Load and accept the required PIM model files.",
        "model.selected": "Selected product model files",
        "model.warning": "Changing these files clears the current mapping structure, preview and generated products.json. Other functions are available only after accepting the model.",
        "model.accept": "Accept product model",
        "model.accepted": "The product model has been accepted. You can start importing customer data.",
        "model.previewTitle": "Product PIM Model",
        "model.previewHelp": "This is the target product structure read from the PIM model files. Rules and mapping appear after loading the customer data file.",
        "model.previewSummary": "Product model",
        "model.fieldsLoaded": "Loaded model fields",
        "model.missingFiles": "Missing required files: ",
        "model.changed": "Model files were changed. Existing mapping and generated data were cleared. Accept the model again.",
        "gate.locked": "Accept the product PIM model first.",
        "products.title": "1. Products",
        "products.help": "Analyze a file, map columns to the product model and type series, configure cleanup, then generate products.json.",
        "products.file": "Products file",
        "products.analyze": "Analyze and map products",
        "products.generate": "Generate products.json from mapping",
        "products.outputTitle": "products.json output",
        "products.outputHelp": "This saves the actual product data file. The mapping project only saves work settings.",
        "products.saveAs": "Save products.json as...",
        "products.saveMissing": "Generate products.json from the current mapping first.",
        "products.saveFailed": "Could not save products.json.",
        "products.saved": "Saved products.json:",
        "products.ready": "Ready to import products.",
        "project.title": "Mapping Project",
        "project.help": "Saves mapping, cleanup and row hierarchy decisions so the same work can be reused for later customer files.",
        "project.name": "Project name",
        "project.save": "Save mapping project to disk",
        "project.load": "Open mapping project from disk",
        "project.notSaved": "The project is not saved yet.",
        "typical.title": "Mapped Data Enrichment",
        "typical.help": "Load typical data in generated products.json format or add missing values manually. The enrichment session is saved with the mapping project.",
        "typical.file": "Typical data file",
        "typical.optional": "Optional: choose a typical-data file.",
        "typical.waitForMapping": "Load the imported file and create product mapping first.",
        "enrichment.title": "Mapped data enrichment",
        "enrichment.help": "This is a separate enrichment session. Manual values and typical-data sources are kept separately from column mapping.",
        "enrichment.typicalLoaded": "Typical-data file is valid",
        "enrichment.typicalInvalid": "Typical-data file must be JSON in generated products.json format.",
        "enrichment.productsFound": "products",
        "enrichment.attributesFound": "attributes",
        "enrichment.manualTitle": "Add a value manually",
        "enrichment.targetField": "PIM model feature",
        "enrichment.value": "Value to write",
        "enrichment.scope": "Scope",
        "enrichment.scopeCurrent": "Current preview product",
        "enrichment.scopeAll": "All products",
        "enrichment.scopeSelectedProducts": "Selected products from the list",
        "enrichment.scopeMatchByFeature": "Match products by the same feature",
        "enrichment.mode": "Mode",
        "enrichment.missingOnly": "Fill empty values only",
        "enrichment.replace": "Replace existing values",
        "enrichment.addManual": "Add to manual session",
        "enrichment.session": "Enrichment session",
        "enrichment.noEntries": "No manual enrichments.",
        "enrichment.noTypical": "No typical data loaded.",
        "enrichment.remove": "Remove",
        "enrichment.savedWithProject": "The session will be saved with the mapping project and sent when generating products.json.",
        "enrichment.mappingTab": "Product mapping",
        "enrichment.enrichmentTab": "Data enrichment",
        "enrichment.workflowTabs": "Work stage",
        "enrichment.fileMappingStep": "1. Enrichment file and mapping",
        "enrichment.applyStep": "2. Apply enrichments",
        "enrichment.fileSelector": "Enrichment file list",
        "enrichment.loadExternalFile": "Load enrichment file",
        "enrichment.sourceMode": "Enrichment source type",
        "enrichment.sourceMapped": "Mapped products.json with source model",
        "enrichment.sourceRaw": "Raw file to map from scratch",
        "enrichment.supplementFile": "Enrichment file to map",
        "enrichment.supplementMapLater": "This file must be mapped to the active product model. Enrichment mapping is a separate stage and does not replace the main product mapping.",
        "enrichment.mapSupplement": "Map enrichment file",
        "enrichment.prepareSupplement": "Accept enrichment mapping",
        "enrichment.supplementReady": "Enrichment data is ready for choosing a reference product.",
        "enrichment.supplementMappingTitle": "Enrichment file mapping",
        "enrichment.backToProducts": "Back to product mapping",
        "enrichment.noSupplementMapping": "Map the enrichment file first.",
        "enrichment.noSupplementFile": "Choose an enrichment file first.",
        "enrichment.supplementPrepared": "The enrichment mapping was accepted. Choose a reference product and features to apply.",
        "enrichment.sourceModels": "Typical-data source model",
        "enrichment.loadSourceModels": "Load source productsModels.json",
        "enrichment.loadSourceAttributes": "Load source productsAttributes.json",
        "enrichment.loadRawFile": "Load raw file",
        "enrichment.loaded": "loaded",
        "enrichment.notLoaded": "not loaded",
        "enrichment.mappedProductsFile": "Mapped products.json",
        "enrichment.rawFile": "Raw file",
        "enrichment.rawModeHelp": "A raw file needs a separate mapping to the active model before it can be used as typical data.",
        "enrichment.sourceModelMissing": "Add the source model if the file comes from a different model than the active one.",
        "enrichment.sourceModelLoaded": "Typical-data source model loaded.",
        "enrichment.attributeMap": "Map source features to the active model",
        "enrichment.sourceAttribute": "Source feature",
        "enrichment.targetAttribute": "Feature in active model",
        "enrichment.noAttributeMap": "No features to map or the enrichment file is not loaded yet.",
        "enrichment.preserveExisting": "Do not change existing data",
        "enrichment.noVariantFill": "Enrichment applies to product features. Type-series variants are not enriched one by one.",
        "enrichment.clearSession": "Remove added data",
        "enrichment.sessionCleared": "The enrichment session has been cleared.",
        "enrichment.typicalSection": "Enrichment file mapping",
        "enrichment.manualSection": "Manual enrichment",
        "enrichment.chooseTypicalFile": "Load enrichment file",
        "enrichment.currentProduct": "Current imported product",
        "enrichment.typicalProduct": "Record from enrichment file",
        "enrichment.supplementMatchField": "Same feature in enrichment file",
        "enrichment.addTypicalMatch": "Apply change to selected products",
        "enrichment.saveEnriched": "Save enriched products.json",
        "enrichment.plannedTitle": "Planned enrichments for this product",
        "enrichment.plannedEmpty": "No planned enrichments for the current product.",
        "enrichment.manualCurrentProduct": "Manual edit for current product",
        "enrichment.applyTypeSeriesAll": "Apply type-series features to all product variants",
        "enrichment.askTypeSeriesAll": "For type-series features, choose whether to apply the value to all variants.",
        "enrichment.enableManualEdit": "Enable manual editing",
        "enrichment.disableManualEdit": "Disable manual editing",
        "enrichment.saveManualEdits": "Save manual product edits",
        "enrichment.undoProductChanges": "Undo this product's changes",
        "enrichment.editingDisabled": "Enable manual editing to change values in data fields.",
        "enrichment.editingEnabled": "You are editing the current product directly in the preview. Saving adds the values to the manual session.",
        "enrichment.manualSaved": "Manual product changes were saved in the session.",
        "enrichment.manualNoValues": "No values were entered to save.",
        "enrichment.productChangesUndone": "Changes for the current product were undone.",
        "enrichment.collapsedMapping": "Accepted enrichment mapping",
        "enrichment.editSupplementMapping": "Edit mapping",
        "enrichment.noTypicalProducts": "Load a valid typical-data file first.",
        "enrichment.noMatches": "No typical-product assignments.",
        "enrichment.matchSaved": "The typical product was assigned to the current product.",
        "enrichment.modelCheckOk": "Typical data matches the PIM model structure.",
        "enrichment.modelCheckWarn": "Warning: some typical-data attributes are not present in the active PIM model.",
        "enrichment.manualModeHelp": "Choose a product in the preview above, enter a value and add it to the manual session. On generation, the value will be remembered as manually added.",
        "report.title": "Mapping and Preview",
        "report.idle": "No action",
        "report.empty": "After analysis, the target model structure appears here. For each PIM feature, choose the imported-file column, cleanup, unit or dictionary-answer map.",
        "mapping.ignore": "Ignore column",
        "mapping.targetField": "Target model field",
        "mapping.unitManual": "Manual source unit",
        "mapping.unitColumn": "Source unit from column",
        "mapping.targetUnit": "Model unit",
        "mapping.noTargetUnit": "No model unit",
        "mapping.unitConversionFactor": "Conversion formula to model unit",
        "mapping.unitConversionHelp": "Result = value * multiplier. For example 0.001 for mm -> m. Leave 1 or blank if the value already uses the model unit.",
        "mapping.removeText": "Remove text from value",
        "mapping.replaceText": "Replace text",
        "mapping.replaceWith": "With text",
        "mapping.splitBy": "Split value by text",
        "mapping.splitPart": "Use part no.",
        "mapping.addExtraction": "Add another value from this column",
        "mapping.extraction": "Extraction",
        "mapping.trim": "Trim leading and trailing spaces",
        "mapping.decimalComma": "Convert decimal comma to dot",
        "mapping.parseNumber": "Keep only the number",
        "mapping.before": "Before",
        "mapping.after": "After",
        "mapping.confidence": "Confidence",
        "mapping.missing": "Missing",
        "mapping.clientColumn": "Client column",
        "mapping.modelField": "PIM model feature",
        "mapping.productSection": "General product feature mapping",
        "mapping.typeSeriesSection": "Type-series mapping",
        "mapping.emptySection": "No model fields in this section.",
        "mapping.sourceColumn": "Imported-file column",
        "mapping.mappedColumn": "mapped column",
        "mapping.noSource": "Do not import this feature",
        "mapping.mappingCleanup": "Mapping and cleanup",
        "mapping.valuePreview": "Value preview",
        "mapping.moreRecords": "Show more records",
        "mapping.rowNumber": "Row",
        "mapping.rowValue": "Value",
        "mapping.usedByRules": "Columns and model fields handled by row rules are hidden from manual mapping",
        "mapping.checkApplied": "The model structure was recalculated for the current rules and mapping.",
        "model.mapped": "mapped",
        "model.empty": "empty",
        "model.status": "Status",
        "model.sourceColumn": "column",
        "model.sourceRule": "rule",
        "model.moreValues": "more values",
        "model.singleChoice": "single choice",
        "model.multiChoice": "multiple choice",
        "model.options": "options",
        "rows.title": "Row and Hierarchy Rules",
        "rows.help": "Use this when the file has separate product rows and variant rows. Select the row type and the product ID -> variant Parent ID relation.",
        "rows.openMenu": "Row and hierarchy rules",
        "rows.closeMenu": "Close rules",
        "rows.menuHint": "Open only when the import has group rows, product rows or parent-child relations.",
        "rows.summaryEmpty": "No active rules.",
        "rows.summary": "Active rules",
        "rows.typeColumn": "Column defining row type",
        "rows.typeColumnHelp": "Column containing the row type definition, for example Product or Article.",
        "rows.mode": "Row relation type",
        "rows.modeProductVariants": "Product -> type-series variants",
        "rows.modeHelp": "Rows marked as products create products. Rows marked as variants create type-series table rows under the parent product.",
        "rows.productValues": "Value meaning product",
        "rows.productValuesHelp": "Enter or choose the value from the row-type column, for example Product or PR. This row creates a product.",
        "rows.groupValues": "Value meaning variant",
        "rows.groupValuesHelp": "Enter or choose the value from the row-type column, for example Article or AR. This row creates a type-series variant.",
        "rows.productIdColumn": "Product ID column",
        "rows.productIdColumnHelp": "The value in this column identifies the product row that variants should attach to.",
        "rows.variantParentIdColumn": "Variant Parent ID column",
        "rows.variantParentIdColumnHelp": "The value in this column on a variant row must point to the parent product ID.",
        "rows.prefixColumn": "ID column for prefix detection",
        "rows.prefixColumnHelp": "Use this when groups and products are distinguished by ID prefix, for example PR for groups and AR for products.",
        "rows.productPrefixes": "Prefixes meaning product",
        "rows.productPrefixesHelp": "For example AR. You can enter multiple values separated by commas.",
        "rows.groupPrefixes": "Prefixes meaning variant",
        "rows.groupPrefixesHelp": "For example AR. You can enter multiple values separated by commas.",
        "rows.mappingHint": "Assign the product name, product code, variant name and other features below in the normal model-field mapping.",
        "rows.rule": "Rule",
        "rows.addRule": "Add rule",
        "rows.applyRules": "Apply rules",
        "rows.applied": "Rules were applied. Selected columns are now hidden from manual mapping.",
        "rows.removeRule": "Remove rule",
        "rows.statsProductRows": "Product rows",
        "rows.statsVariantRows": "Variant rows",
        "rows.statsMatchedVariants": "Variants matched by Parent ID",
        "rows.statsOrphanVariants": "Variants without a matching product",
        "mapping.check": "Check current mapping",
        "mapping.checkTitle": "Current Mapping Result",
        "mapping.checkHelp": "This is the sample-data result after applying current row rules, column mapping and cleanup.",
        "mapping.detectedProducts": "Detected products from sample",
        "mapping.checkedAt": "Checked",
        "mapping.noPreviewRows": "No products detected in the sample.",
        "mapping.rawPreview": "JSON preview",
        "mapping.duplicateTarget": "This target field is assigned more than once. Change one mapping or set it to ignore.",
        "mapping.duplicateTargetBlocked": "Cannot save or generate data: remove duplicate target-field mappings.",
        "mapping.choiceMatched": "Matched options",
        "mapping.choiceUnmatched": "Outside dictionary - will not be imported without a value map",
        "mapping.choiceMap": "Client value to PIM option map",
        "mapping.choiceMapHelp": "One pair per line, for example thermal = Thermal insulation. Left side is the client-file value, right side is the PIM model option. Values outside the dictionary are skipped during import unless mapped here.",
        "mapping.choiceOptions": "PIM options",
        "mapping.choiceClientValue": "Client value",
        "mapping.choicePimOption": "PIM option",
        "mapping.choiceDoNotImport": "Do not import without a map",
        "mapping.choicePickSource": "Choose a source column to see values from the customer data.",
        "preview.title": "Live: Mapping Result",
        "preview.help": "First detected product after mapping, cleanup and context inherited from group rows.",
        "preview.sample": "from sample",
        "preview.productFields": "Product fields",
        "preview.typeSeries": "Type-series table",
        "preview.field": "Field",
        "preview.variantFeature": "Variant feature",
        "preview.cleanedValue": "Cleaned value",
        "preview.unit": "Unit",
        "preview.source": "Source",
        "preview.context": "context",
        "preview.fromGroupRow": "from group row",
        "preview.previousProduct": "Previous product",
        "preview.nextProduct": "Next product",
        "preview.productCounter": "Product",
        "preview.chooseProduct": "Choose product",
        "none": "None",
        "missing.productFields": "No product fields mapped.",
        "missing.typeSeries": "No type-series fields mapped.",
        "analysis.running": "Analysis is running.",
        "analysis.ready": "Analysis complete. Check mapping and preview on the right.",
        "analysis.chooseFile": "Choose a file to analyze.",
        "analysis.noTables": "No tables found for analysis.",
        "status.error": "Error",
        "project.analyzeFirst": "Analyze a file and configure mapping first.",
        "project.saveFailed": "Could not save the project.",
        "project.saved": "Saved project to disk:",
        "project.download": "download project JSON",
        "project.downloaded": "The project was downloaded as a JSON file. If the browser asks for a download location, choose the target folder.",
        "project.loaded": "Loaded project:",
        "project.loadFailed": "Could not load the mapping project.",
        "project.loadedComplete": "The project contains saved model files and customer data.",
        "project.legacyMissingFiles": "This project does not contain saved files. Select the PIM model files and customer data file again.",
        "project.missingModelFiles": "The project is missing PIM model files:",
        "project.missingProductsFile": "The project is missing the customer data file. Select it again.",
        "quality.title": "Data Quality",
        "quality.column": "Column",
        "quality.filled": "Filled",
        "quality.missing": "Missing",
        "quality.missingRows": "Rows with missing values",
        "quality.typical": "Typical values",
        "sample.title": "Sample rows from file"
      }
    };

    function t(key) {
      return I18N[currentLang]?.[key] || I18N.pl[key] || key;
    }

    function applyLanguage() {
      document.documentElement.lang = currentLang;
      $("languageSelect").value = currentLang;
      for (const element of document.querySelectorAll("[data-i18n]")) {
        element.textContent = t(element.dataset.i18n);
      }
      if (activeTable && activeMode) {
        showReport(renderMappingEditor(activeTable, activeMode), "Mapping: products");
        applyLoadedProjectToUi(activeMode);
        attachMappingEvents(activeMode);
      } else if (isProductModelAccepted() && activeProductModelFields.length) {
        renderProductModelPreview();
      }
      updateWorkflowGate();
    }

    function setLanguage(language) {
      currentLang = language;
      localStorage.setItem("aiDataMasterLang", language);
      applyLanguage();
    }

    const esc = (value) => String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");

    function linkLabel(url, limit = 72) {
      let label = String(url || "");
      try {
        const parsed = new URL(label);
        const fileName = decodeURIComponent(parsed.pathname.split("/").filter(Boolean).pop() || parsed.hostname);
        label = fileName || parsed.hostname;
      } catch (_) {
        label = label.replace(new RegExp("^https?://"), "");
      }
      return label.length > limit ? `${label.slice(0, limit - 1)}â€¦` : label;
    }

    function renderLinkedText(value, options = {}) {
      const text = displayCellValue(value);
      if (!text) return "";
      const limit = options.limit || 900;
      const compact = text.length > limit;
      const visibleText = compact ? `${text.slice(0, limit)}â€¦` : text;
      const linked = [];
      const urlPattern = /https?:\\/\\/[^\\s"'<>]+/g;
      let lastIndex = 0;
      for (const match of visibleText.matchAll(urlPattern)) {
        const rawUrl = match[0].replace(/[.,;:]+$/, "");
        const start = match.index || 0;
        linked.push(esc(visibleText.slice(lastIndex, start)));
        linked.push(`<a class="value-link" href="${esc(rawUrl)}" target="_blank" rel="noopener noreferrer" title="${esc(rawUrl)}">${esc(linkLabel(rawUrl))}</a>`);
        lastIndex = start + match[0].length;
      }
      linked.push(esc(visibleText.slice(lastIndex)));
      return `<span class="value-text${compact ? " compact" : ""}">${linked.join("")}</span>`;
    }

    function renderJsonSample(value) {
      return renderLinkedText(JSON.stringify(value || [], null, 2), { limit: 6000 });
    }

    function fileOrMessage(inputId, statusId, message) {
      const file = fileForInput(inputId);
      if (!file) {
        $(statusId).textContent = message;
        return null;
      }
      return file;
    }

    function fileForInput(inputId) {
      const chosen = $(inputId)?.files?.[0];
      if (chosen) return chosen;
      if (inputId === "productsFile") return loadedProjectFiles.productsFile || null;
      if (inputId === "typicalFile") return $("typicalFileVisible")?.files?.[0] || loadedProjectFiles.typicalDataFile || null;
      return null;
    }

    async function projectFileFromFile(file) {
      const dataUrl = await new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(String(reader.result || ""));
        reader.onerror = () => reject(reader.error);
        reader.readAsDataURL(file);
      });
      return {
        name: file.name,
        type: file.type || "application/octet-stream",
        size: file.size,
        lastModified: file.lastModified,
        dataUrl
      };
    }

    function fileFromProjectFile(item) {
      if (!item?.dataUrl || !item?.name) return null;
      const [header, base64] = String(item.dataUrl).split(",", 2);
      if (!base64) return null;
      const mime = String(header || "").match(/^data:([^;]+);base64$/)?.[1] || item.type || "application/octet-stream";
      const binary = atob(base64);
      const bytes = new Uint8Array(binary.length);
      for (let index = 0; index < binary.length; index += 1) {
        bytes[index] = binary.charCodeAt(index);
      }
      return new File([bytes], item.name, {
        type: item.type || mime,
        lastModified: item.lastModified || Date.now()
      });
    }

    async function projectFilesFromModelSession() {
      if (!activeProductModelId) return [];
      const response = await fetch(`/product-model-files/${encodeURIComponent(activeProductModelId)}`);
      if (!response.ok) return [];
      const data = await response.json();
      return (data.files || []).map(fileFromProjectFile).filter(Boolean);
    }

    async function productModelFilesForProject() {
      const selected = selectedProductModelFiles();
      if (selected.length) return selected;
      return projectFilesFromModelSession();
    }

    function safeProjectFilename(name) {
      const safe = String(name || "mapping-project")
        .trim()
        .replace(/[.]json$/i, "")
        .replace(/[<>:"/\\|?*]+/g, "-")
        .replace(/\\s+/g, "-")
        .replace(/-+/g, "-")
        .replace(/^-|-$/g, "");
      return `${safe || "mapping-project"}.json`;
    }

    function safeProductsFilename(name) {
      const safe = String(name || "products")
        .trim()
        .replace(/[.]json$/i, "")
        .replace(/[<>:"/\\|?*]+/g, "-")
        .replace(/\\s+/g, "-")
        .replace(/-+/g, "-")
        .replace(/^-|-$/g, "");
      return `${safe || "products"}.json`;
    }

    async function saveJsonFileToDisk(filename, payload) {
      const json = JSON.stringify(payload, null, 2);
      const blob = new Blob([json], { type: "application/json" });
      if (window.showSaveFilePicker) {
        const handle = await window.showSaveFilePicker({
          suggestedName: filename,
          types: [
            {
              description: "Mapping project JSON",
              accept: { "application/json": [".json"] }
            }
          ]
        });
        const writable = await handle.createWritable();
        await writable.write(blob);
        await writable.close();
        return { mode: "picker", filename: handle.name || filename };
      }
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
      return { mode: "download", filename };
    }

    function showReport(html, summary) {
      $("reportEmpty").hidden = true;
      $("report").innerHTML = html;
      $("summary").textContent = summary;
    }

    function renderProductModelPreview() {
      const fields = activeProductModelFields || [];
      if (!fields.length) return;
      showReport(`
        <div class="panel">
          <h2>${esc(t("model.previewTitle"))}</h2>
          <div class="muted">${esc(t("model.previewHelp"))}</div>
          <div class="mapping-check-meta">
            <span class="pill">${esc(t("model.fieldsLoaded"))}: ${esc(fields.length)}</span>
            <span class="pill">${esc(productModelFileNames())}</span>
          </div>
          <div class="target-structure" id="targetStructure">${renderTargetStructure(fields)}</div>
        </div>`,
        t("model.previewSummary")
      );
    }

    function productModelInputItems() {
      return [
        { key: "productsmodels", label: "productsModels.json", inputId: "productModelsFile", file: $("productModelsFile")?.files?.[0] || null },
        { key: "productsattributes", label: "productsAttributes.json", inputId: "productAttributesFile", file: $("productAttributesFile")?.files?.[0] || null }
      ];
    }

    function selectedProductModelFiles() {
      const selected = productModelInputItems().map(item => item.file).filter(Boolean);
      return selected.length ? selected : (loadedProjectFiles.productModelFiles || []);
    }

    function selectedProductModelKeys() {
      const inputItems = productModelInputItems();
      const selectedFromInputs = inputItems.filter(item => item.file);
      if (selectedFromInputs.length) return new Set(selectedFromInputs.map(item => item.key));
      return new Set((loadedProjectFiles.productModelFiles || []).map(modelFileKey).filter(Boolean));
    }

    function normalizedFileStem(file) {
      return String(file?.name || "").toLowerCase().replace(new RegExp("[.]json$", "i"), "").replace(/[^a-z0-9]+/g, "");
    }

    function modelFileKey(file) {
      const stem = normalizedFileStem(file);
      if (stem.includes("productsmodels") || stem.includes("productmodels")) return "productsmodels";
      if (stem.includes("productsattributes") || stem.includes("productattributes")) return "productsattributes";
      if (stem === "products" || stem === "product" || stem.endsWith("products") || stem.endsWith("product")) return "products";
      return "";
    }

    function productModelSignature(files = selectedProductModelFiles()) {
      return files.map((file) => `${file.name}:${file.size}:${file.lastModified}`).sort().join("|");
    }

    function missingProductModelFiles(files = null) {
      const keys = files ? new Set(files.map(modelFileKey).filter(Boolean)) : selectedProductModelKeys();
      return REQUIRED_PRODUCT_MODEL_FILES.filter((required) => !keys.has(required.key)).map((required) => required.label);
    }

    function productModelFileNames(files = selectedProductModelFiles()) {
      if (files.length) return files.map((file) => file.name).join(", ");
      return (INITIAL_PRODUCT_MODEL.files || []).join(", ");
    }

    function productModelDefinitionFiles() {
      const selectedFromInputs = productModelInputItems().filter(item => item.file);
      if (selectedFromInputs.length) {
        return selectedFromInputs.map(item => item.file);
      }
      return selectedProductModelFiles().filter((file) => PRODUCT_MODEL_DEFINITION_FILE_KEYS.has(modelFileKey(file)));
    }

    function updateProductModelAcceptState() {
      const button = $("acceptProductModelBtn");
      if (!button) return;
      if (isProductModelAccepted()) {
        button.disabled = false;
        return;
      }
      const missing = missingProductModelFiles();
      button.disabled = missing.length > 0;
    }

    function updateProductModelSelectionStatus() {
      const files = selectedProductModelFiles();
      updateProductModelAcceptState();
      if (!files.length) {
        $("productModelStatus").textContent = t("model.required");
        return;
      }
      const missing = missingProductModelFiles();
      const selectedLabels = productModelInputItems()
        .filter(item => item.file)
        .map(item => `${item.label}: ${item.file.name}`);
      $("productModelStatus").innerHTML = missing.length
        ? `${esc(t("model.selected"))}: ${selectedLabels.map(item => esc(item)).join(", ")}<br>${esc(t("model.missingFiles"))}${esc(missing.join(", "))}`
        : `${esc(t("model.changed"))} ${esc(t("model.selected"))}: ${selectedLabels.map(item => esc(item)).join(", ")}`;
    }

    function isProductModelAccepted() {
      return pimModelAccepted && (Boolean(activeProductModelId) || productModelSignature() === acceptedProductModelSignature);
    }

    function updateWorkflowGate() {
      const modelReady = isProductModelAccepted();
      const productsReady = modelReady && Boolean(generatedProductsJobId);
      const mappingReady = modelReady && activeMode === "products" && Boolean(activeTable);
      if (modelReady && !activeProductModelFields.length) {
        $("productModelStatus").innerHTML = `<span class="ok">${esc(t("model.accepted"))}</span> ${esc(productModelFileNames())}`;
      }
      for (const element of document.querySelectorAll("#productsForm input, #productsForm button, #projectName, #saveProjectBtn, #generateEnrichedProductsMenuBtn")) {
        element.disabled = !modelReady;
      }
      if ($("loadProjectFile")) $("loadProjectFile").disabled = false;
      if (!modelReady && !$("productsFile").files[0]) {
        $("productsStatus").textContent = t("gate.locked");
      }
      updateProductModelAcceptState();
      updateWorkspaceChrome();
    }

    function resetAfterProductModelChange() {
      pimModelAccepted = false;
      acceptedProductModelSignature = "";
      productMapping = null;
      productMappingProfile = null;
      generatedProductsJobId = null;
      generatedProductsUrl = "";
      mainProductTable = null;
      supplementFileForMapping = null;
      supplementAnalysisTable = null;
      supplementMapping = null;
      supplementMappingProfile = null;
      supplementProductsPayload = null;
      supplementProductsUrl = "";
      activeTable = null;
      activeMode = null;
      activeProductModelFields = [];
      activeProductModelId = "";
      loadedProject = null;
      loadedProjectFiles = { productModelFiles: [], productsFile: null, typicalDataFile: null };
      enrichmentSession = { manual_entries: [], typical_sources: [], typical_matches: [] };
      typicalProductsForEnrichment = [];
      mappingWorkspaceTab = "mapping";
      for (const id of ["productsFile", "typicalFile", "loadProjectFile"]) {
        if ($(id)) $(id).value = "";
      }
      $("productsLinks").innerHTML = "";
      if ($("productsLinksInline")) $("productsLinksInline").innerHTML = "";
      $("projectLinks").innerHTML = "";
      $("report").innerHTML = "";
      $("reportEmpty").hidden = false;
      $("summary").textContent = t("report.idle");
      $("productsStatus").textContent = t("gate.locked");
      $("projectStatus").textContent = t("project.notSaved");
      if ($("typicalStatus")) $("typicalStatus").textContent = t("gate.locked");
      updateWorkflowGate();
    }

    function confirmProductModelChange() {
      if (!pimModelAccepted && !productMappingProfile && !activeTable) return true;
      return window.confirm(
        currentLang === "pl"
          ? "Zmiana modelu produktu rozpocznie nowy projekt i wyczyĹ›ci aktualne mapowanie oraz sesjÄ™ uzupeĹ‚niania. Zapisz obecny projekt przed zmianÄ…. Czy kontynuowaÄ‡?"
          : "Changing the product model starts a new project and clears the current mapping and enrichment session. Save the current project before changing it. Continue?"
      );
    }

    function enrichmentReady() {
      return activeMode === "products" && Boolean(activeTable);
    }

    function updateWorkspaceChrome() {
      const enrichmentMode = mappingWorkspaceTab === "enrichment";
      const hideForEnrichment = enrichmentMode && enrichmentReady();
      if ($("productModelPanel")) $("productModelPanel").hidden = hideForEnrichment;
      if ($("productsPanel")) $("productsPanel").hidden = hideForEnrichment;
      if ($("projectPanel")) $("projectPanel").hidden = false;
      for (const button of document.querySelectorAll("[data-workspace-tab='enrichment']")) {
        button.disabled = !enrichmentReady();
        button.title = enrichmentReady() ? "" : (currentLang === "pl" ? "Najpierw wczytaj i przeanalizuj plik produktĂłw." : "Load and analyze the products file first.");
      }
    }

    function setWorkspaceTab(tab) {
      if (tab === "enrichment" && !enrichmentReady()) {
        const target = $("mappingCheckTopResult");
        if (target) target.innerHTML = `<div class="warn">${esc(currentLang === "pl" ? "UzupeĹ‚nianie danych bÄ™dzie dostÄ™pne po analizie pliku produktĂłw." : "Data enrichment becomes available after analyzing the products file.")}</div>`;
        return;
      }
      mappingWorkspaceTab = tab || "mapping";
      for (const pane of document.querySelectorAll("[data-workspace-pane]")) {
        pane.hidden = pane.dataset.workspacePane !== mappingWorkspaceTab;
      }
      for (const tabButton of document.querySelectorAll("[data-workspace-tab]")) {
        tabButton.setAttribute("aria-pressed", String(tabButton.dataset.workspaceTab === mappingWorkspaceTab));
      }
      if ($("targetStructure")) $("targetStructure").hidden = mappingWorkspaceTab === "enrichment";
      updateWorkspaceChrome();
      renderEnrichmentSessionList();
      refreshEnrichmentCurrentProduct();
      renderProductPreview();
    }

    async function loadProductModelFields(files) {
      const body = new FormData();
      files.forEach((modelFile) => body.append("product_model_files", modelFile));
      const response = await fetch("/product-model", { method: "POST", body });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || (currentLang === "pl" ? "Nie udaĹ‚o siÄ™ odczytaÄ‡ modelu produktu." : "Could not read the product model."));
      activeProductModelFields = data.target_fields || [];
      activeProductModelId = data.model_id || "";
      if ($("productModelId")) $("productModelId").value = activeProductModelId;
      if ($("productsProductModelId")) $("productsProductModelId").value = activeProductModelId;
      if (!activeProductModelFields.length) {
        throw new Error(currentLang === "pl" ? "Model produktu nie zawiera pĂłl do mapowania." : "The product model does not contain mappable fields.");
      }
      return data;
    }

    async function acceptProductModel() {
      if (acceptingProductModel) return;
      acceptingProductModel = true;
      const acceptButton = $("acceptProductModelBtn");
      if (acceptButton) acceptButton.disabled = true;
      try {
        $("productModelStatus").textContent = currentLang === "pl" ? "Sprawdzam wybrane pliki modelu..." : "Checking selected model files...";
        const files = selectedProductModelFiles();
        if (!files.length) {
          pimModelAccepted = false;
          acceptedProductModelSignature = "";
          activeProductModelFields = [];
          activeProductModelId = "";
          $("productModelStatus").textContent = t("model.required");
          updateWorkflowGate();
          return;
        }
        const missing = missingProductModelFiles();
        if (missing.length) {
          pimModelAccepted = false;
          acceptedProductModelSignature = "";
          activeProductModelFields = [];
          activeProductModelId = "";
          $("productModelStatus").textContent = `${t("model.missingFiles")}${missing.join(", ")}`;
          updateWorkflowGate();
          return;
        }
        await loadProductModelFields(productModelDefinitionFiles());
        pimModelAccepted = true;
        acceptedProductModelSignature = productModelSignature(files);
        $("productModelStatus").innerHTML = `<span class="ok">${esc(t("model.accepted"))}</span> ${esc(productModelFileNames(files))}`;
        $("productsStatus").textContent = t("products.ready");
        if ($("typicalStatus")) $("typicalStatus").textContent = t("typical.optional");
        updateWorkflowGate();
        renderProductModelPreview();
      } catch (error) {
        pimModelAccepted = false;
        acceptedProductModelSignature = "";
        activeProductModelFields = [];
        activeProductModelId = "";
        $("productModelStatus").textContent = `${currentLang === "pl" ? "Nie udaĹ‚o siÄ™ zaakceptowaÄ‡ modelu: " : "Could not accept model: "}${error.message}`;
        updateWorkflowGate();
      } finally {
        acceptingProductModel = false;
        updateProductModelAcceptState();
      }
    }
    window.acceptProductModel = acceptProductModel;
    window.acceptProductModelSubmit = (event) => {
      event.preventDefault();
      acceptProductModel();
      return false;
    };

    function fieldGroups(targetFields) {
      const groups = {};
      for (const field of targetFields || []) {
        const group = field.group || "Model";
        if (!groups[group]) groups[group] = [];
        groups[group].push(field);
      }
      return groups;
    }

    function renderTargetStructure(targetFields, usage = {}) {
      const groups = fieldGroups(targetFields);
      return Object.entries(groups).map(([group, fields]) => {
        if (fields.some(fieldIsTypeSeries)) {
          return renderTypeSeriesStructure(group, fields, usage);
        }
        const rows = fields.map(field => {
          const item = usage[field.key] || { sources: [], values: [] };
          const mapped = Boolean(item.sources?.length || item.values?.length);
          const status = mapped ? t("model.mapped") : t("model.empty");
          const sourceTags = (item.sources || []).slice(0, 3).map(source => {
            const prefix = source.kind === "rule" ? t("model.sourceRule") : t("mapping.mappedColumn");
            return `<span class="mapped-source">${esc(prefix)}:<strong>${esc(source.label)}</strong></span>`;
          }).join("");
          const values = (item.values || []).slice(0, 3);
          const valueHtml = values.length ? `<div class="structure-value">${values.map(value => renderLinkedText(value, { limit: 220 })).join("<br>")}${(item.values || []).length > values.length ? `<br>${esc((item.values || []).length - values.length)} ${esc(t("model.moreValues"))}` : ""}</div>` : "";
          return `
            <div class="structure-field ${mapped ? "is-mapped" : "is-empty"}" data-target-field="${esc(field.key)}">
              <div>
                <div class="structure-field-label">${esc(cleanModelLabel(field.label))}${field.required ? " *" : ""}</div>
                <div class="structure-field-key">${esc(cleanModelLabel(field.key))}</div>
              </div>
              <div class="structure-field-options">${renderFieldValueMeta(field)}</div>
              <div class="structure-field-meta"><span class="mapping-state ${mapped ? "mapped" : ""}">${esc(status)}</span>${sourceTags ? `<div class="mapped-source-list">${sourceTags}</div>` : ""}</div>
              <div class="structure-field-value">${valueHtml}</div>
            </div>`;
        }).join("");
        return `<div class="structure-group"><strong>${esc(displayGroupName(group))}</strong>${rows}</div>`;
      }).join("");
    }

    function renderTypeSeriesStructure(group, fields, usage = {}) {
      if (activeMode === "products" && productMappingProfile) {
        return `<div class="structure-group type-series-structure">
          <strong>${esc(displayGroupName(group))}</strong>
          ${renderTypeSeriesPreviewTable(mappedRowsForPreview(), fields)}
        </div>`;
      }
      const rows = fields.map(field => {
        const item = usage[field.key] || { sources: [], values: [] };
        const mapped = Boolean(item.sources?.length || item.values?.length);
        const status = mapped ? t("model.mapped") : t("model.empty");
        const values = (item.values || []).slice(0, 3).join("; ");
        return `<tr>
          <td><strong>${esc(cleanModelLabel(field.label))}${field.required ? " *" : ""}</strong><br><span class="muted">${esc(cleanModelLabel(field.key))}</span></td>
          <td>${esc(field.unit || "-")}</td>
          <td><span class="mapping-state ${mapped ? "mapped" : ""}">${esc(status)}</span></td>
          <td>${values ? renderLinkedText(values, { limit: 400 }) : "-"}</td>
        </tr>`;
      }).join("");
      return `<div class="structure-group type-series-structure">
        <strong>${esc(displayGroupName(group))}</strong>
        <table>
          <thead><tr><th>${esc(t("preview.variantFeature"))}</th><th>${esc(t("preview.unit"))}</th><th>${esc(t("model.status"))}</th><th>${esc(t("preview.cleanedValue"))}</th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>`;
    }

    function targetFieldsForMode(mode) {
      if (!activeTable) return [];
      const mappingData = activeTable.product_mapping;
      return mappingData?.target_fields || [];
    }

    function targetFieldByKey(targetFields, key) {
      return (targetFields || []).find(field => field.key === key) || null;
    }

    function renderFieldValueMeta(field) {
      const options = field?.options || [];
      const kind = field.value_kind === "multi_choice" ? t("model.multiChoice") : t("model.singleChoice");
      const optionMeta = options.length
        ? `<span class="structure-status mapped">${esc(kind)}</span><span class="structure-status">${esc(options.length)} ${esc(t("model.options"))}</span>`
        : "";
      const unitMeta = field?.unit ? `<span class="structure-status">${esc(t("mapping.targetUnit"))}: ${esc(field.unit)}</span>` : "";
      if (!optionMeta && !unitMeta) return "";
      return `<div class="structure-field-meta">${optionMeta}${unitMeta}</div>`;
    }

    function normalizeChoice(value) {
      return String(value || "")
        .normalize("NFD")
        .replace(/[\\u0300-\\u036f]/g, "")
        .trim()
        .toLowerCase();
    }

    function choiceParts(value, field) {
      const text = displayCellValue(value).trim();
      if (!text) return [];
      if (field?.value_kind !== "multi_choice") return [text];
      return text.split(/[;\\n|,]+/).map(part => part.trim()).filter(Boolean);
    }

    function choicePreview(field, value, choiceMap = {}) {
      const options = field?.options || [];
      if (!options.length) return { matched: [], unmatched: [] };
      const optionsByLabel = new Map();
      for (const option of options) {
        for (const key of [option.label, option.value, option.id]) {
          const normalized = normalizeChoice(key);
          if (normalized) optionsByLabel.set(normalized, option);
        }
      }
      const mappedChoices = new Map();
      for (const [source, target] of Object.entries(choiceMap || {})) {
        const normalized = normalizeChoice(source);
        if (normalized) mappedChoices.set(normalized, target);
      }
      const matched = [];
      const unmatched = [];
      for (const part of choiceParts(value, field)) {
        const mappedPart = mappedChoices.get(normalizeChoice(part)) || part;
        const option = optionsByLabel.get(normalizeChoice(mappedPart));
        if (option) matched.push(option.label);
        else unmatched.push(part);
      }
      return { matched, unmatched };
    }

    function renderChoicePreview(field, value, choiceMap = {}) {
      const options = field?.options || [];
      if (!options.length) return "";
      const preview = choicePreview(field, value, choiceMap);
      const kind = field.value_kind === "multi_choice" ? t("model.multiChoice") : t("model.singleChoice");
      const matched = preview.matched.slice(0, 5).map(item => `<span class="pill">${esc(item)}</span>`).join("");
      const unmatched = preview.unmatched.slice(0, 5).map(item => `<span class="pill">${esc(item)}</span>`).join("");
      const optionHint = options.slice(0, 8).map(option => esc(option.label)).join(", ");
      return `<div class="helper"><strong>${esc(kind)}</strong>: ${esc(options.length)} ${esc(t("model.options"))}${optionHint ? ` (${optionHint})` : ""}</div>
        ${matched ? `<div class="helper">${esc(t("mapping.choiceMatched"))}: ${matched}</div>` : ""}
        ${unmatched ? `<div class="helper">${esc(t("mapping.choiceUnmatched"))}: ${unmatched}</div>` : ""}`;
    }

    function choiceOptionText(option) {
      return String(option?.label || option?.value || option?.id || "");
    }

    function inferredChoiceTarget(field, sourceValue) {
      const normalized = normalizeChoice(sourceValue);
      if (!normalized) return "";
      for (const option of field?.options || []) {
        for (const key of [option.label, option.value, option.id]) {
          if (normalizeChoice(key) === normalized) return choiceOptionText(option);
        }
      }
      return "";
    }

    function choiceOptionSelect(field, selected) {
      const selectedNormalized = normalizeChoice(selected);
      const options = (field?.options || []).map(option => {
        const value = choiceOptionText(option);
        const matches = selectedNormalized && [option.label, option.value, option.id].some(key => normalizeChoice(key) === selectedNormalized);
        return `<option value="${esc(value)}"${matches ? " selected" : ""}>${esc(value)}</option>`;
      }).join("");
      return `<option value="">${esc(t("mapping.choiceDoNotImport"))}</option>${options}`;
    }

    function choiceOptionPayload(option) {
      const payload = {
        id: option?.id ?? null,
        label: option?.label ?? "",
        value: option?.value ?? option?.label ?? ""
      };
      return JSON.stringify(payload);
    }

    function choiceOptionMatchesValue(option, value, field) {
      const candidates = [option?.label, option?.value, option?.id].map(normalizeChoice).filter(Boolean);
      if (Array.isArray(value)) {
        return value.some(item => choiceOptionMatchesValue(option, item, field));
      }
      if (value && typeof value === "object") {
        return [value.label, value.value, value.id].some(item => candidates.includes(normalizeChoice(item)));
      }
      const parts = field?.value_kind === "multi_choice" ? choiceParts(value, field) : [displayCellValue(value)];
      return parts.some(part => candidates.includes(normalizeChoice(part)));
    }

    function manualChoiceControl(targetPath, value, field, extraAttrs = "") {
      const options = field?.options || [];
      if (!options.length) return "";
      const size = Math.min(Math.max(options.length, 3), 8);
      const optionHtml = options.map(option => {
        const optionValue = choiceOptionPayload(option);
        return `<option value="${esc(optionValue)}"${choiceOptionMatchesValue(option, value, field) ? " selected" : ""}>${esc(choiceOptionText(option))}</option>`;
      }).join("");
      if (field.value_kind === "multi_choice") {
        return `<select class="editable-value-input" data-inline-manual-target="${esc(targetPath)}" data-inline-manual-kind="multi_choice" data-inline-manual-dirty="0" onchange="this.dataset.inlineManualDirty='1'" ${extraAttrs} multiple size="${esc(size)}">${optionHtml}</select>`;
      }
      return `<select class="editable-value-input" data-inline-manual-target="${esc(targetPath)}" data-inline-manual-kind="single_choice" data-inline-manual-dirty="0" onchange="this.dataset.inlineManualDirty='1'" ${extraAttrs}>
        <option value="">${esc(t("mapping.choiceDoNotImport"))}</option>
        ${optionHtml}
      </select>`;
    }

    function distinctChoiceValues(table, column, field, cleanup = {}, limit = 60) {
      const values = [];
      const seen = new Set();
      const addValue = rawValue => {
        const cleaned = applyCleanup(rawValue, cleanup);
        for (const part of choiceParts(cleaned, field)) {
          const key = normalizeChoice(part);
          if (!key || seen.has(key)) continue;
          seen.add(key);
          values.push(part);
          if (values.length >= limit) return;
        }
      };
      for (const row of table?.sample_rows || []) {
        if (values.length >= limit) break;
        addValue(row?.[column]);
      }
      for (const sample of table?.column_samples?.[column] || []) {
        if (values.length >= limit) break;
        addValue(sample?.value);
      }
      return values;
    }

    function renderChoiceMapEditor(field, table, sourceColumn, choiceMap = {}, cleanup = {}) {
      const options = field?.options || [];
      const hiddenValue = esc(formatChoiceMap(choiceMap || {}));
      if (!options.length) return `<textarea data-cleanup="choiceMap" hidden>${hiddenValue}</textarea>`;
      const optionPills = options
        .map(option => `<span class="pill">${esc(choiceOptionText(option))}</span>`)
        .join("");
      const values = sourceColumn ? distinctChoiceValues(table, sourceColumn, field, cleanup) : [];
      const rows = values.map(value => {
        const selected = choiceMap?.[value] || inferredChoiceTarget(field, value);
        return `<tr>
          <td class="choice-map-value">${renderLinkedText(value, { limit: 500 })}</td>
          <td>
            <select data-choice-map-target data-choice-source="${esc(value)}">
              ${choiceOptionSelect(field, selected)}
            </select>
          </td>
        </tr>`;
      }).join("");
      return `<div class="choice-map-editor" data-choice-map-editor>
        <textarea data-cleanup="choiceMap" hidden>${hiddenValue}</textarea>
        <label>${esc(t("mapping.choiceMap"))}</label>
        <div class="helper">${esc(t("mapping.choiceMapHelp"))}</div>
        <div class="helper"><strong>${esc(t("mapping.choiceOptions"))}</strong></div>
        <div class="choice-map-options">${optionPills}</div>
        ${sourceColumn
          ? `<table class="choice-map-table">
              <thead><tr><th>${esc(t("mapping.choiceClientValue"))}</th><th>${esc(t("mapping.choicePimOption"))}</th></tr></thead>
              <tbody>${rows || `<tr><td colspan="2">${esc(t("mapping.noSource"))}</td></tr>`}</tbody>
            </table>`
          : `<div class="helper">${esc(t("mapping.choicePickSource"))}</div>`}
      </div>`;
    }

    function productFieldsForEnrichment() {
      return targetFieldsForMode("products").filter(field => field && field.key && !fieldIsTypeSeries(field));
    }

    function allFieldsForEnrichment() {
      return targetFieldsForMode("products").filter(field => field && field.key);
    }

    function targetFieldSelectOptions(selected = "") {
      return productFieldsForEnrichment().map(field =>
        `<option value="${esc(field.key)}"${field.key === selected ? " selected" : ""}>${esc(displayGroupName(field.group || "Model"))} / ${esc(cleanModelLabel(field.label || field.key))}</option>`
      ).join("");
    }

    function allTargetFieldSelectOptions(selected = "") {
      const noneOption = `<option value=""${selected ? "" : " selected"}>${esc(currentLang === "pl" ? "brak cechy" : "no feature")}</option>`;
      return noneOption + allFieldsForEnrichment().map(field =>
        `<option value="${esc(field.key)}"${field.key === selected ? " selected" : ""}>${esc(displayGroupName(field.group || "Model"))} / ${esc(cleanModelLabel(field.label || field.key))}</option>`
      ).join("");
    }

    function currentProductKeyForEnrichment() {
      const entry = currentPreviewEntry();
      return productKeyForEnrichmentEntry(entry, productPreviewIndex);
    }

    function productKeyForEnrichmentEntry(entry, index) {
      const mapped = mappedObjectForPreview(entry?.row || {}, entry?.context || {});
      return String(mapped["product.code.value"] || mapped["product.name.value"] || productLabelForPreview(entry || {}, index)).trim();
    }

    function entriesForTypicalScope(scope) {
      const rows = mappedRowsForPreview();
      if (!rows.length) return [{ entry: currentPreviewEntry(), index: productPreviewIndex }];
      let targets = [];
      if (scope === "all_products") {
        targets = rows.map((entry, index) => ({ entry, index }));
      } else if (scope === "selected_products") {
        const selected = new Set(Array.from(document.querySelectorAll("[data-typical-target-product]:checked")).map(input => Number.parseInt(input.value, 10)).filter(index => Number.isFinite(index)));
        if (!selected.size) return [{ entry: currentPreviewEntry(), index: productPreviewIndex }];
        targets = rows
          .map((entry, index) => ({ entry, index }))
          .filter(item => selected.has(item.index));
      } else if (scope === "field_value_filter") {
        targets = rows.map((entry, index) => ({ entry, index }));
      } else {
        targets = [{ entry: currentPreviewEntry(), index: productPreviewIndex }];
      }
      if ($("enableEnrichmentFilter")?.checked || scope === "field_value_filter") {
        const targetPath = $("enrichmentFilterField")?.value || "";
        const expected = normalizeChoice($("enrichmentFilterValue")?.value || "");
        if (!targetPath || !expected) return targets;
        return targets
          .map(item => ({ ...item, mapped: mappedObjectForPreview(item.entry.row || {}, item.entry.context || {}) }))
          .filter(item => normalizeChoice(item.mapped[targetPath] || "") === expected)
          .map(({ entry, index }) => ({ entry, index }));
      }
      return targets;
    }

    function productOptionsForEnrichmentTargets() {
      const rows = mappedRowsForPreview();
      return rows.map((entry, index) =>
        `<option value="${esc(index)}"${index === productPreviewIndex ? " selected" : ""}>${esc(productLabelForPreview(entry, index))}</option>`
      ).join("");
    }

    function productCheckboxesForEnrichmentTargets() {
      const rows = mappedRowsForPreview();
      return rows.map((entry, index) =>
        `<label><input type="checkbox" data-typical-target-product value="${esc(index)}"${index === productPreviewIndex ? " checked" : ""}> <span>${esc(productLabelForPreview(entry, index))}</span></label>`
      ).join("");
    }

    function valuesForProductTarget(targetPath, limit = 80) {
      const values = [];
      const seen = new Set();
      for (const entry of mappedRowsForPreview()) {
        const mapped = mappedObjectForPreview(entry.row || {}, entry.context || {});
        const value = displayCellValue(mapped[targetPath] || "").trim();
        if (!value || seen.has(value)) continue;
        seen.add(value);
        values.push(value);
        if (values.length >= limit) break;
      }
      return values;
    }

    function productTargetValueOptions(targetPath) {
      return `<option value="">${esc(currentLang === "pl" ? "wybierz wartoĹ›Ä‡" : "choose value")}</option>` + valuesForProductTarget(targetPath).map(value => `<option value="${esc(value)}">${esc(value)}</option>`).join("");
    }

    function mainProductValueForPath(entry, targetPath) {
      if (!entry || !targetPath) return "";
      const mapped = mappedObjectForPreview(entry.row || {}, entry.context || {});
      return displayCellValue(mapped[targetPath] || "").trim();
    }

    function normalizeEnrichmentSession(value) {
      const session = value && typeof value === "object" ? value : {};
      return {
        manual_entries: Array.isArray(session.manual_entries) ? session.manual_entries : [],
        typical_sources: Array.isArray(session.typical_sources) ? session.typical_sources : [],
        typical_matches: Array.isArray(session.typical_matches) ? session.typical_matches : [],
        typical_attribute_map: session.typical_attribute_map && typeof session.typical_attribute_map === "object" ? session.typical_attribute_map : {},
        typical_source_model: session.typical_source_model && typeof session.typical_source_model === "object" ? session.typical_source_model : {},
        typical_source_mode: session.typical_source_mode || "raw_file"
      };
    }

    function pimProductAttributes(product) {
      if (Array.isArray(product?.productAttributes)) return product.productAttributes;
      if (Array.isArray(product?.ProductAttributes)) return product.ProductAttributes;
      const versions = Array.isArray(product?.dataVersions)
        ? product.dataVersions
        : (Array.isArray(product?.DataVersions) ? product.DataVersions : []);
      return versions.flatMap(version => {
        if (Array.isArray(version?.productAttributes)) return version.productAttributes;
        if (Array.isArray(version?.ProductAttributes)) return version.ProductAttributes;
        return [];
      });
    }

    function pimAttrValue(attr) {
      for (const key of ["varcharValue", "TextValue", "NumberValue", "IntValue", "IntValue2", "BooleanValue"]) {
        const value = attr?.[key];
        if (value !== undefined && value !== null && value !== "") return value;
      }
      return "";
    }

    function normalizeMatchKey(value) {
      return String(value || "").normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").trim().toLowerCase();
    }

    function pimProductIdentity(product) {
      const attrs = pimProductAttributes(product);
      const sourceNameIds = typicalSourceAttributes
        .filter(attr => normalizeMatchKey(attr.DispName || attr.AttributeName) === normalizeMatchKey("Nazwa") || normalizeMatchKey(attr.AttributeName) === "name")
        .map(attr => Number(attr.Id ?? attr.ID ?? attr.AttributeId));
      const sourceCodeIds = typicalSourceAttributes
        .filter(attr => ["id", "kod", "pim id"].includes(normalizeMatchKey(attr.DispName || attr.AttributeName)))
        .map(attr => Number(attr.Id ?? attr.ID ?? attr.AttributeId));
      const name = attrs.find(attr => Number(attr.AttributeId) === 225)
        || attrs.find(attr => sourceNameIds.includes(Number(attr.AttributeId)));
      const code = attrs.find(attr => Number(attr.AttributeId) === 226)
        || attrs.find(attr => sourceCodeIds.includes(Number(attr.AttributeId)));
      const codeValue = pimAttrValue(code);
      const nameValue = pimAttrValue(name);
      const key = normalizeMatchKey(codeValue || nameValue || product?.Id);
      return {
        key,
        label: String(nameValue || codeValue || product?.Id || key || "Produkt typowy"),
        code: String(codeValue || "")
      };
    }

    function modelAttributeIdsForCheck() {
      const ids = new Set([225, 226, 228, 229, 230, 231, 276]);
      for (const field of targetFieldsForMode("products") || []) {
        const attributeId = attributeIdFromFieldKey(field.key);
        if (attributeId) ids.add(Number(attributeId));
      }
      return ids;
    }

    function modelFieldForAttributeId(attributeId) {
      const key = `pim.attribute.${attributeId}.value`;
      const sotKeyById = {
        277: "type_series[].thickness.value",
        278: "type_series[].lambda_value.value",
        279: "type_series[].density.value",
        295: "type_series[].vapor_permeability_mu.value"
      };
      return targetFieldsForMode("products").find(field => field.key === key || field.key === sotKeyById[Number(attributeId)]) || null;
    }

    function attributeIdFromFieldKey(key) {
      const match = String(key || "").match(/^pim[.]attribute[.](\\d+)[.]value$/);
      if (match) return Number(match[1]);
      const coreIdByKey = {
        "product.name.value": 225,
        "product.code.value": 226,
        "product.category[].value": 230,
        "product.unit.value": 231
      };
      if (coreIdByKey[String(key || "")]) return coreIdByKey[String(key || "")];
      const sotIdByKey = {
        "type_series[].thickness.value": 277,
        "type_series[].lambda_value.value": 278,
        "type_series[].density.value": 279,
        "type_series[].vapor_permeability_mu.value": 295
      };
      return sotIdByKey[String(key || "")] || null;
    }

    function parentAttributeIdForTargetPath(targetPath) {
      if (String(targetPath || "").startsWith("type_series[]")) return 276;
      return 0;
    }

    function sourceAttributeById(attributeId) {
      return typicalSourceAttributes.find(attr => Number(attr.Id ?? attr.ID ?? attr.AttributeId) === Number(attributeId)) || null;
    }

    function sourceAttributeLabel(attributeId) {
      const source = sourceAttributeById(attributeId);
      const current = modelFieldForAttributeId(attributeId);
      return String(source?.DispName || source?.AttributeName || current?.label || `AttributeId ${attributeId}`);
    }

    function parseAttributesPayload(payload) {
      if (Array.isArray(payload)) return payload;
      if (Array.isArray(payload?.attributes)) return payload.attributes;
      if (Array.isArray(payload?.Attributes)) return payload.Attributes;
      if (Array.isArray(payload?.productAttributes)) return payload.productAttributes;
      return [];
    }

    async function loadTypicalSourceModelFile(kind, file) {
      if (!file) return;
      try {
        const payload = JSON.parse(await file.text());
        if (kind === "attributes") {
          typicalSourceAttributes = parseAttributesPayload(payload);
          enrichmentSession.typical_source_model = {
            ...(enrichmentSession.typical_source_model || {}),
            attributes_file: file.name,
            attributes_count: typicalSourceAttributes.length
          };
        } else {
          enrichmentSession.typical_source_model = {
            ...(enrichmentSession.typical_source_model || {}),
            models_file: file.name
          };
        }
        if ($("typicalSourceModelStatus")) $("typicalSourceModelStatus").textContent = t("enrichment.sourceModelLoaded");
        renderTypicalSourceAttributeMap();
        refreshTypicalControls();
        refreshTypicalSourceFileStatus();
      } catch (error) {
        if ($("typicalSourceModelStatus")) $("typicalSourceModelStatus").textContent = error.message || t("enrichment.typicalInvalid");
        refreshTypicalSourceFileStatus();
      }
    }

    function uniqueTypicalSourceAttributes() {
      const byKey = new Map();
      for (const product of typicalProductsPayloadForEnrichment || []) {
        for (const attr of pimProductAttributes(product)) {
          if (pimAttrValue(attr) === "") continue;
          const attributeId = Number(attr.AttributeId);
          if (!Number.isFinite(attributeId)) continue;
          const parentId = Number(attr.ParentAttributeId || 0);
          const key = `${attributeId}:${parentId}`;
          if (!byKey.has(key)) byKey.set(key, { attributeId, parentId, count: 0, sample: pimAttrValue(attr) });
          byKey.get(key).count += 1;
        }
      }
      return Array.from(byKey.values()).sort((a, b) => sourceAttributeLabel(a.attributeId).localeCompare(sourceAttributeLabel(b.attributeId), currentLang));
    }

    function targetFieldOptionsForSourceAttribute(source) {
      const sourceLabel = sourceAttributeLabel(source.attributeId).toLowerCase();
      return [`<option value="">${esc(currentLang === "pl" ? "Nie uĹĽywaj" : "Do not use")}</option>`]
        .concat((targetFieldsForMode("products") || []).filter(field => field?.key).map(field => {
          const targetId = attributeIdFromFieldKey(field.key);
          const sameId = targetId && Number(targetId) === Number(source.attributeId);
          const sameLabel = cleanModelLabel(field.label || "").toLowerCase() === sourceLabel;
          const current = enrichmentSession.typical_attribute_map?.[`${source.attributeId}:${source.parentId}`]?.target_path;
          const selected = current ? current === field.key : (sameId || sameLabel);
          return `<option value="${esc(field.key)}"${selected ? " selected" : ""}>${esc(displayGroupName(field.group || "Model"))} / ${esc(cleanModelLabel(field.label || field.key))}</option>`;
        }))
        .join("");
    }

    function renderTypicalSourceAttributeMap() {
      const target = $("typicalSourceAttributeMap");
      if (!target) return;
      const sources = uniqueTypicalSourceAttributes();
      if (!sources.length) {
        target.innerHTML = `<div class="helper">${esc(t("enrichment.noAttributeMap"))}</div>`;
        return;
      }
      target.innerHTML = `<h4>${esc(t("enrichment.attributeMap"))}</h4>
        <table>
          <thead><tr><th>${esc(t("enrichment.sourceAttribute"))}</th><th>${esc(t("enrichment.targetAttribute"))}</th><th>${esc(t("preview.cleanedValue"))}</th></tr></thead>
          <tbody>${sources.map(source => `<tr>
            <td><strong>${esc(sourceAttributeLabel(source.attributeId))}</strong><br><span class="muted">AttributeId ${esc(source.attributeId)}</span></td>
            <td><select data-typical-attribute-map="${esc(source.attributeId)}:${esc(source.parentId)}">${targetFieldOptionsForSourceAttribute(source)}</select></td>
            <td>${renderLinkedText(source.sample, { limit: 240 })}</td>
          </tr>`).join("")}</tbody>
        </table>`;
      for (const select of target.querySelectorAll("[data-typical-attribute-map]")) {
        select.onchange = () => collectTypicalAttributeMap();
      }
      collectTypicalAttributeMap();
    }

    function collectTypicalAttributeMap() {
      const map = {};
      for (const select of document.querySelectorAll("[data-typical-attribute-map]")) {
        const targetPath = select.value || "";
        if (!targetPath) continue;
        const targetId = attributeIdFromFieldKey(targetPath);
        if (!targetId) continue;
        map[select.dataset.typicalAttributeMap] = {
          target_path: targetPath,
          attribute_id: targetId,
          parent_attribute_id: parentAttributeIdForTargetPath(targetPath)
        };
      }
      enrichmentSession.typical_attribute_map = map;
    }

    function typicalAttributeModelPath(attr) {
      const attributeId = Number(attr?.AttributeId);
      const field = modelFieldForAttributeId(attributeId);
      if (field) return field.key;
      const source = sourceAttributeById(attributeId);
      if (source) return `source.attribute.${attributeId}.value`;
      const corePaths = {
        225: "product.name.value",
        226: "product.code.value",
        230: "product.category[].value",
        231: "product.unit.value",
        276: "type_series"
      };
      return corePaths[attributeId] || `pim.attribute.${attributeId}.value`;
    }

    function typicalAttributeLabel(attr) {
      const attributeId = Number(attr?.AttributeId);
      const field = modelFieldForAttributeId(attributeId);
      if (field) return cleanModelLabel(field.label || field.key);
      const source = sourceAttributeById(attributeId);
      if (source) return String(source.DispName || source.AttributeName || `AttributeId ${attributeId}`);
      const coreNames = {
        225: currentLang === "pl" ? "Nazwa" : "Name",
        226: "ID",
        230: currentLang === "pl" ? "Kategoria" : "Category",
        231: currentLang === "pl" ? "Jednostka" : "Unit",
        276: currentLang === "pl" ? "Typoszereg" : "Type series"
      };
      return coreNames[attributeId] || (currentLang === "pl" ? "Cecha spoza aktualnego modelu" : "Feature outside the active model");
    }

    function typicalAttributeKey(attr) {
      return `${attr?.AttributeId || ""}:${attr?.ParentAttributeId || 0}:${attr?.RowI || 0}`;
    }

    function typicalAttributeIsTypeSeries(attr) {
      return targetPathIsTypeSeries(typicalAttributeModelPath(attr));
    }

    function enrichmentFileOptionsHtml() {
      const sources = enrichmentSession.typical_sources || [];
      if (!sources.length) {
        return `<option value="">${esc(t("enrichment.noTypical"))}</option>`;
      }
      return sources.map((source, index) =>
        `<option value="${esc(index)}">${esc(source.name || t("typical.file"))} - ${esc(source.products_count || 0)} ${esc(t("enrichment.productsFound"))}</option>`
      ).join("");
    }

    function fileStatusHtml(label, file) {
      return `<div class="file-status"><strong>${esc(label)}</strong><span class="${file ? "ok" : "muted"}">${file ? `${esc(t("enrichment.loaded"))}: ${esc(file.name)}` : esc(t("enrichment.notLoaded"))}</span></div>`;
    }

    function typicalSourceFilesStatusHtml() {
      return `<div class="file-status-list">
        ${fileStatusHtml(t("enrichment.mappedProductsFile"), fileForInput("typicalFile"))}
        ${fileStatusHtml("productsModels.json", $("typicalModelsFileVisible")?.files?.[0] || $("typicalModelsFile")?.files?.[0] || null)}
        ${fileStatusHtml("productsAttributes.json", $("typicalAttributesFileVisible")?.files?.[0] || $("typicalAttributesFile")?.files?.[0] || null)}
      </div>`;
    }

    function typicalRawFileStatusHtml() {
      return `<div class="file-status-list">
        ${fileStatusHtml(t("enrichment.rawFile"), $("typicalRawFileVisible")?.files?.[0] || supplementFileForMapping || $("typicalRawFile")?.files?.[0] || loadedProjectFiles.typicalDataFile || null)}
      </div>`;
    }

    function refreshTypicalSourceFileStatus() {
      const mappedStatus = $("typicalMappedFilesStatus");
      if (mappedStatus) mappedStatus.innerHTML = typicalSourceFilesStatusHtml();
      const rawStatus = $("typicalRawFileStatus");
      if (rawStatus) rawStatus.innerHTML = typicalRawFileStatusHtml();
    }

    function updateTypicalSourceModeUi() {
      for (const panel of document.querySelectorAll("[data-source-mode-panel]")) {
        panel.hidden = panel.dataset.sourceModePanel !== typicalSourceMode;
      }
      const select = $("typicalSourceMode");
      if (select) select.value = typicalSourceMode;
      refreshTypicalSourceFileStatus();
    }

    function selectedTypicalProductMetas() {
      return typicalProductMetasForAttributeKeys(selectedSupplementAttributeKeys());
    }

    function selectedTypicalSourceMeta() {
      const selectedKey = $("typicalSourceProduct")?.value || "";
      return typicalProductsForEnrichment.find(product => (product.ui_key || product.key) === selectedKey)
        || typicalProductsForEnrichment[0]
        || null;
    }

    function selectedSupplementAttributeKeys() {
      const select = $("supplementAttributeSelect");
      return Array.from(select?.selectedOptions || [])
        .map(option => option.value)
        .filter(Boolean);
    }

    function typicalProductMetasForAttributeKeys(attributeKeys) {
      const keys = new Set((attributeKeys || []).map(key => String(key).split("|")[0]).filter(Boolean));
      return Array.from(keys)
        .map(key => typicalProductsForEnrichment.find(product => product.ui_key === key || product.key === key))
        .filter(Boolean);
    }

    function supplementMappedAttributeKeys() {
      const keys = new Set();
      for (const item of Object.values(supplementMappingProfile || {})) {
        if (!item || !item.target_path || item.target_path === "ignore") continue;
        const attributeId = attributeIdFromFieldKey(item.target_path);
        if (!attributeId) continue;
        keys.add(`${attributeId}:${parentAttributeIdForTargetPath(item.target_path)}`);
      }
      return keys;
    }

    function supplementMappedTargetPaths() {
      const paths = new Set();
      for (const item of Object.values(supplementMappingProfile || {})) {
        if (!item || !item.target_path || item.target_path === "ignore") continue;
        paths.add(item.target_path);
      }
      return paths;
    }

    function attributeIsFromSupplementMapping(attr) {
      const mappedKeys = supplementMappedAttributeKeys();
      const mappedPaths = supplementMappedTargetPaths();
      if (!mappedKeys.size && !mappedPaths.size) return true;
      const modelPath = typicalAttributeModelPath(attr);
      if (mappedPaths.has(modelPath)) return true;
      return mappedKeys.has(`${Number(attr?.AttributeId)}:${Number(attr?.ParentAttributeId || 0)}`);
    }

    function typicalProductValueForPath(meta, targetPath) {
      if (!meta || !targetPath) return "";
      const product = typicalProductsPayloadForEnrichment[meta.index];
      for (const attr of pimProductAttributes(product)) {
        if (!attributeIsFromSupplementMapping(attr)) continue;
        if (typicalAttributeModelPath(attr) !== targetPath) continue;
        const value = displayCellValue(pimAttrValue(attr) || "").trim();
        if (value) return value;
      }
      return "";
    }

    function typicalAttributeKeysForPaths(meta, targetPaths) {
      const paths = new Set(targetPaths || []);
      if (!meta || !paths.size) return [];
      const product = typicalProductsPayloadForEnrichment[meta.index];
      const keys = [];
      for (const attr of pimProductAttributes(product)) {
        if (!attributeIsFromSupplementMapping(attr) || pimAttrValue(attr) === "") continue;
        if (paths.has(typicalAttributeModelPath(attr))) keys.push(typicalAttributeKey(attr));
      }
      return keys;
    }

    function supplementMatchFieldOptions(selected = "") {
      const fieldsByPath = new Map();
      for (const meta of typicalProductsForEnrichment) {
        const product = typicalProductsPayloadForEnrichment[meta.index];
        for (const attr of pimProductAttributes(product)) {
          if (!attributeIsFromSupplementMapping(attr) || pimAttrValue(attr) === "") continue;
          const path = typicalAttributeModelPath(attr);
          if (!fieldsByPath.has(path)) fieldsByPath.set(path, typicalAttributeLabel(attr));
        }
      }
      const noneOption = `<option value=""${selected ? "" : " selected"}>${esc(currentLang === "pl" ? "wybierz cechÄ™" : "choose feature")}</option>`;
      return noneOption + Array.from(fieldsByPath.entries()).map(([path, label]) =>
        `<option value="${esc(path)}"${path === selected ? " selected" : ""}>${esc(cleanModelLabel(label || path))}</option>`
      ).join("");
    }

    function renderTypicalAttributePicker() {
      const metas = selectedTypicalProductMetas();
      if (!metas.length) return `<div class="helper">${esc(t("enrichment.noTypicalProducts"))}</div>`;
      const rows = metas.flatMap(meta => {
        const product = typicalProductsPayloadForEnrichment[meta.index];
        return pimProductAttributes(product)
          .filter(attr => pimAttrValue(attr) !== "")
          .filter(attributeIsFromSupplementMapping)
          .slice(0, 120)
          .map(attr => {
            const attrKey = typicalAttributeKey(attr);
            const key = `${meta.ui_key || meta.key}|${attrKey}`;
            return `<tr>
              <td><input type="checkbox" data-typical-attr="${esc(key)}" checked></td>
              <td>${esc(meta.label)}${meta.code ? `<br><span class="muted">${esc(meta.code)}</span>` : ""}</td>
              <td>${esc(typicalAttributeLabel(attr))}<br><span class="muted">${esc(typicalAttributeModelPath(attr))}</span><br><span class="muted">AttributeId ${esc(attr.AttributeId)}${attr.RowI ? ` / Row ${esc(attr.RowI)}` : ""}</span></td>
              <td>${renderLinkedText(pimAttrValue(attr), { limit: 360 })}</td>
            </tr>`;
          });
      }).join("");
      return `<table>
        <thead><tr><th></th><th>${esc(t("enrichment.typicalProduct"))}</th><th>${esc(t("preview.field"))}</th><th>${esc(t("preview.cleanedValue"))}</th></tr></thead>
        <tbody>${rows || `<tr><td colspan="4">${esc(t("enrichment.noTypicalProducts"))}</td></tr>`}</tbody>
      </table>`;
    }

    function supplementAttributeOptions() {
      const scope = $("typicalMatchScope")?.value || "selected_products";
      if (scope === "match_by_feature") {
        const fieldsByPath = new Map();
        for (const meta of typicalProductsForEnrichment) {
          const product = typicalProductsPayloadForEnrichment[meta.index];
          for (const attr of pimProductAttributes(product)) {
            if (pimAttrValue(attr) === "" || !attributeIsFromSupplementMapping(attr)) continue;
            const path = typicalAttributeModelPath(attr);
            if (!fieldsByPath.has(path)) {
              fieldsByPath.set(path, `${typicalAttributeLabel(attr)}${typicalAttributeIsTypeSeries(attr) ? " (type series)" : ""}`);
            }
          }
        }
        return Array.from(fieldsByPath.entries()).map(([path, label]) =>
          `<option value="path|${esc(path)}">${esc(label)}</option>`
        ).join("");
      }
      const options = [];
      const meta = selectedTypicalSourceMeta();
      const product = meta ? typicalProductsPayloadForEnrichment[meta.index] : null;
      for (const attr of pimProductAttributes(product)) {
        if (pimAttrValue(attr) === "" || !attributeIsFromSupplementMapping(attr)) continue;
        const attrKey = typicalAttributeKey(attr);
        const key = `${meta.ui_key || meta.key}|${attrKey}`;
        const label = `${typicalAttributeLabel(attr)}${typicalAttributeIsTypeSeries(attr) ? " (type series)" : ""}`;
        options.push(`<option value="${esc(key)}">${esc(label)}</option>`);
      }
      return options.join("");
    }

    function typicalModelCheck(products) {
      const modelIds = modelAttributeIdsForCheck();
      let known = 0;
      let unknown = 0;
      for (const product of products || []) {
        for (const attr of pimProductAttributes(product)) {
          if (modelIds.has(Number(attr.AttributeId))) known += 1;
          else unknown += 1;
        }
      }
      return { known, unknown, ok: unknown === 0 || known >= unknown };
    }

    function validateTypicalProductsPayload(payload) {
      const products = Array.isArray(payload)
        ? payload
        : (Array.isArray(payload?.products) ? payload.products : (Array.isArray(payload?.Products) ? payload.Products : []));
      if (!products.length) return { ok: false, products: [], attributesCount: 0 };
      let attributesCount = 0;
      let validProducts = 0;
      for (const product of products) {
        const attrs = pimProductAttributes(product);
        if (attrs.length) {
          validProducts += 1;
          attributesCount += attrs.length;
        }
      }
      return { ok: validProducts > 0, products, productsCount: validProducts, attributesCount };
    }

    function acceptSupplementProductsPayload(payload, sourceInfo = {}) {
      const validation = validateTypicalProductsPayload(payload);
      if (!validation.ok) {
        throw new Error(t("enrichment.typicalInvalid"));
      }
      const offset = typicalProductsPayloadForEnrichment.length;
      const sourceIndex = (enrichmentSession.typical_sources || []).length;
      typicalProductsPayloadForEnrichment = typicalProductsPayloadForEnrichment.concat(validation.products);
      typicalProductsForEnrichment = typicalProductsForEnrichment.concat(validation.products.map((product, index) => ({
        ...pimProductIdentity(product),
        ui_key: `${sourceIndex}:${index}:${pimProductIdentity(product).key}`,
        index: offset + index,
        source_index: sourceIndex,
        source_name: sourceInfo.name || t("enrichment.supplementFile"),
        attributes_count: pimProductAttributes(product).length
      })).filter(product => product.key));
      const modelCheck = typicalModelCheck(validation.products);
      enrichmentSession.typical_source_mode = "raw_file";
      enrichmentSession.typical_sources = (enrichmentSession.typical_sources || []).filter(source => !source.mapping_required).concat([{
        name: sourceInfo.name || t("enrichment.supplementFile"),
        size: sourceInfo.size || 0,
        products_count: validation.productsCount,
        attributes_count: validation.attributesCount,
        model_check: modelCheck,
        source: sourceInfo.source || "mapped_supplement_file",
        mapping_required: false,
        products_url: sourceInfo.productsUrl || "",
        mapping_profile: sourceInfo.mappingProfile || null,
        loaded_at: new Date().toISOString()
      }]);
      if ($("typicalStatus")) $("typicalStatus").textContent = `${t("enrichment.supplementReady")} ${validation.productsCount} ${t("enrichment.productsFound")}, ${validation.attributesCount} ${t("enrichment.attributesFound")}.`;
      refreshTypicalControls();
      updateTypicalSourceModeUi();
      renderTypicalSourceAttributeMap();
      renderEnrichmentSessionList();
    }

    async function loadTypicalDataFile(file) {
      if (!file) {
        loadedProjectFiles.typicalDataFile = null;
        enrichmentSession.typical_sources = [];
        if ($("typicalStatus")) $("typicalStatus").textContent = t("typical.optional");
        refreshTypicalSourceFileStatus();
        renderEnrichmentSessionList();
        return;
      }
      try {
        const payload = JSON.parse(await file.text());
        const validation = validateTypicalProductsPayload(payload);
        if (!validation.ok) {
          throw new Error(currentLang === "pl"
            ? "Nie rozpoznano produktĂłw i cech w pliku danych typowych. Oczekiwany jest JSON z products[].dataVersions[].productAttributes albo products[].productAttributes."
            : "No products and features were recognized in the typical-data file. Expected JSON with products[].dataVersions[].productAttributes or products[].productAttributes.");
        }
        typicalProductsPayloadForEnrichment = validation.products;
        typicalProductsForEnrichment = validation.products.map((product, index) => ({
          ...pimProductIdentity(product),
          index,
          attributes_count: pimProductAttributes(product).length
        })).filter(product => product.key);
        const modelCheck = typicalModelCheck(validation.products);
        loadedProjectFiles.typicalDataFile = file;
        typicalSourceMode = "mapped_products";
        enrichmentSession.typical_source_mode = "mapped_products";
        enrichmentSession.typical_sources = [{
          name: file.name,
          size: file.size,
          products_count: validation.productsCount,
          attributes_count: validation.attributesCount,
          model_check: modelCheck,
          source: "typical_file",
          loaded_at: new Date().toISOString()
        }];
        if ($("typicalStatus")) $("typicalStatus").textContent = `${t("enrichment.typicalLoaded")}: ${validation.productsCount} ${t("enrichment.productsFound")}, ${validation.attributesCount} ${t("enrichment.attributesFound")}. ${modelCheck.ok ? t("enrichment.modelCheckOk") : t("enrichment.modelCheckWarn")}`;
        refreshTypicalControls();
        updateTypicalSourceModeUi();
        renderTypicalSourceAttributeMap();
        renderEnrichmentSessionList();
      } catch (error) {
        loadedProjectFiles.typicalDataFile = null;
        enrichmentSession.typical_sources = [];
        typicalProductsForEnrichment = [];
        typicalProductsPayloadForEnrichment = [];
        if ($("typicalStatus")) $("typicalStatus").textContent = error.message || t("enrichment.typicalInvalid");
        refreshTypicalControls();
        refreshTypicalSourceFileStatus();
        renderTypicalSourceAttributeMap();
        renderEnrichmentSessionList();
      }
    }

    function renderEnrichmentSessionList() {
      const target = $("enrichmentSessionList");
      if (!target) return;
      const typical = enrichmentSession.typical_sources || [];
      const matches = enrichmentSession.typical_matches || [];
      if (!typical.length && !matches.length) {
        target.innerHTML = "";
        return;
      }
      const typicalHtml = typical.length
        ? typical.map(item => `<div class="notice">${esc(t("enrichment.typicalLoaded"))}: <strong>${esc(item.name || "")}</strong> (${esc(item.products_count || 0)} ${esc(t("enrichment.productsFound"))}, ${esc(item.attributes_count || 0)} ${esc(t("enrichment.attributesFound"))})</div>`).join("")
        : "";
      const matchesHtml = matches.length
        ? matches.map((entry, index) => `<div class="enrichment-entry">
            <div>
              <strong>${esc(entry.product_label || entry.product_key)}</strong><br>
              <span class="muted">${esc(t("enrichment.typicalProduct"))}: ${esc(entry.typical_label || entry.typical_key)}</span><br>
              <span class="muted">${esc(currentLang === "pl" ? "Wybrane cechy" : "Selected features")}: ${esc(entry.selected_attributes_count ?? entry.selected_attributes?.length ?? 0)}</span>
            </div>
            <button type="button" class="secondary" data-remove-typical-match="${esc(index)}">${esc(t("enrichment.remove"))}</button>
          </div>`).join("")
        : "";
      target.innerHTML = `${typicalHtml}${matchesHtml}`;
      for (const button of target.querySelectorAll("[data-remove-typical-match]")) {
        button.onclick = () => {
          const index = Number.parseInt(button.dataset.removeTypicalMatch || "-1", 10);
          if (index >= 0) {
            enrichmentSession.typical_matches.splice(index, 1);
            renderEnrichmentSessionList();
            renderProductPreview();
          }
        };
      }
      for (const button of target.querySelectorAll("[data-remove-enrichment]")) {
        button.onclick = () => {
          const index = Number.parseInt(button.dataset.removeEnrichment || "-1", 10);
          if (index >= 0) {
            enrichmentSession.manual_entries.splice(index, 1);
            renderEnrichmentSessionList();
            renderProductPreview();
          }
        };
      }
    }

    function clearEnrichmentSession() {
      enrichmentSession.manual_entries = [];
      enrichmentSession.typical_matches = [];
      if ($("enrichmentActionStatus")) $("enrichmentActionStatus").textContent = t("enrichment.sessionCleared");
      renderEnrichmentSessionList();
      renderProductPreview();
    }

    function manualValueKey(value) {
      const normalize = item => {
        if (Array.isArray(item)) {
          return item.map(normalize).sort((left, right) => JSON.stringify(left).localeCompare(JSON.stringify(right)));
        }
        if (item && typeof item === "object") {
          return Object.keys(item).sort().reduce((acc, key) => {
            acc[key] = normalize(item[key]);
            return acc;
          }, {});
        }
        return String(displayCellValue(item || "")).trim();
      };
      return JSON.stringify(normalize(value));
    }

    function inlineManualInput(targetPath, value = "", extraAttrs = "", baselineValue = value) {
      const displayValue = displayCellValue(value);
      if (!manualEditEnabled) return renderLinkedText(displayValue, { limit: 360 }) || `<span class="muted">${esc(t("model.empty"))}</span>`;
      const field = targetFieldByKey(targetFieldsForMode("products"), targetPath);
      const manualAttrs = `${extraAttrs} data-inline-manual-baseline="${esc(manualValueKey(baselineValue))}"`;
      if (field?.options?.length) {
        return manualChoiceControl(targetPath, value, field, manualAttrs);
      }
      return `<input class="editable-value-input" type="text" data-inline-manual-target="${esc(targetPath)}" data-inline-manual-dirty="0" oninput="this.dataset.inlineManualDirty='1'" onchange="this.dataset.inlineManualDirty='1'" value="${esc(displayValue)}" ${manualAttrs}>`;
    }

    function parseManualChoiceValue(rawValue) {
      if (!rawValue) return "";
      try {
        const parsed = JSON.parse(rawValue);
        if (parsed && typeof parsed === "object") return parsed;
      } catch (error) {
        return rawValue;
      }
      return rawValue;
    }

    function manualInputValue(input) {
      if (input.dataset.inlineManualKind === "multi_choice") {
        return Array.from(input.selectedOptions || [])
          .map(option => parseManualChoiceValue(option.value))
          .filter(value => value !== "");
      }
      if (input.dataset.inlineManualKind === "single_choice") {
        return parseManualChoiceValue(input.value || "");
      }
      return input.value || "";
    }

    function saveInlineManualEdits() {
      if (!manualEditEnabled) return;
      const productKey = currentProductKeyForEnrichment();
      const normalizedProductKey = normalizeMatchKey(productKey);
      const inputs = Array.from(document.querySelectorAll("[data-inline-manual-target]"))
        .filter(input => input.dataset.inlineManualDirty === "1");
      let added = 0;
      const dirtyKeys = new Set();
      const dirtyTypeSeriesTargets = new Set();
      for (const input of inputs) {
        const targetPath = input.dataset.inlineManualTarget || "";
        const typeSeriesRowIndexRaw = input.dataset.inlineManualTypeSeriesRowIndex;
        const typeSeriesRowIndex = typeSeriesRowIndexRaw === undefined ? null : Number.parseInt(typeSeriesRowIndexRaw || "", 10);
        const hasTypeSeriesRowIndex = Number.isInteger(typeSeriesRowIndex) && typeSeriesRowIndex >= 0;
        if (!targetPath) continue;
        dirtyKeys.add(`${targetPath}::${hasTypeSeriesRowIndex ? typeSeriesRowIndex : ""}`);
        if (targetPathIsTypeSeries(targetPath)) dirtyTypeSeriesTargets.add(targetPath);
      }
      enrichmentSession.manual_entries = (enrichmentSession.manual_entries || []).filter(entry => {
        if (entry.source !== "manual" || normalizeMatchKey(entry.product_key) !== normalizedProductKey) return true;
        const rowIndex = Number.isInteger(entry.type_series_row_index) ? entry.type_series_row_index : "";
        if (targetPathIsTypeSeries(entry.target_path) && dirtyTypeSeriesTargets.has(entry.target_path) && rowIndex === "") return false;
        return !dirtyKeys.has(`${entry.target_path || ""}::${rowIndex}`);
      });
      for (const input of inputs) {
        const targetPath = input.dataset.inlineManualTarget || "";
        const value = manualInputValue(input);
        const typeSeriesRowIndexRaw = input.dataset.inlineManualTypeSeriesRowIndex;
        const typeSeriesRowIndex = typeSeriesRowIndexRaw === undefined ? null : Number.parseInt(typeSeriesRowIndexRaw || "", 10);
        const hasTypeSeriesRowIndex = Number.isInteger(typeSeriesRowIndex) && typeSeriesRowIndex >= 0;
        if (!targetPath) continue;
        if (targetPathIsTypeSeries(targetPath) && !hasTypeSeriesRowIndex) continue;
        if ((input.dataset.inlineManualBaseline || "") === manualValueKey(value)) continue;
        if (Array.isArray(value) && !value.length) continue;
        if (!Array.isArray(value) && !String(displayCellValue(value)).trim()) continue;
        const entry = {
          id: `manual-${Date.now()}-${added}`,
          source: "manual",
          target_path: targetPath,
          value,
          scope: "current_product",
          product_key: productKey,
          mode: $("enrichmentMode")?.value || "replace",
          apply_type_series_to_all: targetPathIsTypeSeries(targetPath) ? false : $("applyTypeSeriesToAll")?.checked !== false,
          created_at: new Date().toISOString()
        };
        if (hasTypeSeriesRowIndex) entry.type_series_row_index = typeSeriesRowIndex;
        enrichmentSession.manual_entries.push(entry);
        added += 1;
      }
      if ($("enrichmentActionStatus")) {
        $("enrichmentActionStatus").textContent = added ? t("enrichment.manualSaved") : t("enrichment.manualNoValues");
      }
      renderEnrichmentSessionList();
      renderProductPreview();
    }

    function undoCurrentProductChanges() {
      const productKey = normalizeMatchKey(currentProductKeyForEnrichment());
      enrichmentSession.manual_entries = (enrichmentSession.manual_entries || []).filter(entry => normalizeMatchKey(entry.product_key) !== productKey);
      enrichmentSession.typical_matches = (enrichmentSession.typical_matches || []).filter(match => normalizeMatchKey(match.product_key) !== productKey);
      if ($("enrichmentActionStatus")) $("enrichmentActionStatus").textContent = t("enrichment.productChangesUndone");
      renderEnrichmentSessionList();
      renderProductPreview();
    }

    function removeEnrichmentForProductKeys(productKeys) {
      const keys = new Set(Array.from(productKeys || []).map(normalizeMatchKey).filter(Boolean));
      if (!keys.size) return 0;
      const beforeManual = (enrichmentSession.manual_entries || []).length;
      const beforeMatches = (enrichmentSession.typical_matches || []).length;
      enrichmentSession.manual_entries = (enrichmentSession.manual_entries || []).filter(entry => !keys.has(normalizeMatchKey(entry.product_key)));
      enrichmentSession.typical_matches = (enrichmentSession.typical_matches || []).filter(match => !keys.has(normalizeMatchKey(match.product_key)));
      return (beforeManual - enrichmentSession.manual_entries.length) + (beforeMatches - enrichmentSession.typical_matches.length);
    }

    function restoreEnrichmentChanges(scope = "current_product") {
      const targets = scope === "all_products"
        ? mappedRowsForPreview().map((entry, index) => ({ entry, index }))
        : entriesForTypicalScope(scope === "selected_products" ? "selected_products" : "current_product");
      const keys = targets.map(({ entry, index }) => productKeyForEnrichmentEntry(entry, index));
      const removed = removeEnrichmentForProductKeys(keys);
      if ($("enrichmentActionStatus")) $("enrichmentActionStatus").textContent = currentLang === "pl"
        ? `Cofni\u0119to wpisy uzupe\u0142nie\u0144: ${removed}.`
        : `Removed enrichment entries: ${removed}.`;
      renderEnrichmentSessionList();
      renderProductPreview();
    }

    function restoreEnrichmentFromUi() {
      const option = window.prompt(currentLang === "pl"
        ? "Wybierz zakres przywracania:\\n1 - widoczny produkt\\n2 - wybrane produkty z listy\\n3 - wszystkie produkty"
        : "Choose restore scope:\\n1 - visible product\\n2 - selected products\\n3 - all products", "1");
      if (!option) return;
      const scope = option === "3" ? "all_products" : (option === "2" ? "selected_products" : "current_product");
      const confirmed = window.confirm(currentLang === "pl"
        ? "Ta operacja usunie zapami\u0119tane uzupe\u0142nienia dla wybranego zakresu. Kontynuowa\u0107?"
        : "This removes remembered enrichments for the selected scope. Continue?");
      if (!confirmed) return;
      restoreEnrichmentChanges(scope);
    }

    function undoLastEnrichmentChange() {
      const manual = (enrichmentSession.manual_entries || []).map((entry, index) => ({ type: "manual", index, created_at: entry.created_at || "" }));
      const typical = (enrichmentSession.typical_matches || []).map((entry, index) => ({ type: "typical", index, created_at: entry.created_at || "" }));
      const last = manual.concat(typical).sort((a, b) => String(a.created_at).localeCompare(String(b.created_at))).pop();
      if (!last) return;
      if (last.type === "manual") enrichmentSession.manual_entries.splice(last.index, 1);
      else enrichmentSession.typical_matches.splice(last.index, 1);
      if ($("enrichmentActionStatus")) $("enrichmentActionStatus").textContent = currentLang === "pl" ? "Cofni\u0119to ostatni\u0105 zmian\u0119." : "Last change undone.";
      renderEnrichmentSessionList();
      renderProductPreview();
    }

    function renderManualEditTable() {
      const entry = currentPreviewEntry();
      const mapped = mappedObjectForPreview(entry.row || {}, entry.context || {});
      const fields = targetFieldsForMode("products").filter(field => field && field.key);
      const rows = fields.map(field => {
        let existing = mapped[field.key] || "";
        if (fieldIsTypeSeries(field)) {
          const variantRow = Array.isArray(entry.variants) && entry.variants.length ? entry.variants[0] : entry.row;
          const mappedItem = Object.values(productMappingProfile || {}).find(item => item?.target_path === field.key);
          if (mappedItem) {
            const sourceColumn = mappedItem.source_column || "";
            existing = applyCleanup(variantRow?.[sourceColumn], cleanupValueOnly(mappedItem));
          }
        }
        return `<tr>
          <td><strong>${esc(cleanModelLabel(field.label || field.key))}</strong><br><span class="muted">${esc(displayGroupName(field.group || ""))}</span></td>
          <td>${renderLinkedText(existing, { limit: 260 }) || `<span class="muted">${esc(t("model.empty"))}</span>`}</td>
          <td><input type="text" data-manual-target="${esc(field.key)}" placeholder="${esc(currentLang === "pl" ? "dopisz wartoĹ›Ä‡" : "add value")}"></td>
        </tr>`;
      }).join("");
      return `<table class="manual-edit-table">
        <thead><tr><th>${esc(t("preview.field"))}</th><th>${esc(currentLang === "pl" ? "Aktualna wartoĹ›Ä‡" : "Current value")}</th><th>${esc(currentLang === "pl" ? "WartoĹ›Ä‡ rÄ™czna" : "Manual value")}</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>`;
    }

    function typicalProductOptions() {
      if (!typicalProductsForEnrichment.length) {
        return `<option value="">${esc(t("enrichment.noTypicalProducts"))}</option>`;
      }
      return typicalProductsForEnrichment.map(product => {
        const label = `${product.source_name ? `${product.source_name} / ` : ""}${product.label}${product.code ? ` (${product.code})` : ""} - ${product.attributes_count} ${t("enrichment.attributesFound")}`;
        return `<option value="${esc(product.ui_key || product.key)}">${esc(label)}</option>`;
      }).join("");
    }

    function shortTypicalProductLabel(product) {
      const labelPath = $("typicalSourceLabelFieldVisible")?.value || $("typicalSourceLabelField")?.value || "";
      if (labelPath) {
        const customValue = typicalProductValueForPath(product, labelPath);
        if (customValue) return customValue;
      }
      const label = displayCellValue(product?.label || product?.key || "");
      const code = displayCellValue(product?.code || "");
      const isTechnicalId = value => /^[a-f0-9]{20,}$/i.test(String(value || "").trim());
      if (label && !isTechnicalId(label)) return label;
      if (code && !isTechnicalId(code)) return code;
      return currentLang === "pl" ? "Produkt z pliku uzupe\u0142nie\u0144" : "Enrichment-file product";
    }

    function typicalSourceLabelFieldOptions() {
      const selected = $("typicalSourceLabelFieldVisible")?.value || $("typicalSourceLabelField")?.value || "";
      return supplementMatchFieldOptions(selected);
    }

    function typicalSourceProductOptions() {
      if (!typicalProductsForEnrichment.length) {
        return `<option value="">${esc(t("enrichment.noTypicalProducts"))}</option>`;
      }
      const selectedKey = $("typicalSourceProduct")?.value || (typicalProductsForEnrichment[0]?.ui_key || typicalProductsForEnrichment[0]?.key || "");
      return typicalProductsForEnrichment.map(product => {
        const key = product.ui_key || product.key;
        return `<option value="${esc(key)}"${key === selectedKey ? " selected" : ""}>${esc(shortTypicalProductLabel(product))}</option>`;
      }).join("");
    }

    function renderTypicalSourceProductPreview() {
      const meta = selectedTypicalSourceMeta();
      const product = meta ? typicalProductsPayloadForEnrichment[meta.index] : null;
      if (!meta || !product) {
        return `<div class="helper">${esc(t("enrichment.noTypicalProducts"))}</div>`;
      }
      const rows = pimProductAttributes(product)
        .filter(attr => pimAttrValue(attr) !== "")
        .filter(attributeIsFromSupplementMapping)
        .slice(0, 80)
        .map(attr => {
          const rowLabel = typicalAttributeIsTypeSeries(attr) && attr.RowI
            ? `${typicalAttributeLabel(attr)} (${currentLang === "pl" ? "wiersz" : "row"} ${attr.RowI})`
            : typicalAttributeLabel(attr);
          return `<tr><td>${esc(cleanModelLabel(rowLabel))}</td><td>${renderLinkedText(pimAttrValue(attr), { limit: 420 })}</td></tr>`;
        }).join("");
      return `<div class="source-product-preview">
        <h3>${esc(currentLang === "pl" ? "Dane produktu \u017ar\u00f3d\u0142owego" : "Source product data")}</h3>
        <div class="muted">${esc(shortTypicalProductLabel(meta))}</div>
        <table>
          <thead><tr><th>${esc(t("preview.field"))}</th><th>${esc(t("preview.cleanedValue"))}</th></tr></thead>
          <tbody>${rows || `<tr><td colspan="2">${esc(currentLang === "pl" ? "Ten produkt nie ma zmapowanych danych do pokazania." : "This product has no mapped data to show.")}</td></tr>`}</tbody>
        </table>
      </div>`;
    }

    function selectedSupplementHasTypeSeries() {
      return selectedSupplementAttributeKeys().some(key => {
        if (key.startsWith("path|")) {
          return key.slice(5).startsWith("type_series[]") || key.slice(5).startsWith("type_series.");
        }
        const [metaKey, attrKey] = key.split("|");
        const meta = typicalProductsForEnrichment.find(product => product.ui_key === metaKey || product.key === metaKey);
        const product = meta ? typicalProductsPayloadForEnrichment[meta.index] : null;
        const attr = pimProductAttributes(product).find(item => typicalAttributeKey(item) === attrKey);
        return typicalAttributeIsTypeSeries(attr);
      });
    }

    function refreshTypicalControls() {
      const fileSelect = $("enrichmentFileSelect");
      if (fileSelect) fileSelect.innerHTML = enrichmentFileOptionsHtml();
      const sourceLabelFieldVisible = $("typicalSourceLabelFieldVisible");
      if (sourceLabelFieldVisible) {
        const previous = sourceLabelFieldVisible.value;
        sourceLabelFieldVisible.innerHTML = typicalSourceLabelFieldOptions();
        if (previous && Array.from(sourceLabelFieldVisible.options).some(option => option.value === previous)) {
          sourceLabelFieldVisible.value = previous;
        }
      }
      const targetProducts = $("typicalTargetProducts");
      if (targetProducts) targetProducts.innerHTML = productCheckboxesForEnrichmentTargets();
      const sourceProductSelect = $("typicalSourceProduct");
      if (sourceProductSelect) {
        const previous = sourceProductSelect.value;
        sourceProductSelect.innerHTML = typicalSourceProductOptions();
        if (previous && Array.from(sourceProductSelect.options).some(option => option.value === previous)) {
          sourceProductSelect.value = previous;
        }
        sourceProductSelect.disabled = !typicalProductsForEnrichment.length;
      }
      const sourcePreview = $("typicalSourceProductPreview");
      if (sourcePreview) sourcePreview.innerHTML = renderTypicalSourceProductPreview();
      const picker = $("typicalAttributePicker");
      if (picker) picker.innerHTML = renderTypicalAttributePicker();
      const supplementSelect = $("supplementAttributeSelect");
      if (supplementSelect) {
        supplementSelect.innerHTML = supplementAttributeOptions();
        supplementSelect.disabled = !typicalProductsForEnrichment.length;
      }
      const supplementMatchField = $("supplementMatchField");
      if (supplementMatchField) {
        supplementMatchField.innerHTML = supplementMatchFieldOptions(supplementMatchField.value || "");
        supplementMatchField.disabled = !typicalProductsForEnrichment.length;
      }
      const addButton = $("addTypicalMatchBtn");
      if (addButton) addButton.disabled = !typicalProductsForEnrichment.length;
      updateTypeSeriesApplyVisibility();
    }

    function updateTypeSeriesApplyVisibility() {
      const row = $("applyTypeSeriesToAll")?.closest("[data-type-series-apply-row]");
      if (row) row.hidden = !selectedSupplementHasTypeSeries();
    }

    function updateEnrichmentScopeUi() {
      const scope = $("typicalMatchScope")?.value || "selected_products";
      const filterEnabled = $("enableEnrichmentFilter")?.checked || false;
      for (const element of document.querySelectorAll("[data-enrichment-match-row]")) {
        element.hidden = scope !== "match_by_feature";
      }
      for (const element of document.querySelectorAll("[data-source-product-row]")) {
        element.hidden = scope === "match_by_feature";
      }
      for (const element of document.querySelectorAll("[data-selected-products-row]")) {
        element.hidden = scope !== "selected_products";
      }
      for (const element of document.querySelectorAll("[data-enrichment-filter-row]")) {
        element.hidden = !filterEnabled;
      }
      const supplementSelect = $("supplementAttributeSelect");
      if (supplementSelect) supplementSelect.innerHTML = supplementAttributeOptions();
      const filterValue = $("enrichmentFilterValue");
      if (filterValue) filterValue.disabled = !$("enrichmentFilterField")?.value;
      updateTypeSeriesApplyVisibility();
    }

    function selectedSupplementTargetPaths() {
      const paths = [];
      for (const key of selectedSupplementAttributeKeys()) {
        if (key.startsWith("path|")) {
          paths.push(key.slice(5));
          continue;
        }
        const [metaKey, attrKey] = key.split("|");
        const meta = typicalProductsForEnrichment.find(product => product.ui_key === metaKey || product.key === metaKey);
        const product = meta ? typicalProductsPayloadForEnrichment[meta.index] : null;
        const attr = pimProductAttributes(product).find(item => typicalAttributeKey(item) === attrKey);
        if (attr) paths.push(typicalAttributeModelPath(attr));
      }
      return Array.from(new Set(paths.filter(Boolean)));
    }

    function addMatchesBySharedFeature(selectedTargetPaths) {
      const mainMatchPath = $("enrichmentMatchField")?.value || $("enrichmentFilterField")?.value || "";
      const supplementMatchPath = $("supplementMatchField")?.value || "";
      if (!mainMatchPath || !supplementMatchPath || !selectedTargetPaths.length) {
        if ($("enrichmentActionStatus")) $("enrichmentActionStatus").textContent = currentLang === "pl"
          ? "Wybierz cechÄ™ identyfikujÄ…cÄ… w mapowaniu gĹ‚Ăłwnym, takÄ… samÄ… cechÄ™ w pliku uzupeĹ‚nieĹ„ oraz cechÄ™ do dopisania."
          : "Choose the identifying feature in main mapping, the same feature in enrichment file, and the feature to apply.";
        return;
      }
      const typicalByValue = new Map();
      for (const meta of typicalProductsForEnrichment) {
        const key = normalizeMatchKey(typicalProductValueForPath(meta, supplementMatchPath));
        if (key && !typicalByValue.has(key)) typicalByValue.set(key, meta);
      }
      const matches = [];
      for (const [index, entry] of mappedRowsForPreview().entries()) {
        const lookup = normalizeMatchKey(mainProductValueForPath(entry, mainMatchPath));
        const typical = lookup ? typicalByValue.get(lookup) : null;
        if (!typical) continue;
        const selectedForTypical = typicalAttributeKeysForPaths(typical, selectedTargetPaths);
        if (!selectedForTypical.length) continue;
        const productKey = normalizeMatchKey(productKeyForEnrichmentEntry(entry, index));
        if (!productKey) continue;
        matches.push({ entry, index, productKey, typical, selectedForTypical });
      }
      const productKeys = new Set(matches.map(match => match.productKey));
      enrichmentSession.typical_matches = (enrichmentSession.typical_matches || []).filter(match => !productKeys.has(match.product_key));
      for (const match of matches) {
        enrichmentSession.typical_matches.push({
          source: "same_feature_match",
          scope: "match_by_feature",
          product_key: match.productKey,
          product_label: productLabelForPreview(match.entry, match.index),
          typical_key: match.typical.key,
          typical_label: match.typical.label || match.typical.key,
          selected_attributes: match.selectedForTypical,
          selected_attributes_count: match.selectedForTypical.length,
          match_field: mainMatchPath,
          supplement_match_field: supplementMatchPath,
          preserve_existing: $("preserveExistingEnrichment")?.checked !== false,
          apply_type_series_to_all: $("applyTypeSeriesToAll")?.checked !== false,
          created_at: new Date().toISOString()
        });
      }
      if ($("enrichmentActionStatus")) $("enrichmentActionStatus").textContent = currentLang === "pl"
        ? `Dopisano dane dla ${matches.length} produktĂłw dopasowanych po tej samej cesze.`
        : `Applied data to ${matches.length} products matched by the same feature.`;
      renderEnrichmentSessionList();
      renderProductPreview();
    }

    function addTypicalMatchFromUi() {
      const selectedAttributes = selectedSupplementAttributeKeys().length
        ? selectedSupplementAttributeKeys()
        : Array.from(document.querySelectorAll("[data-typical-attr]:checked")).map(input => input.dataset.typicalAttr);
      const scope = $("typicalMatchScope")?.value || "current_product";
      if (scope === "match_by_feature") {
        addMatchesBySharedFeature(selectedSupplementTargetPaths());
        return;
      }
      const selectedTypicalProducts = typicalProductMetasForAttributeKeys(selectedAttributes);
      if (!selectedTypicalProducts.length) return;
      if (!selectedAttributes.length) {
        if ($("enrichmentActionStatus")) $("enrichmentActionStatus").textContent = currentLang === "pl"
          ? "Wybierz przynajmniej jednÄ… zmapowanÄ… cechÄ™ z pliku uzupeĹ‚nieĹ„."
          : "Choose at least one mapped feature from the enrichment file.";
        return;
      }
      const targets = entriesForTypicalScope(scope);
      if (!targets.length) {
        if ($("enrichmentActionStatus")) $("enrichmentActionStatus").textContent = currentLang === "pl"
          ? "Filtr nie znalaz\u0142 produkt\u00f3w do uzupe\u0142nienia."
          : "The filter did not find products to enrich.";
        return;
      }
      const productKeys = new Set(targets.map(({ entry, index }) => normalizeMatchKey(productKeyForEnrichmentEntry(entry, index))).filter(Boolean));
      enrichmentSession.typical_matches = (enrichmentSession.typical_matches || []).filter(match => !productKeys.has(match.product_key));
      for (const { entry, index } of targets) {
        const productKey = normalizeMatchKey(productKeyForEnrichmentEntry(entry, index));
        if (!productKey) continue;
        for (const typical of selectedTypicalProducts) {
          const typicalUiKey = typical.ui_key || typical.key;
          const selectedForTypical = selectedAttributes
            .filter(key => key.startsWith(`${typicalUiKey}|`))
            .map(key => key.split("|").slice(1).join("|"));
          if (!selectedForTypical.length) continue;
          enrichmentSession.typical_matches.push({
            source: "typical_manual_match",
            scope,
            product_key: productKey,
            product_label: productLabelForPreview(entry, index),
            typical_key: typical.key,
            typical_label: typical.label || typical.key,
            selected_attributes: selectedForTypical,
            selected_attributes_count: selectedForTypical.length,
            preserve_existing: $("preserveExistingEnrichment")?.checked !== false,
            apply_type_series_to_all: $("applyTypeSeriesToAll")?.checked !== false,
            created_at: new Date().toISOString()
          });
        }
      }
      $("enrichmentActionStatus").textContent = `${t("enrichment.matchSaved")} (${targets.length} x ${selectedTypicalProducts.length})`;
      renderEnrichmentSessionList();
      renderProductPreview();
    }

    function bestAnalysisTable(data) {
      return (data.tables || [])
        .map(table => ({ table, score: table.product_mapping?.score || 0 }))
        .sort((a, b) => b.score - a.score)[0]?.table || null;
    }

    function showProductWorkspace(tab = "mapping") {
      if (!mainProductTable) {
        renderProductModelPreview();
        return;
      }
      activeTable = mainProductTable;
      activeMode = "products";
      mappingWorkspaceTab = tab;
      showReport(renderMappingEditor(mainProductTable, "products"), tab === "enrichment" ? t("enrichment.enrichmentTab") : "Mapping: products");
      attachMappingEvents("products");
      setWorkspaceTab(tab);
    }

    async function analyzeSupplementFileForMapping() {
      const file = supplementFileForMapping || $("typicalRawFileVisible")?.files?.[0] || loadedProjectFiles.typicalDataFile;
      if (!file) {
        if ($("typicalStatus")) $("typicalStatus").textContent = t("enrichment.noSupplementFile");
        return;
      }
      if (activeMode === "products" && activeTable) {
        collectMapping("products");
        mainProductTable = activeTable;
      }
      const body = new FormData();
      body.append("file", file);
      if (activeProductModelId) {
        body.append("product_model_id", activeProductModelId);
      } else {
        productModelDefinitionFiles().forEach((modelFile) => body.append("product_model_files", modelFile));
      }
      if ($("typicalStatus")) $("typicalStatus").textContent = t("analysis.running");
      const response = await fetch("/analyze", { method: "POST", body });
      const data = await response.json();
      if (!response.ok) {
        if ($("typicalStatus")) $("typicalStatus").textContent = data.detail || t("status.error");
        return;
      }
      const best = bestAnalysisTable(data);
      if (!best) {
        if ($("typicalStatus")) $("typicalStatus").textContent = t("analysis.noTables");
        return;
      }
      supplementAnalysisTable = best;
      activeTable = best;
      activeMode = "supplement";
      mappingWorkspaceTab = "mapping";
      productPreviewIndex = 0;
      showReport(renderMappingEditor(best, "supplement"), t("enrichment.supplementMappingTitle"));
      attachMappingEvents("supplement");
      if ($("typicalStatus")) $("typicalStatus").textContent = t("analysis.ready");
    }

    async function prepareSupplementDataFromMapping() {
      const file = supplementFileForMapping || $("typicalRawFileVisible")?.files?.[0] || loadedProjectFiles.typicalDataFile;
      const status = $("supplementMappingStatus") || $("typicalStatus") || $("productsStatus");
      if (!file) {
        if (status) status.textContent = t("enrichment.noSupplementFile");
        return;
      }
      if (activeMode === "supplement") collectMapping("supplement");
      if (!supplementMappingProfile) {
        if (status) status.textContent = t("enrichment.noSupplementMapping");
        return;
      }
      validateMappingConflicts(supplementMappingProfile);
      if (hasBlockingMappingConflicts()) {
        if (status) status.textContent = t("mapping.duplicateTargetBlocked");
        return;
      }
      const body = new FormData();
      body.append("file", file);
      if (supplementMapping) body.append("product_mapping", JSON.stringify(supplementMapping));
      body.append("product_mapping_profile", JSON.stringify(supplementMappingProfile));
      if (status) status.textContent = currentLang === "pl" ? "PrzygotowujÄ™ dane uzupeĹ‚nieĹ„." : "Preparing enrichment data.";
      try {
        const response = await fetch("/convert-products", { method: "POST", body });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || t("status.error"));
        supplementProductsUrl = data.files?.products_json || "";
        const productsResponse = await fetch(supplementProductsUrl);
        if (!productsResponse.ok) throw new Error(t("enrichment.typicalInvalid"));
        supplementProductsPayload = await productsResponse.json();
        acceptSupplementProductsPayload(supplementProductsPayload, {
          name: file.name,
          size: file.size,
          source: "mapped_supplement_file",
          productsUrl: supplementProductsUrl,
          mappingProfile: supplementMappingProfile
        });
        collapsedSupplementMappings.push({
          name: file.name,
          size: file.size,
          table: supplementAnalysisTable,
          profile: JSON.parse(JSON.stringify(supplementMappingProfile || {})),
          mapping: JSON.parse(JSON.stringify(supplementMapping || {})),
          accepted_at: new Date().toISOString()
        });
        if (status) status.textContent = t("enrichment.supplementPrepared");
        showProductWorkspace("enrichment");
      } catch (error) {
        if (status) status.textContent = error.message || t("status.error");
      }
    }

    function refreshEnrichmentCurrentProduct() {
      const input = $("enrichmentCurrentProduct");
      if (input) input.value = currentProductKeyForEnrichment();
      const manualLabel = $("manualCurrentProduct");
      if (manualLabel) manualLabel.textContent = currentProductKeyForEnrichment();
      const targetProducts = $("typicalTargetProducts");
      if (targetProducts && !targetProducts.querySelector("[data-typical-target-product]:checked")) {
        targetProducts.innerHTML = productCheckboxesForEnrichmentTargets();
      }
    }

    async function loadRawTypicalFileForMapping(file) {
      if (!file) return;
      typicalSourceMode = "raw_file";
      enrichmentSession.typical_source_mode = "raw_file";
      loadedProjectFiles.typicalDataFile = file;
      supplementFileForMapping = file;
      supplementAnalysisTable = null;
      supplementMapping = null;
      supplementMappingProfile = null;
      supplementProductsPayload = null;
      supplementProductsUrl = "";
      enrichmentSession.typical_sources = (enrichmentSession.typical_sources || []).filter(source => !source.mapping_required).concat([{
        name: file.name,
        size: file.size,
        source: "supplement_file_to_map",
        mapping_required: true,
        loaded_at: new Date().toISOString()
      }]);
      if ($("typicalStatus")) $("typicalStatus").textContent = `${t("enrichment.supplementFile")}: ${file.name}. ${t("enrichment.supplementMapLater")}`;
      updateTypicalSourceModeUi();
      refreshTypicalControls();
      renderEnrichmentSessionList();
    }

    function renderCollapsedSupplementMappings() {
      const mappings = collapsedSupplementMappings || [];
      if (!mappings.length) return "";
      return `<div class="collapsed-mapping-list">
        ${mappings.map((item, index) => `<div class="collapsed-mapping-item">
          <div>
            <strong>${esc(t("enrichment.collapsedMapping"))}</strong><br>
            <span class="muted">${esc(item.name || t("enrichment.supplementFile"))}</span>
          </div>
          <button type="button" class="secondary" data-edit-supplement-mapping="${esc(index)}">${esc(t("enrichment.editSupplementMapping"))}</button>
        </div>`).join("")}
      </div>`;
    }

    function editCollapsedSupplementMapping(index) {
      const item = collapsedSupplementMappings[index];
      if (!item || !item.table) return;
      supplementAnalysisTable = item.table;
      supplementMappingProfile = JSON.parse(JSON.stringify(item.profile || {}));
      supplementMapping = JSON.parse(JSON.stringify(item.mapping || {}));
      activeTable = item.table;
      activeMode = "supplement";
      mappingWorkspaceTab = "mapping";
      showReport(renderMappingEditor(item.table, "supplement"), t("enrichment.supplementMappingTitle"));
      attachMappingEvents("supplement");
    }

    function renderEnrichmentPanel() {
      const options = targetFieldSelectOptions();
      if (!options) return "";
      const supplementReady = typicalProductsForEnrichment.length > 0;
      return `<div class="mapping-card" id="enrichmentPanel">
        <h2 class="mapping-section-title">${esc(t("enrichment.title"))}</h2>
        <div class="muted">${esc(t("enrichment.help"))}</div>
        <div id="typicalStatus" class="status">${esc(t("typical.optional"))}</div>
        <div class="enrichment-actions-row">
          <button type="button" class="secondary" id="toggleManualEditBtn">${esc(manualEditEnabled ? t("enrichment.disableManualEdit") : t("enrichment.enableManualEdit"))}</button>
          <button type="button" class="secondary" id="openSupplementFileBtn">${esc(currentLang === "pl" ? "Edytuj dane na podstawie pliku z uzupe\u0142nieniami" : "Edit data from enrichment file")}</button>
          <button type="button" class="secondary" id="restoreEnrichmentBtn">${esc(currentLang === "pl" ? "Przywr\u00f3\u0107 dane do mapowania g\u0142\u00f3wnego" : "Restore main-mapping data")}</button>
        </div>
        ${manualEditEnabled ? `<div class="manual-edit-actions">
          <span class="helper">${esc(t("enrichment.editingEnabled"))}</span>
          <button type="button" id="saveManualEditsBtn">${esc(t("enrichment.saveManualEdits"))}</button>
          <button type="button" class="secondary" id="undoProductChangesBtn">${esc(t("enrichment.undoProductChanges"))}</button>
          <label>${esc(t("enrichment.mode"))}
            <select id="enrichmentMode">
              <option value="replace" selected>${esc(t("enrichment.replace"))}</option>
              <option value="missing_only">${esc(t("enrichment.missingOnly"))}</option>
            </select>
          </label>
        </div>` : `<div class="helper">${esc(t("enrichment.editingDisabled"))}</div>`}
        <div class="workflow-step">
          <h3>${esc(t("enrichment.fileMappingStep"))}</h3>
          <label>${esc(t("enrichment.supplementFile"))}
            <input id="typicalRawFileVisible" type="file" accept=".xlsx,.xlsm,.json,.csv,.tsv">
          </label>
          <div id="typicalRawFileStatus">${typicalRawFileStatusHtml()}</div>
          <div class="helper">${esc(t("enrichment.supplementMapLater"))}</div>
          <div class="mapping-tools">
            <button type="button" class="secondary" id="mapSupplementFileBtn">${esc(t("enrichment.mapSupplement"))}</button>
            <button type="button" id="prepareSupplementDataBtn"${supplementMappingProfile ? "" : " disabled"}>${esc(t("enrichment.prepareSupplement"))}</button>
          </div>
          ${renderCollapsedSupplementMappings()}
        </div>
        ${supplementReady ? `<div class="workflow-step is-secondary">
          <h3>${esc(t("enrichment.applyStep"))}</h3>
          <div class="enrichment-section">
            <h3>${esc(currentLang === "pl" ? "Produkty edytowane" : "Edited products")}</h3>
            <div class="enrichment-grid">
            <label>${esc(currentLang === "pl" ? "Nazwa produktu wyĹ›wietlana w podglÄ…dzie na ĹĽywo" : "Product shown in live preview")}
              <input id="enrichmentCurrentProduct" type="text" value="${esc(currentProductKeyForEnrichment())}" readonly>
            </label>
            <label>${esc(currentLang === "pl" ? "Zakres produktĂłw do edycji" : "Products to edit")}
              <select id="typicalMatchScope">
                <option value="selected_products" selected>${esc(currentLang === "pl" ? "Wybrane z listy" : "Selected from list")}</option>
                <option value="all_products">${esc(currentLang === "pl" ? "Wszystkie produkty" : "All products")}</option>
              </select>
            </label>
            </div>
            <div data-selected-products-row>
              <div class="muted">${esc(currentLang === "pl" ? "Lista produktĂłw z moĹĽliwoĹ›ciÄ… wielokrotnego wyboru" : "Product list with multi-selection")}</div>
              <div id="typicalTargetProducts" class="product-checkbox-list">${productCheckboxesForEnrichmentTargets()}</div>
            </div>
            <label class="inline-check">
              <input id="enableEnrichmentFilter" type="checkbox">
              <span>${esc(currentLang === "pl" ? "UĹĽyj dodatkowego filtra po cesze produktu" : "Use an additional product-feature filter")}</span>
            </label>
            <div class="enrichment-grid">
            <label data-enrichment-filter-row>${esc(currentLang === "pl" ? "Cecha identyfikujÄ…ca produkty do zmiany" : "Feature identifying products to change")}
              <select id="enrichmentFilterField">${allTargetFieldSelectOptions("")}</select>
            </label>
            <label data-enrichment-filter-row>${esc(currentLang === "pl" ? "Warto\u015b\u0107 cechy" : "Feature value")}
              <select id="enrichmentFilterValue" disabled>${productTargetValueOptions("")}</select>
            </label>
            <label data-enrichment-match-row>${esc(currentLang === "pl" ? "Cecha identyfikujÄ…ca w mapowaniu gĹ‚Ăłwnym" : "Identifying feature in main mapping")}
              <select id="enrichmentMatchField">${allTargetFieldSelectOptions("")}</select>
            </label>
            <label data-enrichment-match-row>${esc(t("enrichment.supplementMatchField"))}
              <select id="supplementMatchField"${supplementReady ? "" : " disabled"}>${supplementMatchFieldOptions("")}</select>
            </label>
            </div>
          </div>
          <div class="enrichment-section">
            <h3>${esc(currentLang === "pl" ? "Produkt z pliku uzupeĹ‚nieĹ„" : "Product from enrichment file")}</h3>
            <div class="enrichment-grid">
            <label data-source-product-row>${esc(currentLang === "pl" ? "Cecha uĹĽywana do wyboru produktu ĹşrĂłdĹ‚owego" : "Feature used to choose the source product")}
              <select id="typicalSourceLabelFieldVisible">${typicalSourceLabelFieldOptions()}</select>
            </label>
            <label data-source-product-row>${esc(currentLang === "pl" ? "Produkt ĹşrĂłdĹ‚owy z pliku uzupeĹ‚nieĹ„" : "Source product from enrichment file")}
              <select id="typicalSourceProduct"${supplementReady ? "" : " disabled"}>${typicalSourceProductOptions()}</select>
            </label>
            <label>${esc(currentLang === "pl" ? "Cecha z pliku uzupe\u0142nie\u0144 do dopisania" : "Feature from enrichment file to apply")}
              <select id="supplementAttributeSelect"${supplementReady ? "" : " disabled"}>${supplementAttributeOptions()}</select>
            </label>
            <label class="inline-check">
              <input id="preserveExistingEnrichment" type="checkbox" checked>
              <span>${esc(t("enrichment.preserveExisting"))}</span>
            </label>
            <label class="inline-check" data-type-series-apply-row>
              <input id="applyTypeSeriesToAll" type="checkbox" checked>
              <span>${esc(t("enrichment.applyTypeSeriesAll"))}</span>
            </label>
          </div>
          <div id="typicalSourceProductPreview" data-source-product-row>${renderTypicalSourceProductPreview()}</div>
          <h3>${esc(currentLang === "pl" ? "Dane z pliku uzupeĹ‚nieĹ„ do dopisania" : "Enrichment-file data to apply")}</h3>
          <div class="notice">${esc(t("enrichment.askTypeSeriesAll"))}</div>
          <div id="typicalAttributePicker" hidden>${renderTypicalAttributePicker()}</div>
          <div class="enrichment-actions-row">
            <button type="button" class="secondary" id="undoLastEnrichmentBtn">${esc(currentLang === "pl" ? "Cofnij ostatniÄ… zmianÄ™" : "Undo last change")}</button>
            <button type="button" id="addTypicalMatchBtn"${typicalProductsForEnrichment.length ? "" : " disabled"}>${esc(t("enrichment.addTypicalMatch"))}</button>
            <button type="button" class="secondary" id="clearEnrichmentSessionBtn">${esc(t("enrichment.clearSession"))}</button>
          </div>
        </div>
        ` : ""}
        <div id="enrichmentActionStatus" class="status"></div>
        <div id="enrichmentSessionList" class="enrichment-session-list"></div>
      </div>`;
    }

    function renderProductsOutputPanel() {
      return `<div class="mapping-card">
        <h2 class="mapping-section-title">${esc(t("products.outputTitle"))}</h2>
        <div class="muted">${esc(t("products.outputHelp"))}</div>
        <button type="button" id="generateProductsInlineBtn">${esc(t("products.generate"))}</button>
        <button type="button" class="secondary" id="saveProductsAsBtn">${esc(t("products.saveAs"))}</button>
        <div id="productsSaveStatus" class="status"></div>
        <div id="productsLinksInline" class="links"></div>
      </div>`;
    }

    function renderSupplementOutputPanel() {
      return `<div class="mapping-card">
        <h2 class="mapping-section-title">${esc(t("enrichment.supplementMappingTitle"))}</h2>
        <div class="muted">${esc(t("enrichment.supplementMapLater"))}</div>
        <div class="mapping-tools">
          <button type="button" id="prepareSupplementDataInlineBtn">${esc(t("enrichment.prepareSupplement"))}</button>
          <button type="button" class="secondary" id="backToProductMappingBtn">${esc(t("enrichment.backToProducts"))}</button>
        </div>
        <div id="supplementMappingStatus" class="status"></div>
      </div>`;
    }

    function collectChoiceMap(row) {
      const hidden = row?.querySelector("[data-cleanup='choiceMap']");
      const map = parseChoiceMap(hidden?.value || "");
      for (const select of row?.querySelectorAll("[data-choice-map-target]") || []) {
        const source = select.dataset.choiceSource || "";
        if (!source) continue;
        if (select.value) map[source] = select.value;
        else delete map[source];
      }
      if (hidden) hidden.value = formatChoiceMap(map);
      return map;
    }

    function addTargetUsage(usage, targetPath, source, value) {
      if (!targetPath || targetPath === "ignore") return;
      if (!usage[targetPath]) usage[targetPath] = { sources: [], values: [] };
      if (source?.label && !usage[targetPath].sources.some(item => item.kind === source.kind && item.label === source.label)) {
        usage[targetPath].sources.push(source);
      }
      const text = String(value ?? "").trim();
      if (text && !usage[targetPath].values.includes(text)) usage[targetPath].values.push(text);
    }

    function buildTargetUsagePreview(rows = null) {
      const usage = {};
      if (activeMode !== "products" || !productMappingProfile) return usage;
      const previewRows = rows || mappedRowsForPreview();
      for (const entry of previewRows) {
        for (const [sourceColumn, item] of Object.entries(productMappingProfile || {})) {
          if (sourceColumn.startsWith("_")) continue;
          if (Array.isArray(entry.variants) && mappingItemIsTypeSeries(item)) continue;
          const actualSourceColumn = item.source_column || sourceColumn.split("::extract::")[0];
          const targetPath = item.target_path || "";
          if (!targetPath || targetPath === "ignore") continue;
          addTargetUsage(
            usage,
            targetPath,
            { kind: "column", label: actualSourceColumn },
            applyCleanup(entry.row[actualSourceColumn], cleanupWithModelUnit(item))
          );
        }
        for (const variantRow of entry.variants || []) {
          for (const [sourceColumn, item] of Object.entries(productMappingProfile || {})) {
            if (sourceColumn.startsWith("_") || !mappingItemIsTypeSeries(item)) continue;
            const actualSourceColumn = item.source_column || sourceColumn.split("::extract::")[0];
            const targetPath = item.target_path || "";
            if (!targetPath || targetPath === "ignore") continue;
            addTargetUsage(
              usage,
              targetPath,
              { kind: "column", label: actualSourceColumn },
              applyCleanup(variantRow[actualSourceColumn], cleanupWithModelUnit(item))
            );
          }
        }
        for (const [targetPath, value] of Object.entries(entry.context || {})) {
          const meta = entry.contextMeta?.[targetPath] || {};
          addTargetUsage(
            usage,
            targetPath,
            { kind: "rule", label: meta.sourceColumn || cleanModelLabel(targetPath) },
            value
          );
        }
      }
      return usage;
    }

    function refreshTargetStructure() {
      const target = $("targetStructure");
      if (!target) return;
      target.innerHTML = renderTargetStructure(targetFieldsForMode(activeMode), buildTargetUsagePreview());
    }

    const MODEL_GROUP_LABELS = {
      pl: {
        "product identity": "Identyfikacja produktu",
        "classification": "Klasyfikacja",
        "descriptions": "Opisy",
        "documents and references": "Dokumenty i odnoĹ›niki",
        "packages": "Opakowania",
        "type series": "Typoszereg"
      },
      en: {
        "product identity": "Product identity",
        "classification": "Classification",
        "descriptions": "Descriptions",
        "documents and references": "Documents and references",
        "packages": "Packages",
        "type series": "Type series"
      }
    };

    const MODEL_TOKEN_LABELS = {
      pl: {
        "product": "Produkt",
        "type_series": "Typoszereg",
        "category": "kategoria",
        "packages": "opakowania",
        "documents": "dokumenty",
        "name": "nazwa",
        "code": "kod",
        "unit": "jednostka",
        "value": "wartoĹ›Ä‡",
        "description": "opis",
        "manufacturer": "producent",
        "product_url": "link do strony www",
        "properties": "wĹ‚aĹ›ciwoĹ›ci",
        "application": "zastosowanie",
        "usage_method": "sposĂłb uĹĽycia",
        "norms": "normy",
        "raw_text": "tekst ĹşrĂłdĹ‚owy",
        "weight": "waga",
        "capacity": "pojemnoĹ›Ä‡",
        "variant_code": "kod wariantu",
        "variant_name": "nazwa wariantu",
        "thickness": "gruboĹ›Ä‡",
        "lambda_value": "lambda",
        "density": "gÄ™stoĹ›Ä‡",
        "vapor_permeability_mu": "mu",
        "specific_heat": "ciepĹ‚o wĹ‚aĹ›ciwe",
        "additional_properties": "pozostaĹ‚e cechy"
      },
      en: {
        "product": "Product",
        "type_series": "Type series",
        "category": "category",
        "packages": "packages",
        "documents": "documents",
        "name": "name",
        "code": "code",
        "unit": "unit",
        "value": "value",
        "description": "description",
        "manufacturer": "manufacturer",
        "product_url": "website link",
        "properties": "properties",
        "application": "application",
        "usage_method": "usage method",
        "norms": "norms",
        "raw_text": "source text",
        "weight": "weight",
        "capacity": "capacity",
        "variant_code": "variant code",
        "variant_name": "variant name",
        "thickness": "thickness",
        "lambda_value": "lambda",
        "density": "density",
        "vapor_permeability_mu": "mu",
        "specific_heat": "specific heat",
        "additional_properties": "additional properties"
      }
    };

    function displayGroupName(group) {
      const text = String(group ?? "").trim();
      const normalized = text.toLowerCase();
      return MODEL_GROUP_LABELS[currentLang]?.[normalized] || text;
    }

    function cleanModelLabel(value) {
      const text = String(value ?? "").trim();
      if (!text) return "";
      const groupLabel = MODEL_GROUP_LABELS[currentLang]?.[text.toLowerCase()];
      if (groupLabel) return groupLabel;
      if (!/[._\\[\\]]/.test(text)) return text;
      const tokenLabels = MODEL_TOKEN_LABELS[currentLang] || MODEL_TOKEN_LABELS.pl;
      return text
        .replaceAll("[]", "")
        .split(/[./]+/)
        .filter(Boolean)
        .map(token => tokenLabels[token] || token.replaceAll("_", " "))
        .join(" / ");
    }

    function fieldIsTypeSeries(field) {
      const key = String(field?.key || "");
      const group = String(field?.group || "").toLowerCase();
      return key.startsWith("type_series[]") || group.includes("type series") || group.includes("typoszereg");
    }

    function targetPathIsTypeSeries(targetPath) {
      const target = String(targetPath || "");
      const field = targetFieldByKey(targetFieldsForMode("products"), target) || targetFieldByKey(activeProductModelFields, target);
      return fieldIsTypeSeries(field) || target.startsWith("type_series[]") || target.startsWith("type_series.");
    }

    function modelUnitForTarget(targetPath) {
      const field = targetFieldByKey(targetFieldsForMode("products"), targetPath) || targetFieldByKey(activeProductModelFields, targetPath);
      return field?.unit || "";
    }

    function cleanupWithModelUnit(item) {
      const cleanup = { ...(item?.cleanup || {}) };
      const targetUnit = cleanup.targetUnit || item?.target_unit || modelUnitForTarget(item?.target_path || "");
      if (targetUnit) cleanup.targetUnit = targetUnit;
      return cleanup;
    }

    function cleanupValueOnly(item) {
      const cleanup = cleanupWithModelUnit(item);
      delete cleanup.targetUnit;
      delete cleanup.target_unit;
      delete cleanup.unit;
      delete cleanup.unitSourceColumn;
      delete cleanup.unit_source_column;
      return cleanup;
    }

    function mappingItemIsTypeSeries(item) {
      const target = String(item?.target_path || "");
      const group = String(item?.target_group || item?.group || "").toLowerCase();
      return targetPathIsTypeSeries(target) || group.includes("type series") || group.includes("typoszereg");
    }

    function targetOptions(targetFields, selected, mode) {
      const blockedTargets = mode === "products" ? rowRuleTargetPaths(rowRuleList(productMappingProfile?._row_rules || {})) : new Set();
      const base = [
        ["ignore", t("mapping.ignore")]
      ];
      const baseOptions = base
        .map(([value, label]) => `<option value="${esc(value)}" data-label="${esc(label)}" data-group=""${value === selected ? " selected" : ""}>${esc(label)}</option>`)
        .join("");
      const groupedOptions = Object.entries(fieldGroups(targetFields)).map(([group, fields]) => {
        const options = fields
          .map(field => `<option value="${esc(field.key)}" data-label="${esc(cleanModelLabel(field.label))}" data-group="${esc(group)}"${field.key === selected ? " selected" : ""}${blockedTargets.has(field.key) && field.key !== selected ? " disabled" : ""}>${esc(cleanModelLabel(field.label))}${field.required ? " *" : ""}</option>`)
          .join("");
        return `<optgroup label="${esc(displayGroupName(group))}">${options}</optgroup>`;
      }).join("");
      return baseOptions + groupedOptions;
    }

    function ruleTargetOptions(targetFields, selected) {
      const fields = targetFields || [];
      const selectedValue = selected || "product.category[].value";
      const baseOption = `<option value="product.category[].value"${selectedValue === "product.category[].value" ? " selected" : ""}>${esc(cleanModelLabel("product.category[].value"))}</option>`;
      const groupedOptions = Object.entries(fieldGroups(fields)).map(([group, groupFields]) => {
        const options = groupFields
          .filter(field => !String(field.key || "").startsWith("type_series[]") && field.key !== "product.category[].value")
          .map(field => `<option value="${esc(field.key)}"${field.key === selectedValue ? " selected" : ""}>${esc(cleanModelLabel(field.label))}${field.required ? " *" : ""}</option>`)
          .join("");
        return options ? `<optgroup label="${esc(displayGroupName(group))}">${options}</optgroup>` : "";
      }).join("");
      return baseOption + groupedOptions;
    }

    function columnOptions(columns, selected) {
      const options = [`<option value="">${esc(t("none"))}</option>`].concat((columns || []).map(column => {
        return `<option value="${esc(column)}"${column === selected ? " selected" : ""}>${esc(column)}</option>`;
      }));
      return options.join("");
    }

    function applyCleanup(value, rule) {
      let current = displayCellValue(value);
      if (rule.trim) current = current.trim();
      if (rule.removeText) current = current.split(rule.removeText).join("");
      if (rule.replaceFrom) current = current.split(rule.replaceFrom).join(rule.replaceTo || "");
      if (rule.splitBy) {
        const parts = current.split(rule.splitBy);
        const part = Number.parseInt(rule.splitPart || "1", 10);
        current = part >= 1 && part <= parts.length ? parts[part - 1].trim() : "";
      }
      if (rule.decimalComma) current = current.replaceAll(",", ".");
      if (rule.parseNumber) {
        const match = current.match(new RegExp("[-+]?\\\\d*\\\\.?\\\\d+"));
        current = match ? match[0] : "";
      }
      if (rule.unitConversionFactor && current !== "") {
        const factor = Number.parseFloat(String(rule.unitConversionFactor).replace(",", "."));
        const number = Number.parseFloat(String(current).replace(",", "."));
        if (Number.isFinite(factor) && Number.isFinite(number)) {
          current = formatConvertedNumber(number * factor);
        }
      }
      let sourceUnit = rule.unit || "";
      if (!sourceUnit && rule.unitSourceColumn && activeTable?.sample_rows?.[0]) {
        sourceUnit = displayCellValue(activeTable.sample_rows[0][rule.unitSourceColumn] || "");
      }
      const unit = rule.targetUnit || sourceUnit;
      if (unit && current !== "") current = `${current} ${unit}`;
      return current;
    }

    function formatConvertedNumber(value) {
      if (!Number.isFinite(value)) return "";
      return Number(value.toPrecision(12)).toString();
    }

    function parseChoiceMap(text) {
      const result = {};
      for (const line of String(text || "").split(/\\r?\\n/)) {
        const trimmed = line.trim();
        if (!trimmed) continue;
        const separator = trimmed.includes("=>") ? "=>" : "=";
        const parts = trimmed.split(separator);
        if (parts.length < 2) continue;
        const source = parts.shift().trim();
        const target = parts.join(separator).trim();
        if (source && target) result[source] = target;
      }
      return result;
    }

    function formatChoiceMap(map) {
      return Object.entries(map || {}).map(([source, target]) => `${source} = ${target}`).join("\\n");
    }

    function collectMapping(mode) {
      const result = {};
      const profile = {};
      const rowRules = mode === "products" ? collectRowRules() : { rules: [] };
      const ruleOwnedColumns = mode === "products" ? columnsHandledByRowRules(rowRules.rules || []) : new Set();
      const ruleOwnedTargets = mode === "products" ? rowRuleTargetPaths(rowRules.rules || []) : new Set();
      for (const select of document.querySelectorAll(`select[data-map-mode="${mode}"]`)) {
        const row = select.closest(".mapping-row");
        const sourceSelect = row?.querySelector("[data-source-column-select]");
        const sourceColumn = sourceSelect ? sourceSelect.value : select.dataset.sourceColumn;
        const targetPath = select.dataset.fixedTargetPath || select.value;
        if (row) row.dataset.sourceColumn = sourceColumn || "";
        if (ruleOwnedColumns.has(sourceColumn)) continue;
        if (ruleOwnedTargets.has(targetPath)) {
          if (!select.dataset.fixedTargetPath) select.value = "ignore";
          continue;
        }
        if (!sourceColumn || !targetPath || targetPath === "ignore") {
          if (row) {
            const beforeTarget = row.querySelector("[data-preview='before']");
            const afterTarget = row.querySelector("[data-preview='after']");
            if (beforeTarget) beforeTarget.innerHTML = "";
            if (afterTarget) afterTarget.innerHTML = "";
            const selectedField = targetFieldByKey(targetFieldsForMode(mode), targetPath);
            const choiceEditor = row.querySelector("[data-choice-map-editor]");
            if (choiceEditor) choiceEditor.outerHTML = renderChoiceMapEditor(selectedField, activeTable, "", collectChoiceMap(row), {});
          }
          continue;
        }
        const instance = row.dataset.mapInstance || "0";
        const profileKey = row.dataset.profileKey || (instance === "0" ? sourceColumn : `${sourceColumn}::extract::${instance}`);
        const selectedOption = select.selectedOptions?.[0];
        const selectedField = targetFieldByKey(targetFieldsForMode(mode), targetPath);
        const cleanup = cleanupFromMappingRow(row, selectedField);
        let choiceMap = collectChoiceMap(row);
        const before = previewRowForMapping(selectedField)?.[sourceColumn] ?? "";
        const after = applyCleanup(before, cleanup);
        row.querySelector("[data-preview='before']").innerHTML = renderLinkedText(before, { limit: 700 });
        row.querySelector("[data-preview='after']").innerHTML = renderLinkedText(after, { limit: 700 });
        const choiceEditor = row.querySelector("[data-choice-map-editor]");
        if (choiceEditor) {
          choiceEditor.outerHTML = renderChoiceMapEditor(selectedField, activeTable, sourceColumn, choiceMap, cleanup);
          choiceMap = collectChoiceMap(row);
        }
        const choicePreviewTarget = row.querySelector("[data-choice-preview]");
        if (choicePreviewTarget) {
          choicePreviewTarget.innerHTML = renderChoicePreview(selectedField, after, choiceMap);
        }
        result[profileKey] = targetPath;
        profile[profileKey] = {
          source_column: sourceColumn,
          target_path: targetPath,
          target_label: selectedField?.label || selectedOption?.dataset?.label || selectedOption?.textContent?.replace(" *", "") || "",
          target_group: selectedField?.group || selectedOption?.dataset?.group || "",
          target_value_kind: selectedField?.value_kind || "free_text",
          target_options: selectedField?.options || [],
          target_unit: selectedField?.unit || "",
          choice_map: choiceMap,
          cleanup
        };
      }
      if (mode === "products") {
        profile._row_rules = rowRules;
        productMapping = result;
        productMappingProfile = profile;
        refreshRuleOwnedRows(rowRules.rules || []);
        refreshRuleOwnedTargetOptions(ruleOwnedTargets);
        validateMappingConflicts(profile);
      } else if (mode === "supplement") {
        supplementMapping = result;
        supplementMappingProfile = profile;
        validateMappingConflicts(profile);
      }
      renderProductPreview();
      refreshTargetStructure();
      attachChoiceMapEvents(mode);
      return result;
    }

    function mappingConflictKey(item) {
      const target = item?.target_path || "";
      if (!target || target === "ignore") return "";
      return target;
    }

    function mappingRowForProfileEntry(profileKey, item) {
      const sourceColumn = item?.source_column || String(profileKey).split("::extract::")[0];
      const instance = extractionInstanceFromKey(profileKey);
      return Array.from(document.querySelectorAll(".mapping-row[data-source-column]"))
        .find(row => (row.dataset.profileKey && row.dataset.profileKey === String(profileKey)) || (row.dataset.sourceColumn === sourceColumn && (row.dataset.mapInstance || "0") === String(instance)));
    }

    function validateMappingConflicts(profile = productMappingProfile || {}) {
      for (const row of document.querySelectorAll(".mapping-row.has-conflict")) {
        row.classList.remove("has-conflict");
      }
      for (const validation of document.querySelectorAll("[data-validation='duplicateTarget']")) {
        validation.textContent = "";
      }

      const byTarget = new Map();
      for (const [profileKey, item] of Object.entries(profile || {})) {
        if (String(profileKey).startsWith("_")) continue;
        const key = mappingConflictKey(item);
        if (!key) continue;
        if (!byTarget.has(key)) byTarget.set(key, []);
        byTarget.get(key).push({ profileKey, item });
      }

      const conflicts = Array.from(byTarget.values()).filter(entries => entries.length > 1);
      for (const entries of conflicts) {
        for (const entry of entries) {
          const row = mappingRowForProfileEntry(entry.profileKey, entry.item);
          if (!row) continue;
          row.classList.add("has-conflict");
          const validation = row.querySelector("[data-validation='duplicateTarget']");
          if (validation) validation.textContent = t("mapping.duplicateTarget");
        }
      }
      return conflicts;
    }

    function hasBlockingMappingConflicts() {
      return validateMappingConflicts(productMappingProfile || {}).length > 0;
    }

    function collectRowRules() {
      const panel = $("rowRulesPanel");
      if (!panel) return { rules: [] };
      const rules = Array.from(document.querySelectorAll(".row-rule")).map(rule => ({
        row_mode: rule.querySelector("[data-row-rule='rowMode']")?.value || "product_variants",
        row_type_column: rule.querySelector("[data-row-rule='rowTypeColumn']")?.value || "",
        product_row_values: rule.querySelector("[data-row-rule='productRowValues']")?.value || "",
        group_row_values: rule.querySelector("[data-row-rule='groupRowValues']")?.value || "",
        id_column: rule.querySelector("[data-row-rule='idColumn']")?.value || "",
        parent_id_column: rule.querySelector("[data-row-rule='parentIdColumn']")?.value || ""
      })).filter(isActiveRowRule);
      return { rules };
    }

    function isActiveRowRule(rule) {
      return [
        "row_type_column",
        "product_row_values",
        "group_row_values",
        "id_column",
        "parent_id_column"
      ].some(key => String(rule?.[key] || "").trim() !== "");
    }

    function columnsHandledByRowRules(rules) {
      const columns = new Set();
      for (const rule of rules || []) {
        if (rule.row_type_column) columns.add(rule.row_type_column);
      }
      return columns;
    }

    function rowRuleTargetPaths(rules) {
      return new Set();
    }

    function refreshRuleOwnedTargetOptions(targets) {
      const blocked = targets || new Set();
      for (const select of document.querySelectorAll('select[data-map-mode="products"]')) {
        if (select.dataset.fixedTargetPath) continue;
        if (blocked.has(select.value)) select.value = "ignore";
        for (const option of select.options || []) {
          option.disabled = blocked.has(option.value);
        }
      }
    }

    function refreshRuleOwnedRows(rules) {
      const columns = columnsHandledByRowRules(rules || []);
      const targets = rowRuleTargetPaths(rules || []);
      for (const row of document.querySelectorAll(".mapping-row[data-source-column]")) {
        const sourceColumn = row.querySelector("[data-source-column-select]")?.value || row.dataset.sourceColumn || "";
        row.classList.toggle("rule-owned-row", columns.has(sourceColumn));
      }
      const notice = $("ruleOwnedNotice");
      if (notice) {
        const owned = Array.from(columns).concat(Array.from(targets).map(target => cleanModelLabel(target)));
        notice.innerHTML = owned.length ? `<div class="notice">${esc(t("mapping.usedByRules"))}: ${owned.map(item => esc(item)).join(", ")}</div>` : "";
      }
      const summary = $("rowRulesSummary");
      if (summary) {
        const activeRules = (rules || []).filter(isActiveRowRule).length;
        summary.textContent = activeRules ? `${t("rows.summary")}: ${activeRules}` : t("rows.summaryEmpty");
      }
    }

    function rowRuleList(rowRules) {
      if (!rowRules) return [];
      if (Array.isArray(rowRules)) return rowRules;
      if (Array.isArray(rowRules.rules)) return rowRules.rules;
      return Object.keys(rowRules).length ? [rowRules] : [];
    }

    function normalizedValues(text) {
      return new Set(String(text || "").split(",").map(item => item.trim().toLowerCase()).filter(Boolean));
    }

    function mappedRowsForPreview() {
      if (!activeTable || !productMappingProfile) return [];
      const rules = rowRuleList(productMappingProfile._row_rules || {});
      if (!rules.length) return (activeTable.sample_rows || []).map(row => ({ row, context: {} }));
      const rows = activeTable.sample_rows || [];
      const variantRule = rules.find(rule => rule.row_mode === "product_variants");
      if (variantRule) return mappedRowsForProductVariantsPreview(rows, variantRule);
      const groupContextsById = rules.map(() => ({}));
      const mapped = [];
      rules.forEach((rule, index) => {
        for (const row of rows) {
          if (!isGroupRowForRule(row, rule)) continue;
          const groupId = String(row[rule.id_column] || "").trim().toLowerCase();
          const groupValue = row[rule.group_source_column];
          if (groupId && groupValue !== undefined && groupValue !== null && groupValue !== "") {
            groupContextsById[index][groupId] = groupValue;
          }
        }
      });
      const hasProductFilters = rules.some(rule => normalizedValues(rule.product_row_values).size || normalizedPrefixes(rule.product_prefixes).length);
      for (const row of rows) {
        const groupMatches = rules
          .map((rule, index) => isGroupRowForRule(row, rule) ? index : -1)
          .filter(index => index >= 0);
        if (groupMatches.length) {
          continue;
        }
        if (hasProductFilters && !rules.some(rule => isProductRowForRule(row, rule))) continue;
        const rowContext = {};
        const rowContextMeta = {};
        rules.forEach((rule, index) => {
          const ruleHasProductFilter = normalizedValues(rule.product_row_values).size > 0;
          if (!ruleHasProductFilter || isProductRowForRule(row, rule)) {
            const productIdValue = rule.product_id_column ? row[rule.product_id_column] : "";
            if (productIdValue !== undefined && productIdValue !== null && productIdValue !== "") {
              rowContext["product.code.value"] = productIdValue;
              rowContextMeta["product.code.value"] = { sourceColumn: rule.product_id_column || t("rows.rule") };
            }
            const productNameValue = rule.product_name_column ? row[rule.product_name_column] : "";
            if (productNameValue !== undefined && productNameValue !== null && productNameValue !== "") {
              rowContext["product.name.value"] = productNameValue;
              rowContextMeta["product.name.value"] = { sourceColumn: rule.product_name_column || t("rows.rule") };
            }
          }
          const target = rule.group_target_path || "product.category[].value";
          const parentContext = groupContextsById[index][String(row[rule.parent_id_column] || "").trim().toLowerCase()];
          if (parentContext !== undefined && parentContext !== null && parentContext !== "") {
            rowContext[target] = parentContext;
            rowContextMeta[target] = { sourceColumn: rule.group_source_column || rule.parent_id_column || t("rows.rule") };
          }
        });
        mapped.push({ row, context: rowContext, contextMeta: rowContextMeta });
      }
      return mapped.length ? mapped : rows.map(row => ({ row, context: {} }));
    }

    function productVariantRuleStats(rows, rule) {
      const productIds = new Set();
      let productRows = 0;
      let variantRows = 0;
      let matchedVariants = 0;
      let orphanVariants = 0;
      const hasParentReference = Boolean(rule?.id_column && rule?.parent_id_column);
      for (const row of rows || []) {
        if (!isParentProductRowForVariantRule(row, rule)) continue;
        productRows += 1;
        const productId = String(row[rule.id_column] || "").trim().toLowerCase();
        if (productId) productIds.add(productId);
      }
      for (const row of rows || []) {
        if (!isVariantRowForVariantRule(row, rule)) continue;
        variantRows += 1;
        if (!hasParentReference) {
          matchedVariants += 1;
          continue;
        }
        const parentId = String(row[rule.parent_id_column] || "").trim().toLowerCase();
        if (parentId && productIds.has(parentId)) matchedVariants += 1;
        else orphanVariants += 1;
      }
      return { productRows, variantRows, matchedVariants, orphanVariants };
    }

    function renderRowRuleStats(rules) {
      const rows = activeTable?.sample_rows || [];
      const variantRule = rowRuleList(rules || {}).find(rule => rule.row_mode === "product_variants");
      if (!variantRule) return "";
      const stats = productVariantRuleStats(rows, variantRule);
      return `<div class="mapping-check-meta">
        <span class="pill">${esc(t("rows.statsProductRows"))}: ${esc(stats.productRows)}</span>
        <span class="pill">${esc(t("rows.statsVariantRows"))}: ${esc(stats.variantRows)}</span>
        <span class="pill">${esc(t("rows.statsMatchedVariants"))}: ${esc(stats.matchedVariants)}</span>
        <span class="pill">${esc(t("rows.statsOrphanVariants"))}: ${esc(stats.orphanVariants)}</span>
      </div>`;
    }

    function mappedRowsForProductVariantsPreview(rows, rule) {
      const productsById = new Map();
      const orderedIds = [];
      let currentProductId = "";
      const hasParentReference = Boolean(rule.id_column && rule.parent_id_column);
      if (hasParentReference) {
        for (const row of rows) {
          if (!isParentProductRowForVariantRule(row, rule)) continue;
          const productId = String(row[rule.id_column] || "").trim().toLowerCase();
          if (!productId) continue;
          if (!productsById.has(productId)) orderedIds.push(productId);
          productsById.set(productId, { row, context: {}, contextMeta: {}, variants: [] });
        }
        for (const row of rows) {
          if (!isVariantRowForVariantRule(row, rule)) continue;
          const parentId = String(row[rule.parent_id_column] || "").trim().toLowerCase();
          const parent = productsById.get(parentId);
          if (!parent) continue;
          parent.variants.push(row);
        }
      } else {
        for (const row of rows) {
          if (isParentProductRowForVariantRule(row, rule)) {
            currentProductId = `product-${orderedIds.length + 1}`;
            orderedIds.push(currentProductId);
            productsById.set(currentProductId, { row, context: {}, contextMeta: {}, variants: [] });
            continue;
          }
          if (isVariantRowForVariantRule(row, rule) && currentProductId) {
            productsById.get(currentProductId).variants.push(row);
          }
        }
      }
      return orderedIds.map(id => productsById.get(id)).filter(Boolean);
    }

    function isGroupRowForRule(row, rule) {
      const rowTypeColumn = rule.row_type_column || "";
      const groupValues = normalizedValues(rule.group_row_values);
      const rowType = String(row[rowTypeColumn] || "").trim().toLowerCase();
      return Boolean(rowTypeColumn && groupValues.has(rowType));
    }

    function isProductRowForRule(row, rule) {
      const rowTypeColumn = rule.row_type_column || "";
      const productValues = normalizedValues(rule.product_row_values);
      const rowType = String(row[rowTypeColumn] || "").trim().toLowerCase();
      return Boolean(rowTypeColumn && productValues.has(rowType));
    }

    function isParentProductRowForVariantRule(row, rule) {
      return isProductRowForRule(row, rule);
    }

    function isVariantRowForVariantRule(row, rule) {
      return isGroupRowForRule(row, rule);
    }

    function sampleValueFor(sourceColumn, profileItem) {
      const actualSourceColumn = profileItem?.source_column || sourceColumn.split("::extract::")[0];
      const before = previewRowForMapping(profileItem)?.[actualSourceColumn] ?? "";
      return applyCleanup(before, cleanupWithModelUnit(profileItem));
    }

    function labelForTarget(targetPath) {
      const field = targetFieldByKey(targetFieldsForMode("products"), targetPath);
      if (field) return cleanModelLabel(field.label || field.key);
      const option = Array.from(document.querySelectorAll("select[data-map-mode] option"))
        .find(candidate => candidate.value === targetPath);
      return option ? cleanModelLabel(option.textContent.replace(" *", "")) : cleanModelLabel(targetPath);
    }

    function currentPreviewEntry() {
      const rows = mappedRowsForPreview();
      if (!rows.length) return { row: activeTable?.sample_rows?.[0] || {}, variants: [] };
      const index = Math.min(Math.max(productPreviewIndex, 0), rows.length - 1);
      return rows[index] || rows[0] || { row: activeTable?.sample_rows?.[0] || {}, variants: [] };
    }

    function previewRowForMapping(targetOrItem) {
      const entry = currentPreviewEntry();
      const isTypeSeries = targetOrItem?.target_path
        ? mappingItemIsTypeSeries(targetOrItem)
        : fieldIsTypeSeries(targetOrItem);
      if (isTypeSeries && Array.isArray(entry.variants) && entry.variants.length) {
        return entry.variants[0] || {};
      }
      return entry.row || {};
    }

    function cleanupFromMappingRow(row, selectedField) {
      return {
        trim: row.querySelector("[data-cleanup='trim']")?.checked,
        removeText: row.querySelector("[data-cleanup='removeText']")?.value || "",
        replaceFrom: row.querySelector("[data-cleanup='replaceFrom']")?.value || "",
        replaceTo: row.querySelector("[data-cleanup='replaceTo']")?.value || "",
        splitBy: row.querySelector("[data-cleanup='splitBy']")?.value || "",
        splitPart: row.querySelector("[data-cleanup='splitPart']")?.value || "1",
        decimalComma: row.querySelector("[data-cleanup='decimalComma']")?.checked,
        parseNumber: row.querySelector("[data-cleanup='parseNumber']")?.checked,
        unit: row.querySelector("[data-cleanup='unit']")?.value || "",
        unitSourceColumn: row.querySelector("[data-cleanup='unitSourceColumn']")?.value || "",
        targetUnit: row.querySelector("[data-cleanup='targetUnit']")?.value || selectedField?.unit || "",
        unitConversionFactor: row.querySelector("[data-cleanup='unitConversionFactor']")?.value || ""
      };
    }

    function mappedObjectForPreview(row, context) {
      const result = {};
      for (const [sourceColumn, item] of Object.entries(productMappingProfile || {})) {
        if (sourceColumn.startsWith("_")) continue;
        if (!item.target_path || item.target_path === "ignore") continue;
        const actualSourceColumn = item.source_column || sourceColumn.split("::extract::")[0];
        result[item.target_path] = applyCleanup(row[actualSourceColumn], cleanupWithModelUnit(item));
      }
      for (const [target, value] of Object.entries(context || {})) {
        result[target] = value;
      }
      return result;
    }

    function typeSeriesFieldName(targetPath) {
      return cleanModelLabel(String(targetPath || "")
        .replace("type_series.", "")
        .replace("type series.", ""));
    }

    function typeSeriesColumnsFromProfile(modelFields = []) {
      const columns = [];
      for (const field of modelFields || []) {
        const key = field.key;
        const mappedItem = Object.values(productMappingProfile || {}).find((item) => item?.target_path === key);
        columns.push({
          key,
          label: cleanModelLabel(field.label || key),
          sourceColumn: mappedItem?.source_column || "",
          unit: mappedItem?.target_unit || field.unit || ""
        });
      }
      for (const [sourceColumn, item] of Object.entries(productMappingProfile || {})) {
        if (sourceColumn.startsWith("_")) continue;
        if (!item.target_path || !(mappingItemIsTypeSeries(item) || columns.some(column => column.key === item.target_path))) continue;
        const actualSourceColumn = item.source_column || sourceColumn.split("::extract::")[0];
        const key = item.target_path;
        if (!columns.some(column => column.key === key)) {
          columns.push({
            key,
            label: labelForTarget(item.target_path),
            sourceColumn: actualSourceColumn,
            unit: item.target_unit || modelUnitForTarget(item.target_path)
          });
        }
      }
      const variantRule = rowRuleList(productMappingProfile?._row_rules || {}).find(rule => rule.row_mode === "product_variants");
      if (variantRule?.variant_id_column) {
        const existing = columns.find(column => column.key === "type_series[].variant_code.value");
        if (existing) {
          existing.sourceColumn = variantRule.variant_id_column;
        } else {
          columns.unshift({
            key: "type_series[].variant_code.value",
            label: cleanModelLabel("type_series[].variant_code.value"),
            sourceColumn: variantRule.variant_id_column,
            unit: modelUnitForTarget("type_series[].variant_code.value")
          });
        }
      }
      if (variantRule?.variant_name_column) {
        const existing = columns.find(column => column.key === "type_series[].variant_name.value");
        if (existing) {
          existing.sourceColumn = variantRule.variant_name_column;
        } else {
          columns.unshift({
            key: "type_series[].variant_name.value",
            label: cleanModelLabel("type_series[].variant_name.value"),
            sourceColumn: variantRule.variant_name_column,
            unit: modelUnitForTarget("type_series[].variant_name.value")
          });
        }
      }
      return columns;
    }

    function renderTypeSeriesPreviewTable(previewRows, modelFields = [], maxRows = 3, productKey = "") {
      const columns = typeSeriesColumnsFromProfile(modelFields);
      const typeSeriesEnrichments = productKey && !showMainMappingOnly
        ? plannedEnrichmentsForProduct(productKey).filter(item => item.is_type_series)
        : [];
      for (const item of typeSeriesEnrichments) {
        if (!item.target_path || columns.some(column => column.key === item.target_path)) continue;
        columns.push({
          key: item.target_path,
          label: item.label || labelForTarget(item.target_path),
          sourceColumn: "",
          unit: modelUnitForTarget(item.target_path)
        });
      }
      if (!columns.length) return `<div class="type-series-preview-scroll"><table class="type-series-preview-table"><tbody><tr><td>${esc(t("missing.typeSeries"))}</td></tr></tbody></table></div>`;
      const variantRule = rowRuleList(productMappingProfile?._row_rules || {}).find(rule => rule.row_mode === "product_variants");
      const variantEntries = (previewRows || []).flatMap(entry =>
        Array.isArray(entry.variants) ? entry.variants.map(row => ({ row })) : []
      );
      const sourceEntries = variantEntries.length ? variantEntries : (variantRule ? [] : (previewRows || []));
      const rows = sourceEntries.slice(0, maxRows).map((entry, index) => {
        const valuesByKey = {};
        for (const [sourceColumn, item] of Object.entries(productMappingProfile || {})) {
          if (sourceColumn.startsWith("_")) continue;
          if (!item.target_path || !mappingItemIsTypeSeries(item) || !columns.some(column => column.key === item.target_path)) continue;
          const actualSourceColumn = item.source_column || sourceColumn.split("::extract::")[0];
          valuesByKey[item.target_path] = applyCleanup(entry.row[actualSourceColumn], cleanupValueOnly(item));
        }
        if (variantRule?.variant_id_column) {
          valuesByKey["type_series[].variant_code.value"] = displayCellValue(entry.row[variantRule.variant_id_column] || "");
        }
        if (variantRule?.variant_name_column) {
          valuesByKey["type_series[].variant_name.value"] = displayCellValue(entry.row[variantRule.variant_name_column] || "");
        }
        const baselineByKey = { ...valuesByKey };
        const addedByKey = {};
        for (const item of typeSeriesEnrichments) {
          if (!item.target_path) continue;
          if (item.apply_to_all_variants || item.type_series_row_index === index) {
            valuesByKey[item.target_path] = item.value;
            addedByKey[item.target_path] = true;
          }
        }
        const cells = columns.map(column => {
          const value = valuesByKey[column.key] || "";
          const cellValue = manualEditEnabled
            ? inlineManualInput(column.key, value, `data-inline-manual-type-series-row-index="${esc(index)}"`, baselineByKey[column.key] || "")
            : renderLinkedText(value, { limit: 260 });
          return `<td${addedByKey[column.key] ? ` class="enrichment-added-cell"` : ""}>${cellValue}</td>`;
        }).join("");
        return `<tr><td>${esc(index + 1)}</td>${cells}</tr>`;
      }).join("");
      return `<div class="type-series-preview-scroll"><table class="type-series-preview-table">
        <thead><tr><th>#</th>${columns.map(column => `<th>${esc(column.label)}${column.unit ? `<br><span class="muted">${esc(t("preview.unit"))}: ${esc(column.unit)}</span>` : ""}</th>`).join("")}</tr></thead>
        <tbody>${rows || `<tr><td colspan="${esc(columns.length + 1)}">${esc(t("missing.typeSeries"))}</td></tr>`}</tbody>
      </table></div>`;
    }

    function productLabelForPreview(entry, index) {
      const preferredTargets = ["product.name.value", "product.code.value", "product.unit.value"];
      for (const target of preferredTargets) {
        for (const item of Object.values(productMappingProfile || {})) {
          if (!item || item.target_path !== target || mappingItemIsTypeSeries(item)) continue;
          const sourceColumn = item.source_column || "";
          const value = applyCleanup(entry.row?.[sourceColumn], cleanupWithModelUnit(item));
          if (String(value || "").trim()) return `${index + 1}. ${displayCellValue(value)}`;
        }
        const contextValue = entry.context?.[target];
        if (String(contextValue || "").trim()) return `${index + 1}. ${displayCellValue(contextValue)}`;
      }
      return `${t("preview.productCounter")} ${index + 1}`;
    }

    function typicalProductByKey(key) {
      const normalized = normalizeMatchKey(key);
      const meta = typicalProductsForEnrichment.find(product => normalizeMatchKey(product.key) === normalized);
      return meta ? typicalProductsPayloadForEnrichment[meta.index] : null;
    }

    function plannedEnrichmentsForProduct(productKey) {
      const normalizedProductKey = normalizeMatchKey(productKey);
      const rows = [];
      for (const match of enrichmentSession.typical_matches || []) {
        if (normalizeMatchKey(match.product_key) !== normalizedProductKey) continue;
        const typicalProduct = typicalProductByKey(match.typical_key);
        if (!typicalProduct) continue;
        const selected = new Set(match.selected_attributes || []);
        for (const attr of pimProductAttributes(typicalProduct)) {
          const attrKey = typicalAttributeKey(attr);
          if (selected.size && !selected.has(attrKey)) continue;
          if (!attributeIsFromSupplementMapping(attr)) continue;
          rows.push({
            source: match.typical_label || match.typical_key,
            label: typicalAttributeLabel(attr),
            target_path: typicalAttributeModelPath(attr),
            is_type_series: typicalAttributeIsTypeSeries(attr),
            apply_to_all_variants: match.apply_type_series_to_all !== false,
            type_series_row_index: Number.isInteger(match.type_series_row_index) ? match.type_series_row_index : null,
            value: pimAttrValue(attr)
          });
        }
      }
      for (const entry of enrichmentSession.manual_entries || []) {
        if (entry.scope !== "current_product" || normalizeMatchKey(entry.product_key) !== normalizedProductKey) continue;
        rows.push({
          source: currentLang === "pl" ? "rÄ™cznie" : "manual",
          label: labelForTarget(entry.target_path),
          target_path: entry.target_path,
          is_type_series: targetPathIsTypeSeries(entry.target_path),
          apply_to_all_variants: entry.apply_type_series_to_all !== false,
          type_series_row_index: Number.isInteger(entry.type_series_row_index) ? entry.type_series_row_index : null,
          value: entry.value
        });
      }
      return rows;
    }

    function renderTypeSeriesEnrichmentTable(productKey) {
      const rows = plannedEnrichmentsForProduct(productKey).filter(item => item.is_type_series);
      if (!rows.length) return "";
      return `<table>
        <thead><tr><th>${esc(currentLang === "pl" ? "Wariant" : "Variant")}</th><th>${esc(t("preview.field"))}</th><th>${esc(t("preview.cleanedValue"))}</th><th>${esc(currentLang === "pl" ? "ĹąrĂłdĹ‚o" : "Source")}</th></tr></thead>
        <tbody>${rows.map(row => `<tr class="enrichment-added"><td>${esc(row.apply_to_all_variants ? (currentLang === "pl" ? "wszystkie" : "all") : String((row.type_series_row_index ?? 0) + 1))}</td><td>${esc(row.label)}</td><td>${renderLinkedText(row.value, { limit: 260 })}</td><td>${esc(row.source)}</td></tr>`).join("")}</tbody>
      </table>`;
    }

    function renderPlannedEnrichments(productKey) {
      const rows = plannedEnrichmentsForProduct(productKey);
      return `<div class="planned-enrichment">
        <h2 class="title">${esc(t("enrichment.plannedTitle"))}</h2>
        <table>
          <thead><tr><th>${esc(currentLang === "pl" ? "ĹąrĂłdĹ‚o" : "Source")}</th><th>${esc(t("preview.field"))}</th><th>${esc(t("preview.cleanedValue"))}</th></tr></thead>
          <tbody>${rows.map(row => `<tr><td>${esc(row.source)}</td><td>${esc(row.label)}</td><td>${renderLinkedText(row.value, { limit: 360 })}</td></tr>`).join("") || `<tr><td colspan="3">${esc(t("enrichment.plannedEmpty"))}</td></tr>`}</tbody>
        </table>
      </div>`;
    }

    function renderProductPreview() {
      const panel = $("productPreview");
      if (!panel || activeMode !== "products" || !productMappingProfile) return;
      const previewRows = mappedRowsForPreview();
      if (productPreviewIndex >= previewRows.length) productPreviewIndex = Math.max(0, previewRows.length - 1);
      if (productPreviewIndex < 0) productPreviewIndex = 0;
      const previewEntry = previewRows[productPreviewIndex] || previewRows[0] || { row: activeTable?.sample_rows?.[0] || {}, context: {}, contextMeta: {} };
      const previewRow = previewEntry.row || {};
      const previewContext = previewEntry.context || {};
      const previewContextMeta = previewEntry.contextMeta || {};
      const productRows = [];
      const shownProductTargets = new Set();
      const typeSeriesFields = targetFieldsForMode("products").filter(fieldIsTypeSeries);
      const productKey = productKeyForEnrichmentEntry(previewEntry, productPreviewIndex);
      const productEnrichments = !showMainMappingOnly
        ? plannedEnrichmentsForProduct(productKey).filter(item => !item.is_type_series)
        : [];
      const productEnrichmentByTarget = new Map();
      for (const item of productEnrichments) {
        if (!item.target_path || productEnrichmentByTarget.has(item.target_path)) continue;
        productEnrichmentByTarget.set(item.target_path, item);
      }
      for (const [sourceColumn, item] of Object.entries(productMappingProfile)) {
        if (sourceColumn.startsWith("_")) continue;
        if (!item.target_path || item.target_path === "ignore") continue;
        const actualSourceColumn = item.source_column || sourceColumn.split("::extract::")[0];
        const label = labelForTarget(item.target_path);
        const added = productEnrichmentByTarget.get(item.target_path);
        const baselineValue = applyCleanup(previewRow[actualSourceColumn], cleanupWithModelUnit(item));
        const value = added ? added.value : baselineValue;
        const unit = cleanupWithModelUnit(item).targetUnit || "";
        const row = `<tr${added ? ` class="enrichment-added"` : ""}><td>${esc(label)}${added ? `<br><span class="muted">${esc(added.source)}</span>` : ""}</td><td>${inlineManualInput(item.target_path, value, "", baselineValue)}</td><td>${esc(unit || "-")}</td></tr>`;
        if (mappingItemIsTypeSeries(item)) {
          continue;
        } else {
          shownProductTargets.add(item.target_path);
          productRows.push(row);
        }
      }
      for (const [targetPath, value] of Object.entries(previewContext)) {
        if (targetPathIsTypeSeries(targetPath)) continue;
        const added = productEnrichmentByTarget.get(targetPath);
        shownProductTargets.add(targetPath);
        productRows.push(`<tr${added ? ` class="enrichment-added"` : ""}><td>${esc(cleanModelLabel(targetPath))}${added ? `<br><span class="muted">${esc(added.source)}</span>` : ""}</td><td>${inlineManualInput(targetPath, added ? added.value : value, "", value)}</td><td>${esc(modelUnitForTarget(targetPath) || "-")}</td></tr>`);
      }
      if (!showMainMappingOnly) {
        for (const item of productEnrichments) {
          if (targetPathIsTypeSeries(item.target_path)) continue;
          if (shownProductTargets.has(item.target_path)) continue;
          shownProductTargets.add(item.target_path);
          productRows.push(`<tr class="enrichment-added"><td>${esc(item.label)}<br><span class="muted">${esc(item.source)}</span></td><td>${inlineManualInput(item.target_path, item.value)}</td><td>${esc(modelUnitForTarget(item.target_path || "") || "-")}</td></tr>`);
        }
      }
      if (manualEditEnabled) {
        for (const field of targetFieldsForMode("products")) {
          if (!field?.key || fieldIsTypeSeries(field) || shownProductTargets.has(field.key)) continue;
          shownProductTargets.add(field.key);
          productRows.push(`<tr><td>${esc(cleanModelLabel(field.label || field.key))}</td><td>${inlineManualInput(field.key, "")}</td><td>${esc(field.unit || modelUnitForTarget(field.key) || "-")}</td></tr>`);
        }
      }
      const detectedProducts = previewRows.length;
      const currentProductLabel = detectedProducts ? `${t("preview.productCounter")} ${productPreviewIndex + 1} / ${detectedProducts}` : `0 ${t("preview.sample")}`;
      const productOptions = previewRows.map((entry, index) =>
        `<option value="${esc(index)}"${index === productPreviewIndex ? " selected" : ""}>${esc(productLabelForPreview(entry, index))}</option>`
      ).join("");
      panel.innerHTML = `
        <div class="live-preview-panel">
          <div class="live-preview-header">
            <div>
              <h2>${esc(t("preview.title"))}</h2>
              <div class="muted">${esc(t("preview.help"))}</div>
            </div>
            <div class="mapping-tools">
              <button type="button" class="secondary" data-preview-product="prev"${productPreviewIndex <= 0 ? " disabled" : ""}>${esc(t("preview.previousProduct"))}</button>
              <span class="live-badge">${esc(currentProductLabel)}</span>
              <button type="button" class="secondary" data-preview-product="next"${productPreviewIndex >= detectedProducts - 1 ? " disabled" : ""}>${esc(t("preview.nextProduct"))}</button>
            </div>
          </div>
          <label>${esc(t("preview.chooseProduct"))}
            <select id="productPreviewSelect"${detectedProducts ? "" : " disabled"}>
              ${productOptions || `<option>${esc(t("missing.productFields"))}</option>`}
            </select>
          </label>
          ${mappingWorkspaceTab === "enrichment" ? `<div class="enrichment-preview-options">
            <label class="inline-check">
              <input id="showMainMappingOnly" type="checkbox"${showMainMappingOnly ? " checked" : ""}>
              <span>${esc(currentLang === "pl" ? "Poka\u017c tylko dane z mapowania g\u0142\u00f3wnego" : "Show only main-mapping data")}</span>
            </label>
          </div>` : ""}
          <div class="preview-columns">
            <div>
              <h2 class="title">${esc(t("preview.productFields"))}</h2>
              <table>
                <thead><tr><th>${esc(t("preview.field"))}</th><th>${esc(t("preview.cleanedValue"))}</th><th>${esc(t("preview.unit"))}</th></tr></thead>
                <tbody>${productRows.join("") || `<tr><td colspan='3'>${esc(t("missing.productFields"))}</td></tr>`}</tbody>
              </table>
            </div>
            <div>
              <h2 class="title">${esc(t("preview.typeSeries"))}</h2>
              ${renderTypeSeriesPreviewTable([previewEntry], typeSeriesFields, 3, productKey)}
            </div>
          </div>
        </div>`;
      for (const button of panel.querySelectorAll("[data-preview-product]")) {
        button.onclick = () => {
          productPreviewIndex += button.dataset.previewProduct === "next" ? 1 : -1;
          renderProductPreview();
        };
      }
      const productSelect = $("productPreviewSelect");
      if (productSelect) {
        productSelect.onchange = () => {
          productPreviewIndex = Number.parseInt(productSelect.value || "0", 10) || 0;
          renderProductPreview();
        };
      }
      const showMainOnly = $("showMainMappingOnly");
      if (showMainOnly) {
        showMainOnly.onchange = () => {
          showMainMappingOnly = showMainOnly.checked;
          renderProductPreview();
        };
      }
      updateMappingPreviewValues();
      refreshEnrichmentCurrentProduct();
    }

    function updateMappingPreviewValues() {
      if (!activeTable) return;
      for (const row of document.querySelectorAll(".mapping-row")) {
        const select = row.querySelector("select[data-map-mode]");
        if (!select) continue;
        const sourceSelect = row.querySelector("[data-source-column-select]");
        const sourceColumn = sourceSelect ? sourceSelect.value : select.dataset.sourceColumn;
        const targetPath = select.dataset.fixedTargetPath || select.value;
        const selectedField = targetFieldByKey(targetFieldsForMode(activeMode), targetPath);
        const beforeTarget = row.querySelector("[data-preview='before']");
        const afterTarget = row.querySelector("[data-preview='after']");
        if (!beforeTarget || !afterTarget || !sourceColumn || !selectedField || targetPath === "ignore") continue;
        const cleanup = cleanupFromMappingRow(row, selectedField);
        const before = previewRowForMapping(selectedField)?.[sourceColumn] ?? "";
        const after = applyCleanup(before, cleanup);
        beforeTarget.innerHTML = renderLinkedText(before, { limit: 700 });
        afterTarget.innerHTML = renderLinkedText(after, { limit: 700 });
        const choicePreviewTarget = row.querySelector("[data-choice-preview]");
        if (choicePreviewTarget) {
          choicePreviewTarget.innerHTML = renderChoicePreview(selectedField, after, collectChoiceMap(row));
        }
      }
    }

    function renderMappingCheckHtml(result) {
      const checkedAt = new Date().toLocaleTimeString(currentLang === "pl" ? "pl-PL" : "en-US");
      const rules = rowRuleList(productMappingProfile?._row_rules || {});
      return `
        <div class="notice">
          ${esc(t("mapping.checkApplied"))}
          <div class="mapping-check-meta">
            <span class="pill">${esc(t("mapping.detectedProducts"))}: ${esc(result.length)}</span>
            <span class="pill">${esc(t("mapping.checkedAt"))}: ${esc(checkedAt)}</span>
          </div>
          ${renderRowRuleStats(rules)}
          ${result.length ? "" : `<div class="warn">${esc(t("mapping.noPreviewRows"))}</div>`}
        </div>`;
    }

    function renderMappingCheck() {
      if (activeMode !== "products") return;
      collectMapping("products");
      const rows = mappedRowsForPreview();
      const result = rows.map(entry => mappedObjectForPreview(entry.row, entry.context));
      const target = $("mappingCheckTopResult") || $("mappingCheckResult");
      if (!target) return;
      refreshTargetStructure();
      target.innerHTML = renderMappingCheckHtml(result);
      const oldTarget = $("mappingCheckResult");
      if (oldTarget && oldTarget !== target) oldTarget.innerHTML = "";
      ($("targetStructure") || target).scrollIntoView({ behavior: "smooth", block: "start" });
    }

    function applyRowRules() {
      if (activeMode !== "products") return;
      productPreviewIndex = 0;
      collectMapping("products");
      refreshTargetStructure();
      renderProductPreview();
      const rules = rowRuleList(productMappingProfile?._row_rules || {});
      const columns = Array.from(columnsHandledByRowRules(rules));
      const target = $("mappingCheckTopResult") || $("mappingCheckResult");
      if (target) {
        target.innerHTML = `<div class="notice">${esc(t("rows.applied"))}${columns.length ? `<div class="mapping-check-meta">${columns.map(column => `<span class="pill">${esc(column)}</span>`).join("")}</div>` : ""}${renderRowRuleStats(rules)}</div>`;
      }
    }

    function addColumnExtraction(button) {
      if (!activeTable) return;
      const sourceColumn = button.dataset.addExtraction;
      const rows = Array.from(document.querySelectorAll(".mapping-row[data-source-column]"))
        .filter(row => row.dataset.sourceColumn === sourceColumn);
      const instance = rows.length;
      const lastRow = rows[rows.length - 1];
      const mappingData = activeTable.product_mapping;
      lastRow.insertAdjacentHTML("afterend", mappingRow(activeTable, sourceColumn, mappingData, activeMode, null, instance));
      attachMappingEvents(activeMode);
      collectMapping(activeMode);
    }

    function displayCellValue(value) {
      if (value === null || value === undefined) return "";
      if (Array.isArray(value)) return value.map(item => displayCellValue(item)).filter(Boolean).join("; ");
      if (typeof value === "object" && ("label" in value || "value" in value || "id" in value)) {
        return String(value.label || value.value || value.id || "");
      }
      if (typeof value === "object") return JSON.stringify(value);
      return String(value);
    }

    function renderColumnSamples(table, column) {
      const samples = table.column_samples?.[column] || [];
      if (!samples.length) return "";
      const rows = samples.map(sample => `
        <tr>
          <td>${esc(sample.row)}</td>
          <td>${renderLinkedText(sample.value, { limit: 700 })}</td>
        </tr>`).join("");
      return `
        <details class="column-samples">
          <summary>${esc(t("mapping.moreRecords"))}</summary>
          <table>
            <thead><tr><th>${esc(t("mapping.rowNumber"))}</th><th>${esc(t("mapping.rowValue"))}</th></tr></thead>
            <tbody>${rows}</tbody>
          </table>
        </details>`;
    }

    function renderQualityRows(quality) {
      return Object.entries(quality || {}).map(([sourceColumn, item]) => {
        const typical = (item.typical_values || []).map(value => `${displayCellValue(value.value)} (${value.count})`).join(", ");
        const missing = (item.missing_row_numbers || []).join(", ");
        return `<tr>
          <td>${esc(sourceColumn)}</td>
          <td>${esc(item.filled_rows)} / ${esc(item.total_rows)}</td>
          <td>${esc(item.missing_rows)}</td>
          <td>${esc(missing)}</td>
          <td>${renderLinkedText(typical, { limit: 500 })}</td>
        </tr>`;
      }).join("");
    }

    function mappingProfileForMode(mode = activeMode) {
      if (mode === "supplement") return supplementMappingProfile || {};
      return productMappingProfile || loadedProject?.product_mapping_profile || {};
    }

    function profileItemForTarget(targetPath, profile = null) {
      const effectiveProfile = profile || mappingProfileForMode(activeMode);
      for (const [key, item] of Object.entries(effectiveProfile || {})) {
        if (String(key).startsWith("_")) continue;
        if (item?.target_path === targetPath) return item;
      }
      return null;
    }

    function suggestedSourceColumnForField(table, mappingData, field, profileItem = null) {
      if (profileItem?.source_column && (table.columns || []).includes(profileItem.source_column)) {
        return profileItem.source_column;
      }
      for (const [column, target] of Object.entries(mappingData.mapping || {})) {
        if (target === field.key) return column;
      }
      return "";
    }

    function renderModelFieldMappingRow(table, field, mappingData, mode) {
      const profileItem = profileItemForTarget(field.key, mappingProfileForMode(mode));
      const sourceColumn = suggestedSourceColumnForField(table, mappingData, field, profileItem);
      const quality = mappingData.field_quality || {};
      const cleanup = profileItem?.cleanup || {};
      const effectiveCleanup = { ...cleanup, targetUnit: cleanup.targetUnit || profileItem?.target_unit || field.unit || "" };
      const sampleValue = sourceColumn ? displayCellValue(previewRowForMapping(field)?.[sourceColumn] ?? "") : "";
      const afterValue = sourceColumn ? applyCleanup(sampleValue, effectiveCleanup) : "";
      const typicalValues = sourceColumn
        ? (quality[sourceColumn]?.typical_values || []).slice(0, 4).map(v => `<span class="pill">${renderLinkedText(v.value, { limit: 120 })} (${esc(v.count)})</span>`).join("")
        : "";
      const choiceMapEditor = renderChoiceMapEditor(field, table, sourceColumn, profileItem?.choice_map || {}, effectiveCleanup);
      return `<div class="mapping-row" data-source-column="${esc(sourceColumn)}" data-profile-key="target::${esc(field.key)}" data-map-instance="0">
        <div>
          <div class="source-name">${esc(cleanModelLabel(field.label || field.key))}${field.required ? " *" : ""}</div>
          <div class="source-meta">${esc(displayGroupName(field.group || ""))}<br>${esc(cleanModelLabel(field.key))}</div>
          ${renderFieldValueMeta(field)}
        </div>
        <div>
          <label>${esc(t("mapping.sourceColumn"))}
            <select data-source-column-select>
              ${columnOptions(table.columns, sourceColumn)}
            </select>
            <span class="helper">${esc(sourceColumn ? `${t("mapping.confidence")}: ${Math.round((quality[sourceColumn]?.confidence || mappingData.confidence?.[sourceColumn] || 0) * 100)}%  ${t("mapping.missing")}: ${quality[sourceColumn]?.missing_rows ?? 0}` : t("mapping.noSource"))}</span>
          </label>
          <select data-map-mode="${esc(mode)}" data-fixed-target-path="${esc(field.key)}" data-source-column="${esc(sourceColumn)}" hidden>
            <option value="${esc(field.key)}" data-label="${esc(field.label || field.key)}" data-group="${esc(field.group || "")}" selected>${esc(field.label || field.key)}</option>
          </select>
          <span class="helper" data-validation="duplicateTarget"></span>
          <span class="helper" data-choice-preview>${renderChoicePreview(field, afterValue, profileItem?.choice_map || {})}</span>
          <div>${typicalValues}</div>
          ${sourceColumn ? renderColumnSamples(table, sourceColumn) : ""}
          <details class="cleanup-details">
            <summary>${esc(t("mapping.mappingCleanup"))}</summary>
            <div class="rule-grid">
            <label>${esc(t("mapping.unitManual"))}
              <input type="text" data-cleanup="unit" value="${esc(effectiveCleanup.unit || "")}" placeholder="np. mm, W/mK, kg/m3">
            </label>
            <label>${esc(t("mapping.unitColumn"))}
              <select data-cleanup="unitSourceColumn">${columnOptions(table.columns, effectiveCleanup.unitSourceColumn || "")}</select>
            </label>
            <label>${esc(t("mapping.targetUnit"))}
              <input type="hidden" data-cleanup="targetUnit" value="${esc(effectiveCleanup.targetUnit || "")}">
              <div class="readonly-unit">${esc(effectiveCleanup.targetUnit || t("mapping.noTargetUnit"))}</div>
            </label>
            <label>${esc(t("mapping.unitConversionFactor"))}
              <input type="text" data-cleanup="unitConversionFactor" value="${esc(effectiveCleanup.unitConversionFactor || "")}" placeholder="1">
              <span class="helper">${esc(t("mapping.unitConversionHelp"))}</span>
            </label>
            ${choiceMapEditor}
            <label>${esc(t("mapping.removeText"))}
              <input type="text" data-cleanup="removeText" value="${esc(cleanup.removeText || "")}" placeholder="np. gruboĹ›Ä‡, ok., mm">
            </label>
            <label>${esc(t("mapping.replaceText"))}
              <input type="text" data-cleanup="replaceFrom" value="${esc(cleanup.replaceFrom || "")}" placeholder="tekst do zamiany">
            </label>
            <label>${esc(t("mapping.replaceWith"))}
              <input type="text" data-cleanup="replaceTo" value="${esc(cleanup.replaceTo || "")}" placeholder="nowa wartoĹ›Ä‡">
            </label>
            <label>${esc(t("mapping.splitBy"))}
              <input type="text" data-cleanup="splitBy" value="${esc(cleanup.splitBy || "")}" placeholder="np. /, x, ;">
            </label>
            <label>${esc(t("mapping.splitPart"))}
              <input type="text" data-cleanup="splitPart" value="${esc(cleanup.splitPart || "1")}" placeholder="1">
            </label>
            <div class="checkbox-row"><input type="checkbox" data-cleanup="trim"${cleanup.trim === false ? "" : " checked"}> ${esc(t("mapping.trim"))}</div>
            <div class="checkbox-row"><input type="checkbox" data-cleanup="decimalComma"${cleanup.decimalComma ? " checked" : ""}> ${esc(t("mapping.decimalComma"))}</div>
            <div class="checkbox-row"><input type="checkbox" data-cleanup="parseNumber"${cleanup.parseNumber ? " checked" : ""}> ${esc(t("mapping.parseNumber"))}</div>
            </div>
          </details>
        </div>
        <div>
          <div class="preview-box">
            <div class="preview-line"><div class="preview-label">${esc(t("mapping.before"))}</div><div class="preview-value" data-preview="before">${renderLinkedText(sampleValue, { limit: 700 })}</div></div>
            <div class="preview-line"><div class="preview-label">${esc(t("mapping.after"))}</div><div class="preview-value after-value" data-preview="after">${renderLinkedText(afterValue, { limit: 700 })}</div></div>
          </div>
        </div>
      </div>`;
    }

    function mappingRow(table, column, mappingData, mode, profileItem = null, instance = 0) {
      const mapping = mappingData.mapping || {};
      const confidence = mappingData.confidence || {};
      const quality = mappingData.field_quality || {};
      const targetFields = mappingData.target_fields || [];
      const cleanup = profileItem?.cleanup || {};
      const selected = profileItem?.target_path || (instance === 0 ? mapping[column] : "ignore") || "ignore";
      const selectedField = targetFieldByKey(targetFields, selected);
      const effectiveCleanup = { ...cleanup, targetUnit: cleanup.targetUnit || profileItem?.target_unit || selectedField?.unit || "" };
      const sampleValue = displayCellValue(previewRowForMapping(selectedField)?.[column] ?? "");
      const typicalValues = (quality[column]?.typical_values || []).slice(0, 4).map(v => `<span class="pill">${renderLinkedText(v.value, { limit: 120 })} (${esc(v.count)})</span>`).join("");
      return `<div class="mapping-row" data-source-column="${esc(column)}" data-map-instance="${esc(instance)}">
        <div>
          <div class="source-name">${esc(column)}${instance > 0 ? ` Â· ${esc(t("mapping.extraction"))} ${esc(instance + 1)}` : ""}</div>
          <div class="source-meta">${esc(t("mapping.confidence"))}: ${esc(Math.round((confidence[column] || 0) * 100))}%<br>${esc(t("mapping.missing"))}: ${esc(quality[column]?.missing_rows ?? 0)}</div>
          <div>${typicalValues}</div>
          ${renderColumnSamples(table, column)}
          ${mode === "products" ? `<button type="button" class="secondary" data-add-extraction="${esc(column)}">${esc(t("mapping.addExtraction"))}</button>` : ""}
        </div>
        <div>
          <label>${esc(t("mapping.targetField"))}
            <select data-map-mode="${esc(mode)}" data-source-column="${esc(column)}">
              ${targetOptions(targetFields, selected, mode)}
            </select>
            <span class="helper" data-validation="duplicateTarget"></span>
            <span class="helper" data-choice-preview>${renderChoicePreview(selectedField, sampleValue, profileItem?.choice_map || {})}</span>
          </label>
          <details class="cleanup-details">
            <summary>${esc(t("mapping.mappingCleanup"))}</summary>
            <div class="rule-grid">
            <label>${esc(t("mapping.unitManual"))}
              <input type="text" data-cleanup="unit" value="${esc(effectiveCleanup.unit || "")}" placeholder="np. mm, W/mK, kg/m3">
            </label>
            <label>${esc(t("mapping.unitColumn"))}
              <select data-cleanup="unitSourceColumn">${columnOptions(table.columns, effectiveCleanup.unitSourceColumn || "")}</select>
            </label>
            <label>${esc(t("mapping.targetUnit"))}
              <input type="hidden" data-cleanup="targetUnit" value="${esc(effectiveCleanup.targetUnit || "")}">
              <div class="readonly-unit">${esc(effectiveCleanup.targetUnit || t("mapping.noTargetUnit"))}</div>
            </label>
            <label>${esc(t("mapping.unitConversionFactor"))}
              <input type="text" data-cleanup="unitConversionFactor" value="${esc(effectiveCleanup.unitConversionFactor || "")}" placeholder="1">
              <span class="helper">${esc(t("mapping.unitConversionHelp"))}</span>
            </label>
            ${renderChoiceMapEditor(selectedField, table, column, profileItem?.choice_map || {}, effectiveCleanup)}
            <label>${esc(t("mapping.removeText"))}
              <input type="text" data-cleanup="removeText" value="${esc(cleanup.removeText || "")}" placeholder="np. gruboĹ›Ä‡, ok., mm">
            </label>
            <label>${esc(t("mapping.replaceText"))}
              <input type="text" data-cleanup="replaceFrom" value="${esc(cleanup.replaceFrom || "")}" placeholder="tekst do zamiany">
            </label>
            <label>${esc(t("mapping.replaceWith"))}
              <input type="text" data-cleanup="replaceTo" value="${esc(cleanup.replaceTo || "")}" placeholder="nowa wartoĹ›Ä‡">
            </label>
            <label>${esc(t("mapping.splitBy"))}
              <input type="text" data-cleanup="splitBy" value="${esc(cleanup.splitBy || "")}" placeholder="np. /, x, ;">
            </label>
            <label>${esc(t("mapping.splitPart"))}
              <input type="text" data-cleanup="splitPart" value="${esc(cleanup.splitPart || "1")}" placeholder="1">
            </label>
            <div class="checkbox-row"><input type="checkbox" data-cleanup="trim"${cleanup.trim === false ? "" : " checked"}> ${esc(t("mapping.trim"))}</div>
            <div class="checkbox-row"><input type="checkbox" data-cleanup="decimalComma"${cleanup.decimalComma ? " checked" : ""}> ${esc(t("mapping.decimalComma"))}</div>
            <div class="checkbox-row"><input type="checkbox" data-cleanup="parseNumber"${cleanup.parseNumber ? " checked" : ""}> ${esc(t("mapping.parseNumber"))}</div>
            </div>
          </details>
        </div>
        <div>
          <div class="preview-box">
            <div class="preview-line"><div class="preview-label">${esc(t("mapping.before"))}</div><div class="preview-value" data-preview="before">${renderLinkedText(sampleValue, { limit: 700 })}</div></div>
            <div class="preview-line"><div class="preview-label">${esc(t("mapping.after"))}</div><div class="preview-value after-value" data-preview="after">${renderLinkedText(sampleValue, { limit: 700 })}</div></div>
          </div>
        </div>
      </div>`;
    }

    function renderRowRules(table) {
      const loadedRules = rowRuleList(loadedProject?.product_mapping_profile?._row_rules || {});
      const rule = loadedRules.find(item => item.row_mode === "product_variants") || loadedRules[0] || {};
      const ruleCard = renderRowRuleCard(table, rule, 0);
      return `
      <div class="mapping-tools">
        <button type="button" class="secondary" id="rowRulesToggle">${esc(t("rows.openMenu"))}</button>
        <button type="button" class="secondary" id="checkMappingBtn">${esc(t("mapping.check"))}</button>
        <span class="rule-summary" id="rowRulesSummary">${esc(t("rows.summaryEmpty"))}</span>
      </div>
      <div id="rowRulesPanel" class="panel rule-menu" hidden>
        <div class="rule-menu-header">
          <div>
            <h2>${esc(t("rows.title"))}</h2>
            <div class="muted">${esc(t("rows.help"))}</div>
            <div class="helper">${esc(t("rows.menuHint"))}</div>
          </div>
          <button type="button" class="secondary" id="rowRulesClose">${esc(t("rows.closeMenu"))}</button>
        </div>
        <div id="rowRulesList">${ruleCard}</div>
        <div class="mapping-tools">
          <button type="button" id="applyRowRulesBtn">${esc(t("rows.applyRules"))}</button>
        </div>
        <div id="mappingCheckResult"></div>
      </div>`;
    }

    function distinctColumnValues(table, column, limit = 30) {
      const values = [];
      for (const row of table.sample_rows || []) {
        const value = displayCellValue(row[column] ?? "").trim();
        if (value && !values.includes(value)) values.push(value);
        if (values.length >= limit) break;
      }
      return values;
    }

    function rowTypeValueOptions(table, rule, selected) {
      const values = distinctColumnValues(table, rule.row_type_column || "");
      const selectedValue = String(selected || "");
      if (selectedValue && !values.includes(selectedValue)) values.unshift(selectedValue);
      return [`<option value="">${esc(t("none"))}</option>`]
        .concat(values.map(value => `<option value="${esc(value)}"${value === selectedValue ? " selected" : ""}>${esc(value)}</option>`))
        .join("");
    }

    function rowTypeValueDatalist(table, rule, listId) {
      const values = distinctColumnValues(table, rule.row_type_column || "");
      return `<datalist id="${esc(listId)}">${values.map(value => `<option value="${esc(value)}"></option>`).join("")}</datalist>`;
    }

    function refreshRowTypeValueOptions(card) {
      if (!activeTable || !card) return;
      const rowTypeColumn = card.querySelector("[data-row-rule='rowTypeColumn']")?.value || "";
      const values = distinctColumnValues(activeTable, rowTypeColumn);
      for (const key of ["productRowValues", "groupRowValues"]) {
        const field = card.querySelector(`[data-row-rule='${key}']`);
        if (!field) continue;
        if (field.tagName === "SELECT") {
          const previous = field.value;
          field.innerHTML = [`<option value="">${esc(t("none"))}</option>`]
            .concat(values.map(value => `<option value="${esc(value)}"${value === previous ? " selected" : ""}>${esc(value)}</option>`))
            .join("");
          continue;
        }
        const listId = field.getAttribute("list");
        const dataList = listId ? document.getElementById(listId) : null;
        if (!dataList) continue;
        const previous = field.value;
        dataList.innerHTML = values.map(value => `<option value="${esc(value)}"></option>`).join("");
        field.value = previous;
      }
    }

    function renderRowRuleCard(table, rule, index) {
      return `<div class="row-rule panel" data-rule-index="${esc(index)}">
        <h2>${esc(t("rows.rule"))} ${esc(index + 1)}</h2>
        <div class="rule-grid">
          <label>${esc(t("rows.mode"))}
            <input type="hidden" data-row-rule="rowMode" value="product_variants">
            <div class="readonly-value">${esc(t("rows.modeProductVariants"))}</div>
            <span class="helper">${esc(t("rows.modeHelp"))}</span>
          </label>
          <label>${esc(t("rows.typeColumn"))}
            <select data-row-rule="rowTypeColumn">${columnOptions(table.columns, rule.row_type_column || "")}</select>
            <span class="helper">${esc(t("rows.typeColumnHelp"))}</span>
          </label>
          <label>${esc(t("rows.productValues"))}
            <input type="text" data-row-rule="productRowValues" list="rowTypeProductValues${esc(index)}" value="${esc(rule.product_row_values || "")}" placeholder="Product">
            ${rowTypeValueDatalist(table, rule, `rowTypeProductValues${index}`)}
            <span class="helper">${esc(t("rows.productValuesHelp"))}</span>
          </label>
          <label>${esc(t("rows.groupValues"))}
            <input type="text" data-row-rule="groupRowValues" list="rowTypeVariantValues${esc(index)}" value="${esc(rule.group_row_values || "")}" placeholder="Article">
            ${rowTypeValueDatalist(table, rule, `rowTypeVariantValues${index}`)}
            <span class="helper">${esc(t("rows.groupValuesHelp"))}</span>
          </label>
          <label>${esc(t("rows.productIdColumn"))}
            <select data-row-rule="idColumn">${columnOptions(table.columns, rule.id_column || "")}</select>
            <span class="helper">${esc(t("rows.productIdColumnHelp"))}</span>
          </label>
          <label>${esc(t("rows.variantParentIdColumn"))}
            <select data-row-rule="parentIdColumn">${columnOptions(table.columns, rule.parent_id_column || "")}</select>
            <span class="helper">${esc(t("rows.variantParentIdColumnHelp"))}</span>
          </label>
          <div class="notice">${esc(t("rows.mappingHint"))}</div>
        </div>
      </div>`;
    }

    function renderMappingEditor(table, mode) {
      const mappingData = table.product_mapping;
      const targetFields = mappingData.target_fields || [];
      const productFields = targetFields.filter(field => !fieldIsTypeSeries(field));
      const typeSeriesFields = targetFields.filter(fieldIsTypeSeries);
      const renderMappingSection = (title, fields) => {
        const rows = fields.map(field => renderModelFieldMappingRow(table, field, mappingData, mode)).join("");
        return `<div class="mapping-card">
          <h2 class="mapping-section-title">${esc(title)}</h2>
          <div class="mapping-head">
            <div>${esc(t("mapping.modelField"))}</div>
            <div>${esc(t("mapping.mappingCleanup"))}</div>
            <div>${esc(t("mapping.valuePreview"))}</div>
          </div>
          ${rows || `<div class="mapping-row">${esc(t("mapping.emptySection"))}</div>`}
        </div>`;
      };
      const workspaceSwitcher = mode === "products" ? `<div>
        <div class="helper"><strong>${esc(t("enrichment.workflowTabs"))}</strong></div>
        <div class="workspace-switcher">
          <button type="button" data-workspace-tab="mapping" aria-pressed="${mappingWorkspaceTab === "mapping"}">${esc(t("enrichment.mappingTab"))}</button>
          <button type="button" data-workspace-tab="enrichment" aria-pressed="${mappingWorkspaceTab === "enrichment"}"${enrichmentReady() ? "" : " disabled"}>${esc(t("enrichment.enrichmentTab"))}</button>
        </div>
      </div>` : "";
      return `
        <div class="panel">
          <h2>${esc(table.name)} (${esc(table.rows)} ${currentLang === "pl" ? "wierszy" : "rows"})</h2>
          <div class="muted">${esc(t("report.empty"))}</div>
          ${workspaceSwitcher}
          ${mode === "products" && mappingWorkspaceTab !== "enrichment" ? `<div class="target-structure is-live" id="targetStructure">${renderTargetStructure(targetFields)}</div>` : ""}
          ${mode === "products" ? `<div id="productPreview"></div>` : ""}
          ${mode === "supplement" ? renderSupplementOutputPanel() : ""}
          <div class="workspace-pane" data-workspace-pane="enrichment"${mappingWorkspaceTab === "enrichment" ? "" : " hidden"}>
            ${mode === "products" ? renderEnrichmentPanel() : ""}
          </div>
          <div class="workspace-pane" data-workspace-pane="mapping"${mappingWorkspaceTab === "mapping" ? "" : " hidden"}>
            ${mode === "products" ? renderRowRules(table) : ""}
            ${mode === "products" ? `<div id="mappingCheckTopResult"></div>` : ""}
            ${mode === "products" ? `<div id="ruleOwnedNotice"></div>` : ""}
            ${renderMappingSection(t("mapping.productSection"), productFields)}
            ${renderMappingSection(t("mapping.typeSeriesSection"), typeSeriesFields)}
          </div>
          ${mode === "supplement" ? `<div class="mapping-card">
            <div class="mapping-tools">
              <button type="button" id="prepareSupplementDataBottomBtn">${esc(t("enrichment.prepareSupplement"))}</button>
              <button type="button" class="secondary" id="backToProductMappingBottomBtn">${esc(t("enrichment.backToProducts"))}</button>
            </div>
          </div>` : ""}
        </div>
      `;
    }

    function attachChoiceMapEvents(mode) {
      for (const input of document.querySelectorAll("[data-choice-map-target]")) {
        input.onchange = () => collectMapping(mode);
      }
    }

    function attachMappingEvents(mode) {
      for (const input of document.querySelectorAll("[data-cleanup], [data-source-column-select], select[data-map-mode], #rowRulesPanel input, #rowRulesPanel select")) {
        input.oninput = () => collectMapping(mode);
        input.onchange = () => {
          if (input.dataset.rowRule === "rowTypeColumn") {
            refreshRowTypeValueOptions(input.closest(".row-rule"));
          }
          collectMapping(mode);
        };
      }
      const toggleButton = $("rowRulesToggle");
      const rulesPanel = $("rowRulesPanel");
      if (toggleButton && rulesPanel) {
        toggleButton.onclick = () => {
          rulesPanel.hidden = !rulesPanel.hidden;
          toggleButton.setAttribute("aria-expanded", String(!rulesPanel.hidden));
        };
      }
      const closeButton = $("rowRulesClose");
      if (closeButton && rulesPanel) {
        closeButton.onclick = () => {
          rulesPanel.hidden = true;
          if (toggleButton) toggleButton.setAttribute("aria-expanded", "false");
          collectMapping(mode);
        };
      }
      const checkButton = $("checkMappingBtn");
      if (checkButton) checkButton.onclick = () => renderMappingCheck();
      const applyRulesButton = $("applyRowRulesBtn");
      if (applyRulesButton) applyRulesButton.onclick = () => applyRowRules();
      const toggleManualEditButton = $("toggleManualEditBtn");
      if (toggleManualEditButton) toggleManualEditButton.onclick = () => {
        manualEditEnabled = !manualEditEnabled;
        showProductWorkspace("enrichment");
      };
      const saveManualEditsButton = $("saveManualEditsBtn");
      if (saveManualEditsButton) saveManualEditsButton.onclick = () => saveInlineManualEdits();
      const undoProductChangesButton = $("undoProductChangesBtn");
      if (undoProductChangesButton) undoProductChangesButton.onclick = () => undoCurrentProductChanges();
      const openSupplementFileButton = $("openSupplementFileBtn");
      if (openSupplementFileButton) openSupplementFileButton.onclick = () => $("typicalRawFileVisible")?.click();
      const restoreEnrichmentButton = $("restoreEnrichmentBtn");
      if (restoreEnrichmentButton) restoreEnrichmentButton.onclick = () => restoreEnrichmentFromUi();
      const chooseTypicalButton = $("chooseTypicalDataBtn");
      if (chooseTypicalButton) chooseTypicalButton.onclick = () => $("typicalFile")?.click();
      const chooseTypicalModelsButton = $("chooseTypicalModelsBtn");
      if (chooseTypicalModelsButton) chooseTypicalModelsButton.onclick = () => $("typicalModelsFile")?.click();
      const chooseTypicalAttributesButton = $("chooseTypicalAttributesBtn");
      if (chooseTypicalAttributesButton) chooseTypicalAttributesButton.onclick = () => $("typicalAttributesFile")?.click();
      const chooseTypicalRawButton = $("chooseTypicalRawBtn");
      if (chooseTypicalRawButton) chooseTypicalRawButton.onclick = () => $("typicalRawFile")?.click();
      const typicalFileVisible = $("typicalFileVisible");
      if (typicalFileVisible) typicalFileVisible.onchange = async () => {
        const file = typicalFileVisible.files[0];
        await loadTypicalDataFile(file);
      };
      const typicalModelsVisible = $("typicalModelsFileVisible");
      if (typicalModelsVisible) typicalModelsVisible.onchange = async () => {
        const file = typicalModelsVisible.files[0];
        if (file) await loadTypicalSourceModelFile("models", file);
      };
      const typicalAttributesVisible = $("typicalAttributesFileVisible");
      if (typicalAttributesVisible) typicalAttributesVisible.onchange = async () => {
        const file = typicalAttributesVisible.files[0];
        if (file) await loadTypicalSourceModelFile("attributes", file);
      };
      const typicalRawVisible = $("typicalRawFileVisible");
      if (typicalRawVisible) typicalRawVisible.onchange = () => {
        const file = typicalRawVisible.files[0];
        loadRawTypicalFileForMapping(file);
      };
      const typicalSourceModeSelect = $("typicalSourceMode");
      if (typicalSourceModeSelect) typicalSourceModeSelect.onchange = () => {
        typicalSourceMode = typicalSourceModeSelect.value || "raw_file";
        enrichmentSession.typical_source_mode = typicalSourceMode;
        updateTypicalSourceModeUi();
      };
      const typicalMatchScope = $("typicalMatchScope");
      if (typicalMatchScope) typicalMatchScope.onchange = () => updateEnrichmentScopeUi();
      const enableEnrichmentFilter = $("enableEnrichmentFilter");
      if (enableEnrichmentFilter) enableEnrichmentFilter.onchange = () => updateEnrichmentScopeUi();
      const typicalSourceLabelFieldVisible = $("typicalSourceLabelFieldVisible");
      if (typicalSourceLabelFieldVisible) typicalSourceLabelFieldVisible.onchange = () => {
        const sourceProductSelect = $("typicalSourceProduct");
        if (sourceProductSelect) sourceProductSelect.innerHTML = typicalSourceProductOptions();
        const sourcePreview = $("typicalSourceProductPreview");
        if (sourcePreview) sourcePreview.innerHTML = renderTypicalSourceProductPreview();
      };
      const typicalSourceProduct = $("typicalSourceProduct");
      if (typicalSourceProduct) typicalSourceProduct.onchange = () => {
        const supplementSelect = $("supplementAttributeSelect");
        if (supplementSelect) supplementSelect.innerHTML = supplementAttributeOptions();
        const picker = $("typicalAttributePicker");
        if (picker) picker.innerHTML = renderTypicalAttributePicker();
        const sourcePreview = $("typicalSourceProductPreview");
        if (sourcePreview) sourcePreview.innerHTML = renderTypicalSourceProductPreview();
      };
      const enrichmentFilterField = $("enrichmentFilterField");
      if (enrichmentFilterField) enrichmentFilterField.onchange = () => {
        const values = $("enrichmentFilterValue");
        if (values) {
          values.innerHTML = productTargetValueOptions(enrichmentFilterField.value || "");
          values.disabled = !enrichmentFilterField.value;
        }
      };
      const supplementAttributeSelect = $("supplementAttributeSelect");
      if (supplementAttributeSelect) supplementAttributeSelect.onchange = () => updateTypeSeriesApplyVisibility();
      for (const input of document.querySelectorAll("[data-typical-target-product]")) {
        input.onchange = () => {
          const checked = Array.from(document.querySelectorAll("[data-typical-target-product]:checked"))
            .map(item => Number.parseInt(item.value, 10))
            .filter(Number.isFinite);
          if (checked.length) {
            productPreviewIndex = checked[0];
            renderProductPreview();
          }
        };
      }
      const addTypicalMatchButton = $("addTypicalMatchBtn");
      if (addTypicalMatchButton) addTypicalMatchButton.onclick = () => addTypicalMatchFromUi();
      const undoLastEnrichmentButton = $("undoLastEnrichmentBtn");
      if (undoLastEnrichmentButton) undoLastEnrichmentButton.onclick = () => undoLastEnrichmentChange();
      const clearEnrichmentButton = $("clearEnrichmentSessionBtn");
      if (clearEnrichmentButton) clearEnrichmentButton.onclick = () => clearEnrichmentSession();
      const generateEnrichedButton = $("generateEnrichedProductsBtn");
      if (generateEnrichedButton) generateEnrichedButton.onclick = () => generateProductsFromButton();
      const generateEnrichedMenuButton = $("generateEnrichedProductsMenuBtn");
      if (generateEnrichedMenuButton) generateEnrichedMenuButton.onclick = () => generateAndSaveProductsAs();
      const generateProductsInlineButton = $("generateProductsInlineBtn");
      if (generateProductsInlineButton) generateProductsInlineButton.onclick = () => generateProductsFromButton();
      const saveProductsAsButton = $("saveProductsAsBtn");
      if (saveProductsAsButton) saveProductsAsButton.onclick = () => saveGeneratedProductsAs();
      const mapSupplementButton = $("mapSupplementFileBtn");
      if (mapSupplementButton) mapSupplementButton.onclick = () => analyzeSupplementFileForMapping();
      const prepareSupplementButton = $("prepareSupplementDataBtn");
      if (prepareSupplementButton) prepareSupplementButton.onclick = () => prepareSupplementDataFromMapping();
      const prepareSupplementInlineButton = $("prepareSupplementDataInlineBtn");
      if (prepareSupplementInlineButton) prepareSupplementInlineButton.onclick = () => prepareSupplementDataFromMapping();
      const prepareSupplementBottomButton = $("prepareSupplementDataBottomBtn");
      if (prepareSupplementBottomButton) prepareSupplementBottomButton.onclick = () => prepareSupplementDataFromMapping();
      const backToProductMappingButton = $("backToProductMappingBtn");
      if (backToProductMappingButton) backToProductMappingButton.onclick = () => showProductWorkspace("enrichment");
      const backToProductMappingBottomButton = $("backToProductMappingBottomBtn");
      if (backToProductMappingBottomButton) backToProductMappingBottomButton.onclick = () => showProductWorkspace("enrichment");
      for (const button of document.querySelectorAll("[data-edit-supplement-mapping]")) {
        button.onclick = () => editCollapsedSupplementMapping(Number.parseInt(button.dataset.editSupplementMapping || "-1", 10));
      }
      for (const button of document.querySelectorAll("[data-workspace-tab]")) {
        button.onclick = () => setWorkspaceTab(button.dataset.workspaceTab || "mapping");
      }
      renderEnrichmentSessionList();
      updateTypicalSourceModeUi();
      updateEnrichmentScopeUi();
      for (const button of document.querySelectorAll("[data-preview-product]")) {
        button.onclick = () => {
          productPreviewIndex += button.dataset.previewProduct === "next" ? 1 : -1;
          renderProductPreview();
        };
      }
      for (const button of document.querySelectorAll("[data-add-extraction]")) {
        button.onclick = () => addColumnExtraction(button);
      }
      attachChoiceMapEvents(mode);
      collectMapping(mode);
      updateWorkspaceChrome();
    }

    function renderAnalysis(data, mode) {
      const best = bestAnalysisTable(data);

      if (!best) {
        showReport(`<div class='muted'>${esc(t("analysis.noTables"))}</div>`, `Analysis: ${mode}`);
        return;
      }

      activeTable = best;
      activeMode = mode;
      if (mode === "products") mainProductTable = best;
      productPreviewIndex = 0;
      showReport(renderMappingEditor(best, mode), `Mapping: ${mode}`);
      applyLoadedProjectToUi(mode);
      attachMappingEvents(mode);
    }

    async function projectPayload() {
      const productsFile = fileForInput("productsFile");
      const typicalFile = loadedProjectFiles.typicalDataFile || fileForInput("typicalFile");
      const modelFiles = await productModelFilesForProject();
      return {
        name: $("projectName").value || "import-produktow",
        model_version: "mapping-project.v1",
        source_table: activeTable?.name || null,
        product_mapping: productMapping || {},
        product_mapping_profile: productMappingProfile || {},
        supplement_mapping: supplementMapping || {},
        supplement_mapping_profile: supplementMappingProfile || {},
        supplement_products_url: supplementProductsUrl || "",
        enrichment_session: enrichmentSession,
        embedded_files: {
          product_model_files: await Promise.all(modelFiles.map(file => projectFileFromFile(file))),
          products_file: productsFile ? await projectFileFromFile(productsFile) : null,
          typical_data_file: typicalFile ? await projectFileFromFile(typicalFile) : null
        },
        saved_at: new Date().toISOString()
      };
    }

    async function saveProject() {
      if (!productMappingProfile) {
        $("projectStatus").textContent = t("project.analyzeFirst");
        return;
      }
      collectMapping("products");
      if (hasBlockingMappingConflicts()) {
        $("projectStatus").textContent = t("mapping.duplicateTargetBlocked");
        return;
      }
      try {
        const payload = await projectPayload();
        const filename = safeProjectFilename(payload.name);
        const result = await saveJsonFileToDisk(filename, payload);
        $("projectStatus").textContent = result.mode === "download"
          ? `${t("project.downloaded")} ${result.filename}`
          : `${t("project.saved")} ${result.filename}`;
        $("projectLinks").innerHTML = "";
      } catch (error) {
        if (error?.name === "AbortError") {
          $("projectStatus").textContent = t("project.notSaved");
          return;
        }
        $("projectStatus").textContent = t("project.saveFailed");
      }
    }

    async function loadProjectFromFile(file) {
      try {
        loadedProject = JSON.parse(await file.text());
        const embedded = loadedProject.embedded_files || {};
        loadedProjectFiles = {
          productModelFiles: (embedded.product_model_files || []).map(fileFromProjectFile).filter(Boolean),
          productsFile: fileFromProjectFile(embedded.products_file),
          typicalDataFile: fileFromProjectFile(embedded.typical_data_file)
        };
        enrichmentSession = normalizeEnrichmentSession(loadedProject.enrichment_session);
        supplementMapping = loadedProject.supplement_mapping || null;
        supplementMappingProfile = loadedProject.supplement_mapping_profile || null;
        supplementProductsUrl = loadedProject.supplement_products_url || "";
        typicalSourceMode = enrichmentSession.typical_source_mode || "raw_file";
        if (!loadedProjectFiles.productModelFiles.length && activeProductModelId) {
          loadedProjectFiles.productModelFiles = await projectFilesFromModelSession();
        }
        $("projectName").value = loadedProject.name || "import-produktow";
        const projectWarnings = [];
        if (!loadedProject.embedded_files) {
          projectWarnings.push(t("project.legacyMissingFiles"));
        } else if (!loadedProjectFiles.productModelFiles.length) {
          projectWarnings.push(`${t("project.missingModelFiles")} ${REQUIRED_PRODUCT_MODEL_FILES.map(item => item.label).join(", ")}`);
        }
        if (loadedProjectFiles.productModelFiles.length) {
          const missing = missingProductModelFiles(loadedProjectFiles.productModelFiles);
          pimModelAccepted = false;
          acceptedProductModelSignature = "";
          activeProductModelFields = [];
          if (!missing.length) {
            await loadProductModelFields(loadedProjectFiles.productModelFiles);
            pimModelAccepted = true;
            acceptedProductModelSignature = productModelSignature(loadedProjectFiles.productModelFiles);
          }
          $("productModelStatus").innerHTML = pimModelAccepted
            ? `<span class="ok">${esc(t("model.accepted"))}</span> ${esc(productModelFileNames(loadedProjectFiles.productModelFiles))}`
            : `${t("model.missingFiles")}${missing.join(", ")}`;
          if (missing.length) projectWarnings.push(`${t("project.missingModelFiles")} ${missing.join(", ")}`);
          updateWorkflowGate();
        }
        if (!loadedProjectFiles.productsFile) {
          projectWarnings.push(t("project.missingProductsFile"));
        }
        const hasSupplementFileToMap = (enrichmentSession.typical_sources || [])
          .some(source => source?.source === "supplement_file_to_map" || source?.mapping_required);
        if (loadedProjectFiles.typicalDataFile && hasSupplementFileToMap) {
          supplementFileForMapping = loadedProjectFiles.typicalDataFile;
          typicalProductsForEnrichment = [];
          typicalProductsPayloadForEnrichment = [];
          if ($("typicalStatus")) $("typicalStatus").textContent = `${t("enrichment.supplementFile")}: ${loadedProjectFiles.typicalDataFile.name}. ${t("enrichment.supplementMapLater")}`;
          renderEnrichmentSessionList();
        } else if (loadedProjectFiles.typicalDataFile) {
          await loadTypicalDataFile(loadedProjectFiles.typicalDataFile);
        } else {
          typicalProductsForEnrichment = [];
          typicalProductsPayloadForEnrichment = [];
          renderEnrichmentSessionList();
        }
        $("projectStatus").innerHTML = `<span class="ok">${esc(t("project.loaded"))} ${esc(loadedProject.name || file.name)}</span>${
          projectWarnings.length
            ? `<div class="warn">${projectWarnings.map(item => esc(item)).join("<br>")}</div>`
            : `<div class="helper">${esc(t("project.loadedComplete"))}</div>`
        }`;
        if (loadedProjectFiles.productsFile && pimModelAccepted) {
          $("productsStatus").textContent = currentLang === "pl"
            ? `Wczytano plik danych klienta z projektu: ${loadedProjectFiles.productsFile.name}. AnalizujÄ™ plik.`
            : `Loaded customer data file from project: ${loadedProjectFiles.productsFile.name}. Analyzing file.`;
          await analyzeFile("productsFile", "productsStatus", "products");
        } else if (pimModelAccepted && activeProductModelFields.length) {
          renderProductModelPreview();
        } else if (activeTable && activeMode === "products") {
          showReport(renderMappingEditor(activeTable, "products"), "Mapping: products");
          applyLoadedProjectToUi("products");
          attachMappingEvents("products");
        }
      } catch (error) {
        loadedProject = null;
        loadedProjectFiles = { productModelFiles: [], productsFile: null, typicalDataFile: null };
        enrichmentSession = { manual_entries: [], typical_sources: [], typical_matches: [] };
        typicalProductsForEnrichment = [];
        $("projectStatus").textContent = t("project.loadFailed");
      }
    }

    function applyLoadedProjectToUi(mode) {
      if (!loadedProject || mode !== "products") return;
      const profile = loadedProject.product_mapping_profile || {};
      for (const [sourceColumn, item] of Object.entries(profile)) {
        if (sourceColumn.startsWith("_")) continue;
        const actualSourceColumn = item.source_column || sourceColumn.split("::extract::")[0];
        const instance = extractionInstanceFromKey(sourceColumn);
        let select = Array.from(document.querySelectorAll(`select[data-map-mode="${mode}"]`))
          .find(candidate => candidate.dataset.fixedTargetPath === item.target_path)
          || Array.from(document.querySelectorAll(`select[data-map-mode="${mode}"]`))
            .find(candidate => candidate.dataset.sourceColumn === actualSourceColumn && (candidate.closest(".mapping-row")?.dataset.mapInstance || "0") === String(instance));
        if (!select && instance > 0 && activeTable) {
          const rows = Array.from(document.querySelectorAll(".mapping-row[data-source-column]"))
            .filter(row => row.dataset.sourceColumn === actualSourceColumn);
          const lastRow = rows[rows.length - 1];
          if (lastRow) {
            lastRow.insertAdjacentHTML("afterend", mappingRow(activeTable, actualSourceColumn, activeTable.product_mapping, mode, item, instance));
            select = Array.from(document.querySelectorAll(`select[data-map-mode="${mode}"]`))
              .find(candidate => candidate.dataset.sourceColumn === actualSourceColumn && (candidate.closest(".mapping-row")?.dataset.mapInstance || "0") === String(instance));
          }
        }
        const row = select?.closest(".mapping-row");
        if (!row) continue;
        if (!select.dataset.fixedTargetPath) select.value = item.target_path || "ignore";
        const sourceSelect = row.querySelector("[data-source-column-select]");
        if (sourceSelect) sourceSelect.value = actualSourceColumn;
        row.dataset.sourceColumn = actualSourceColumn;
        row.querySelector("[data-cleanup='unit']").value = item.cleanup?.unit || "";
        row.querySelector("[data-cleanup='unitSourceColumn']").value = item.cleanup?.unitSourceColumn || "";
        const targetUnitInput = row.querySelector("[data-cleanup='targetUnit']");
        if (targetUnitInput) targetUnitInput.value = item.cleanup?.targetUnit || item.target_unit || targetFieldByKey(targetFieldsForMode(mode), item.target_path)?.unit || "";
        const conversionInput = row.querySelector("[data-cleanup='unitConversionFactor']");
        if (conversionInput) conversionInput.value = item.cleanup?.unitConversionFactor || "";
        row.querySelector("[data-cleanup='choiceMap']").value = formatChoiceMap(item.choice_map || {});
        row.querySelector("[data-cleanup='removeText']").value = item.cleanup?.removeText || "";
        row.querySelector("[data-cleanup='replaceFrom']").value = item.cleanup?.replaceFrom || "";
        row.querySelector("[data-cleanup='replaceTo']").value = item.cleanup?.replaceTo || "";
        row.querySelector("[data-cleanup='splitBy']").value = item.cleanup?.splitBy || "";
        row.querySelector("[data-cleanup='splitPart']").value = item.cleanup?.splitPart || "1";
        row.querySelector("[data-cleanup='trim']").checked = item.cleanup?.trim !== false;
        row.querySelector("[data-cleanup='decimalComma']").checked = Boolean(item.cleanup?.decimalComma);
        row.querySelector("[data-cleanup='parseNumber']").checked = Boolean(item.cleanup?.parseNumber);
      }
    }

    function extractionInstanceFromKey(value) {
      const match = String(value || "").match(/::extract::(\\d+)$/);
      return match ? Number.parseInt(match[1], 10) : 0;
    }

    function renderConversion(data, mode, showPanel = true) {
      const links = [];
      if (data.files.products_json) links.push(`<a href="${esc(data.files.products_json)}" target="_blank">products.json</a>`);
      if (data.files.mapping_report_json) links.push(`<a href="${esc(data.files.mapping_report_json)}" target="_blank">mapping_report.json</a>`);
      if (data.files.enrichment_session_json) links.push(`<a href="${esc(data.files.enrichment_session_json)}" target="_blank">enrichment_session.json</a>`);
      if (!showPanel) return links.join("");
      const warnings = data.report?.warnings || {};
      const html = `
        <div class="panel">
          <h2>${esc(currentLang === "pl" ? "Wynik" : "Result")}</h2>
          <table><tbody>
            <tr><th>job_id</th><td>${esc(data.job_id)}</td></tr>
            <tr><th>status</th><td>${esc(data.status)}</td></tr>
            <tr><th>${esc(currentLang === "pl" ? "produkty" : "products")}</th><td>${esc(data.products_count ?? 0)}</td></tr>
            <tr><th>${esc(currentLang === "pl" ? "katalog" : "directory")}</th><td>${esc(data.output_dir)}</td></tr>
          </tbody></table>
          <div class="links">${links.join("")}</div>
          <div class="warn"><strong>${esc(currentLang === "pl" ? "OstrzeĹĽenia" : "Warnings")}</strong><pre>${esc(JSON.stringify(warnings, null, 2))}</pre></div>
        </div>`;
      showReport(html, currentLang === "pl" ? `Konwersja: ${mode}` : `Conversion: ${mode}`);
      return links.join("");
    }

    async function analyzeFile(inputId, statusId, mode) {
      if (!isProductModelAccepted()) {
        $(statusId).textContent = t("gate.locked");
        return;
      }
      const file = fileOrMessage(inputId, statusId, t("analysis.chooseFile"));
      if (!file) return;
      const body = new FormData();
      body.append("file", file);
      if (activeProductModelId) {
        body.append("product_model_id", activeProductModelId);
      } else {
        productModelDefinitionFiles().forEach((modelFile) => body.append("product_model_files", modelFile));
      }
      $(statusId).textContent = t("analysis.running");
      try {
        const response = await fetch("/analyze", { method: "POST", body });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || (currentLang === "pl" ? "BĹ‚Ä…d analizy." : "Analysis error."));
        $(statusId).textContent = t("analysis.ready");
        renderAnalysis(data, mode);
      } catch (error) {
        $(statusId).textContent = error.message;
        $("summary").textContent = t("status.error");
      }
    }

    window.analyzeProductsFromButton = async () => {
      await analyzeFile("productsFile", "productsStatus", "products");
      return false;
    };

    $("languageSelect").addEventListener("change", (event) => setLanguage(event.target.value));
    $("saveProjectBtn").addEventListener("click", () => saveProject());
    $("loadProjectFile").addEventListener("change", () => {
      const file = $("loadProjectFile").files[0];
      if (file) loadProjectFromFile(file);
    });
    for (const inputId of ["productModelsFile", "productAttributesFile"]) {
      const modelInput = $(inputId);
      if (!modelInput) continue;
      modelInput.addEventListener("change", () => {
        if (!confirmProductModelChange()) {
          modelInput.value = "";
          updateProductModelSelectionStatus();
          return;
        }
        resetAfterProductModelChange();
        updateProductModelSelectionStatus();
      });
    }
    $("typicalFile").addEventListener("change", async () => {
      const file = $("typicalFile").files[0];
      await loadTypicalDataFile(file);
    });
    $("typicalModelsFile").addEventListener("change", async () => {
      const file = $("typicalModelsFile").files[0];
      if (file) await loadTypicalSourceModelFile("models", file);
    });
    $("typicalAttributesFile").addEventListener("change", async () => {
      const file = $("typicalAttributesFile").files[0];
      if (file) await loadTypicalSourceModelFile("attributes", file);
    });
    $("typicalRawFile").addEventListener("change", () => {
      const file = $("typicalRawFile").files[0];
      loadRawTypicalFileForMapping(file);
    });
    $("productsFile").addEventListener("change", () => {
      if (!isProductModelAccepted()) {
        $("productsStatus").textContent = t("gate.locked");
        return;
      }
      loadedProjectFiles.productsFile = null;
      productMapping = null;
      productMappingProfile = null;
      generatedProductsJobId = null;
      generatedProductsUrl = "";
      supplementAnalysisTable = null;
      supplementMapping = null;
      supplementMappingProfile = null;
      supplementProductsPayload = null;
      supplementProductsUrl = "";
      if ($("productsSourceId")) $("productsSourceId").value = "";
      $("productsLinks").innerHTML = "";
      if ($("productsLinksInline")) $("productsLinksInline").innerHTML = "";
      updateWorkflowGate();
      if ($("productsFile").files[0]) {
        $("productsStatus").textContent = currentLang === "pl"
          ? `Wybrano ${$("productsFile").files[0].name}. AnalizujÄ™ plik.`
          : `Selected ${$("productsFile").files[0].name}. Analyzing file.`;
        analyzeFile("productsFile", "productsStatus", "products");
      }
    });
    async function generateProductsFromButton() {
      if (!isProductModelAccepted()) {
        $("productsStatus").textContent = t("gate.locked");
        return false;
      }
      const file = fileForInput("productsFile");
      if (!file && !$("productsSourceId")?.value) {
        $("productsStatus").textContent = currentLang === "pl" ? "Wybierz plik produktĂłw." : "Choose a products file.";
        return false;
      }
      collectMapping("products");
      if (hasBlockingMappingConflicts()) {
        $("productsStatus").textContent = t("mapping.duplicateTargetBlocked");
        return false;
      }
      const body = new FormData();
      if (file) body.append("file", file);
      const typicalFile = fileForInput("typicalFile");
      if (typicalFile) body.append("typical_data_file", typicalFile);
      else if (typicalProductsPayloadForEnrichment.length) {
        body.append(
          "typical_data_file",
          new Blob([JSON.stringify({ products: typicalProductsPayloadForEnrichment })], { type: "application/json" }),
          "mapped-supplements.json"
        );
      }
      if ($("productsSourceId")?.value) body.append("products_source_id", $("productsSourceId").value);
      if (productMapping) body.append("product_mapping", JSON.stringify(productMapping));
      if (productMappingProfile) body.append("product_mapping_profile", JSON.stringify(productMappingProfile));
      if ((enrichmentSession.manual_entries || []).length || (enrichmentSession.typical_sources || []).length) {
        body.append("enrichment_session", JSON.stringify(enrichmentSession));
      }
      if (activeProductModelId) {
        body.append("product_model_id", activeProductModelId);
      }
      $("productsStatus").textContent = currentLang === "pl" ? "Konwersja produktĂłw trwa." : "Product conversion is running.";
      $("productsLinks").innerHTML = "";
      if ($("productsLinksInline")) $("productsLinksInline").innerHTML = "";
      try {
        const response = await fetch("/convert-products", { method: "POST", body });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || (currentLang === "pl" ? "BĹ‚Ä…d konwersji produktĂłw." : "Product conversion error."));
        generatedProductsJobId = data.job_id;
        generatedProductsUrl = data.files?.products_json || "";
        $("productsStatus").innerHTML = currentLang === "pl"
          ? `<span class="ok">Produkty zapisane.</span> products.json jest gotowy do uĹĽycia.`
          : `<span class="ok">Products saved.</span> products.json is ready to use.`;
        const conversionLinks = renderConversion(data, "products", false);
        $("productsLinks").innerHTML = conversionLinks;
        if ($("productsLinksInline")) $("productsLinksInline").innerHTML = conversionLinks;
        updateWorkflowGate();
      } catch (error) {
        $("productsStatus").textContent = error.message;
        $("summary").textContent = t("status.error");
      }
      return false;
    }
    window.generateProductsFromButton = generateProductsFromButton;
    async function generateAndSaveProductsAs() {
      await generateProductsFromButton();
      if (generatedProductsUrl) {
        await saveGeneratedProductsAs();
      }
      return false;
    }
    window.generateAndSaveProductsAs = generateAndSaveProductsAs;
    $("productsForm").addEventListener("submit", async (event) => {
      event.preventDefault();
      if (event.submitter?.id === "analyzeProductsBtn") {
        const file = fileOrMessage("productsFile", "productsStatus", t("analysis.chooseFile"));
        if (!file) return;
        $("productsStatus").textContent = currentLang === "pl"
          ? "Proszę czekać, trwa analiza pliku klienta."
          : "Please wait, customer file analysis is running.";
        event.target.submit();
        return;
      }
      await generateProductsFromButton();
    });

    async function saveGeneratedProductsAs() {
      const status = $("productsSaveStatus") || $("productsStatus");
      if (!generatedProductsUrl) {
        if (status) status.textContent = t("products.saveMissing");
        return;
      }
      try {
        const response = await fetch(generatedProductsUrl);
        if (!response.ok) throw new Error(t("products.saveFailed"));
        const payload = await response.json();
        const projectName = $("projectName")?.value || "products";
        const filename = safeProductsFilename(projectName.replace(/project/i, "products"));
        const result = await saveJsonFileToDisk(filename, payload);
        if (status) status.textContent = `${t("products.saved")} ${result.filename}`;
      } catch (error) {
        if (error?.name === "AbortError") {
          if (status) status.textContent = t("products.saveMissing");
          return;
        }
        if (status) status.textContent = error.message || t("products.saveFailed");
      }
    }

    const generateEnrichedProductsMenuButton = $("generateEnrichedProductsMenuBtn");
    if (generateEnrichedProductsMenuButton) {
      generateEnrichedProductsMenuButton.onclick = () => generateAndSaveProductsAs();
    }

    if (activeProductModelId && $("productModelId")) $("productModelId").value = activeProductModelId;
    if (activeProductModelId && $("productsProductModelId")) $("productsProductModelId").value = activeProductModelId;
    if (INITIAL_ANALYSIS && INITIAL_ANALYSIS.source_id && $("productsSourceId")) $("productsSourceId").value = INITIAL_ANALYSIS.source_id;
    if (INITIAL_ANALYSIS && INITIAL_ANALYSIS.analysis) {
      $("productsStatus").textContent = t("analysis.ready");
      renderAnalysis(INITIAL_ANALYSIS.analysis, INITIAL_ANALYSIS.mode || "products");
    }
    applyLanguage();
  </script>
</body>
</html>""".replace("__INITIAL_PRODUCT_MODEL_JSON__", initial_model_json).replace("__INITIAL_ANALYSIS_JSON__", initial_analysis_json).replace("__INITIAL_PRODUCT_MODEL_STATUS__", initial_status).replace("__INITIAL_REPORT_HTML__", initial_report_html).replace("__REPORT_EMPTY_HIDDEN__", report_empty_hidden).replace("__INITIAL_SUMMARY__", initial_summary).replace("__MODEL_READY_DISABLED__", model_ready_disabled).replace("__PRODUCT_MODEL_ID_VALUE__", product_model_id_value).replace("__PRODUCTS_STATUS__", products_status).replace("__PRODUCTS_SOURCE_ID__", html.escape(str((initial_analysis or {}).get("source_id") or "")))


def render_building_elements_home() -> str:
    return """<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>BuildData AI Building Elements</title>
  <style>
    :root {
      --bg:#f3f5f7; --panel:#fff; --soft:#f8fafc; --line:#d8dde6;
      --text:#182230; --muted:#667085; --accent:#0f766e; --secondary:#344054;
      --warn:#9a3412;
      font-family: Arial, sans-serif;
    }
    * { box-sizing:border-box; }
    body { margin:0; background:var(--bg); color:var(--text); font-size:14px; }
    header {
      min-height:58px; display:flex; align-items:center; justify-content:space-between;
      gap:16px; padding:12px 22px; border-bottom:1px solid var(--line); background:var(--panel);
    }
    h1 { margin:0; font-size:20px; }
    h2 { margin:0 0 8px; font-size:17px; }
    h3 { margin:0 0 12px; font-size:15px; }
    p { margin:0 0 14px; color:var(--muted); line-height:1.45; }
    .header-actions, .top-nav { display:flex; align-items:center; gap:8px; }
    .top-nav a {
      display:inline-block; padding:8px 11px; border:1px solid var(--line); border-radius:4px;
      background:#fff; color:var(--secondary); text-decoration:none; font-weight:700; font-size:13px;
    }
    .top-nav a.active { border-color:var(--accent); background:#f0fdfa; color:var(--accent); }
    select.language-select { width:auto; min-width:140px; padding:7px 9px; }
    main { display:grid; grid-template-columns:360px 1fr; gap:16px; padding:16px; }
    .panel {
      border:1px solid var(--line); border-radius:6px; background:var(--panel);
      padding:14px; margin-bottom:14px;
    }
    label { display:block; margin-top:12px; color:#344054; font-weight:700; font-size:12px; }
    input[type=file], input[type=text], textarea {
      width:100%; margin-top:6px; padding:9px 10px; border:1px solid var(--line);
      border-radius:4px; background:#fff; color:var(--text); font:inherit;
    }
    textarea { min-height:110px; font-family:Consolas, "Courier New", monospace; }
    button {
      width:100%; margin-top:12px; padding:11px 14px; border:0; border-radius:4px;
      background:var(--accent); color:#fff; font-weight:700; cursor:pointer;
    }
    button.secondary { background:var(--secondary); }
    pre {
      min-height:220px; max-height:520px; overflow:auto; padding:12px; border-radius:4px;
      background:#0f172a; color:#e5e7eb; white-space:pre-wrap;
    }
    .mode-banner {
      border:1px solid #99f6e4;
      background:#f0fdfa;
      color:#115e59;
      border-radius:6px;
      padding:14px;
      margin-bottom:14px;
    }
    .mode-banner strong { display:block; font-size:18px; margin-bottom:4px; }
    .summary-grid {
      display:grid;
      grid-template-columns:repeat(auto-fit, minmax(150px, 1fr));
      gap:10px;
      margin:12px 0;
    }
    .summary-card {
      border:1px solid var(--line);
      border-radius:6px;
      padding:10px;
      background:#fff;
    }
    .summary-card strong { display:block; font-size:20px; color:var(--text); }
    .summary-card span { color:var(--muted); font-size:12px; }
    .tree-list { margin:12px 0 0; padding-left:18px; line-height:1.55; }
    .model-map {
      border:1px solid var(--line);
      border-radius:6px;
      overflow:hidden;
      margin-top:12px;
      background:#fff;
    }
    .model-map-group {
      padding:10px 12px;
      background:#f8fafc;
      border-top:1px solid var(--line);
      font-weight:700;
      color:#344054;
    }
    .model-map-group:first-child { border-top:0; }
    .model-tree-node {
      border-top:1px solid var(--line);
      background:#fff;
    }
    .model-tree-node:first-child { border-top:0; }
    .model-tree-header {
      padding:12px;
      background:#eef6f4;
      border-bottom:1px solid #eef2f6;
      box-shadow:inset 4px 0 0 var(--accent);
    }
    .model-tree-header strong { display:block; color:var(--text); }
    .model-tree-header span { display:block; color:var(--muted); font-size:12px; margin-top:3px; }
    .model-tree-children { margin-left:22px; border-left:3px solid #99f6e4; }
    .model-tree-empty { padding:10px 12px; color:var(--muted); font-size:12px; }
    .model-map-details {
      grid-column:1 / -1;
      border:1px solid #eef2f6;
      border-radius:4px;
      background:#fbfcfd;
      overflow:hidden;
    }
    .model-map-details summary {
      padding:9px 10px;
      cursor:pointer;
      font-weight:700;
      color:#344054;
      background:#f8fafc;
    }
    .choice-map-table {
      grid-column:1 / -1;
      width:100%;
      table-layout:fixed;
      margin-top:8px;
      font-size:12px;
    }
    .choice-map-table select { width:100%; }
    .choice-map-value { overflow-wrap:anywhere; }
    .pill {
      display:inline-block;
      margin:4px 4px 0 0;
      padding:4px 7px;
      border-radius:999px;
      border:1px solid var(--line);
      background:#fff;
      color:#344054;
      font-size:12px;
    }
    .model-map-row {
      display:grid;
      grid-template-columns:minmax(220px, 1fr) minmax(120px, 170px) minmax(150px, 210px) minmax(170px, 240px);
      gap:12px;
      align-items:start;
      padding:10px 12px;
      border-top:1px solid #eef2f6;
    }
    .model-map-label strong { display:block; color:var(--text); }
    .model-map-label span { display:block; color:var(--muted); font-size:12px; margin-top:3px; word-break:break-word; }
    .model-map-kind {
      color:var(--muted);
      font-size:12px;
      font-weight:700;
    }
    .model-map select {
      width:100%;
      margin:0;
      padding:8px;
      border:1px solid var(--line);
      border-radius:4px;
      background:#fff;
    }
    .model-cleanup {
      grid-column:1 / -1;
      display:grid;
      grid-template-columns:repeat(auto-fit, minmax(150px, 1fr));
      gap:8px;
      padding:8px;
      border:1px solid #eef2f6;
      border-radius:4px;
      background:#fbfcfd;
    }
    .model-cleanup label { margin:0; font-weight:600; color:var(--muted); }
    .model-cleanup input {
      width:100%;
      margin-top:4px;
      padding:7px;
      border:1px solid var(--line);
      border-radius:4px;
    }
    .model-options {
      grid-column:1 / -1;
      color:var(--muted);
      font-size:12px;
      line-height:1.4;
    }
    .status { margin-top:10px; color:var(--muted); line-height:1.45; }
    .notice {
      padding:10px; border:1px solid #fed7aa; border-radius:4px;
      background:#fff7ed; color:var(--warn); line-height:1.45;
    }
    @media (max-width:900px) {
      header { align-items:flex-start; flex-direction:column; }
      main { grid-template-columns:1fr; }
      .header-actions, .top-nav { flex-wrap:wrap; }
    }
  </style>
</head>
<body>
  <header>
    <h1>BuildData AI Building Elements</h1>
    <nav class="top-nav" aria-label="Workspace">
      <a href="/" data-i18n="nav.menu">Wróć do menu głównego</a>
      <a href="/products" data-i18n="nav.products">Produkty</a>
      <a class="active" href="/building-elements" data-i18n="nav.buildingElements">Elementy budowlane</a>
    </nav>
    <div class="header-actions">
      <span class="status" data-i18n="app.subtitle">Mapowanie elementĂłw budowlanych na podstawie modelu PIM</span>
      <select id="languageSelect" class="language-select" aria-label="Language">
        <option value="pl">Polski</option>
        <option value="en">English</option>
      </select>
    </div>
  </header>
  <main>
    <aside>
      <div class="panel">
        <h2 data-i18n="elements.title">Elementy budowlane</h2>
        <p data-i18n="elements.help">Ten moduĹ‚ sĹ‚uĹĽy do rozpoczÄ™cia mapowania elementĂłw budowlanych. Relacje do produktĂłw wymagajÄ… referencyjnego pliku products.json z mapowania produktĂłw.</p>
        <div class="notice" data-i18n="elements.notice">To jest pierwszy ekran roboczy dla elementĂłw budowlanych. Docelowo bÄ™dzie rozwiniÄ™ty do takiego samego poziomu obsĹ‚ugi jak mapowanie produktĂłw.</div>
      </div>
      <div class="panel">
        <h3 data-i18n="elements.files">Model, produkty i dane</h3>
        <label><span data-i18n="elements.modelFiles">buildingElementsModels.json + buildingElementsAttributes.json</span>
          <input id="elementModelFiles" type="file" multiple accept=".json">
        </label>
        <button type="button" class="secondary" onclick="loadElementModelHierarchy()" data-i18n="elements.loadModel">Wczytaj hierarchię modelu</button>
        <label><span data-i18n="elements.productsReference">Referencyjne products.json</span>
          <input id="productReferenceFile" type="file" accept=".json">
        </label>
        <label><span data-i18n="elements.importFile">Plik importowany</span>
          <input id="elementSourceFile" type="file" accept=".xlsx,.xlsm,.json,.csv,.tsv">
        </label>
        <button type="button" onclick="analyzeElements()" data-i18n="elements.analyze">Analizuj elementy budowlane</button>
        <div id="elementStatus" class="status"></div>
      </div>
      <div class="panel">
        <h3 data-i18n="project.title">Projekt mapowania</h3>
        <p data-i18n="project.help">Zapisuje pliki, model i aktualne mapowanie, aby moĹĽna byĹ‚o wrĂłciÄ‡ do pracy bez ponownego ustawiania importu.</p>
        <label><span data-i18n="project.name">Nazwa projektu</span>
          <input id="elementProjectName" type="text" value="mapowanie-elementow-budowlanych">
        </label>
        <button type="button" onclick="saveElementProject()" data-i18n="project.save">Zapisz projekt mapowania</button>
        <label><span data-i18n="project.load">Wczytaj projekt mapowania</span>
          <input id="elementProjectFile" type="file" accept=".json">
        </label>
        <div id="elementProjectStatus" class="status"></div>
      </div>
    </aside>
    <section class="panel">
      <div class="mode-banner">
        <strong data-i18n="elements.modeBannerTitle">Aktualnie mapujesz: ELEMENTY BUDOWLANE</strong>
        <span data-i18n="elements.modeBannerText">Na tym etapie importujemy strukturÄ™ systemĂłw, wariantĂłw i warstw. Produkty w warstwach moĹĽna dopasowaÄ‡ pĂłĹşniej.</span>
      </div>
      <h2 data-i18n="elements.result">Wynik analizy</h2>
      <div id="elementSummary" class="notice" data-i18n="elements.emptyResult">Wczytaj model elementĂłw i plik importowany, a nastÄ™pnie kliknij analizÄ™. Referencyjne products.json jest opcjonalne na tym etapie.</div>
    </section>
  </main>
  <script>
    const I18N = {
      pl: {
        "nav.products": "Produkty",
        "nav.menu": "Wróć do menu głównego",
        "nav.buildingElements": "Elementy budowlane",
        "app.subtitle": "Mapowanie elementĂłw budowlanych na podstawie modelu PIM",
        "elements.title": "Elementy budowlane",
        "elements.help": "Ten moduĹ‚ sĹ‚uĹĽy do rozpoczÄ™cia mapowania elementĂłw budowlanych. Relacje do produktĂłw wymagajÄ… referencyjnego pliku products.json z mapowania produktĂłw.",
        "elements.notice": "To jest pierwszy ekran roboczy dla elementĂłw budowlanych. Docelowo bÄ™dzie rozwiniÄ™ty do takiego samego poziomu obsĹ‚ugi jak mapowanie produktĂłw.",
        "elements.files": "Model, produkty i dane",
        "elements.modelFiles": "buildingElementsModels.json + buildingElementsAttributes.json",
        "elements.loadModel": "Wczytaj hierarchię modelu",
        "elements.productsReference": "Referencyjne products.json (opcjonalne do analizy, wymagane do eksportu relacji)",
        "elements.importFile": "Plik importowany",
        "elements.analyze": "Analizuj elementy budowlane",
        "elements.result": "Wynik analizy",
        "elements.modeBannerTitle": "Aktualnie mapujesz: ELEMENTY BUDOWLANE",
        "elements.modeBannerText": "Na tym etapie importujemy strukturÄ™ systemĂłw, wariantĂłw i warstw. Produkty w warstwach moĹĽna dopasowaÄ‡ pĂłĹşniej.",
        "elements.emptyResult": "Wczytaj model elementĂłw i plik importowany, a nastÄ™pnie kliknij analizÄ™. Referencyjne products.json jest opcjonalne na tym etapie.",
        "project.title": "Projekt mapowania",
        "project.help": "Zapisuje pliki, model i aktualne mapowanie, aby moĹĽna byĹ‚o wrĂłciÄ‡ do pracy bez ponownego ustawiania importu.",
        "project.name": "Nazwa projektu",
        "project.save": "Zapisz projekt mapowania",
        "project.load": "Wczytaj projekt mapowania",
        "project.saved": "Projekt zapisany:",
        "project.loaded": "Wczytano projekt:",
        "project.missing": "Najpierw wczytaj pliki modelu.",
        "project.failed": "Nie udaĹ‚o siÄ™ obsĹ‚uĹĽyÄ‡ projektu.",
        "status.ready": "Analiza gotowa.",
        "status.missing": "Brakuje pliku: ",
        "status.error": "BĹ‚Ä…d ĹĽÄ…dania"
      },
      en: {
        "nav.products": "Products",
        "nav.menu": "Back to main menu",
        "nav.buildingElements": "Building elements",
        "app.subtitle": "Building-element mapping based on the PIM model",
        "elements.title": "Building elements",
        "elements.help": "This module starts building-element mapping. Product relations require a reference products.json exported from product mapping.",
        "elements.notice": "This is the first working screen for building elements. It will be expanded to the same operational depth as product mapping.",
        "elements.files": "Model, products and data",
        "elements.modelFiles": "buildingElementsModels.json + buildingElementsAttributes.json",
        "elements.loadModel": "Load model hierarchy",
        "elements.productsReference": "Reference products.json (optional for analysis, required for relation export)",
        "elements.importFile": "Imported file",
        "elements.analyze": "Analyze building elements",
        "elements.result": "Analysis result",
        "elements.modeBannerTitle": "Currently mapping: BUILDING ELEMENTS",
        "elements.modeBannerText": "This step imports system, variant and layer structure. Layer products can be matched later.",
        "elements.emptyResult": "Load the building-element model and imported file, then run analysis. Reference products.json is optional at this step.",
        "project.title": "Mapping project",
        "project.help": "Saves files, model and current mapping so the work can be reopened without configuring the import again.",
        "project.name": "Project name",
        "project.save": "Save mapping project",
        "project.load": "Open mapping project",
        "project.saved": "Project saved:",
        "project.loaded": "Loaded project:",
        "project.missing": "Load model files first.",
        "project.failed": "Could not handle the project.",
        "status.ready": "Analysis ready.",
        "status.missing": "Missing file: ",
        "status.error": "Request error"
      }
    };
    let currentLang = localStorage.getItem("aiDataMasterLang") || "pl";
    let lastElementAnalysis = null;
    let currentElementMapping = {};
    let loadedElementProject = null;
    let loadedElementProjectFiles = { modelFiles: [], sourceFile: null, productsReferenceFile: null };
    const $ = (id) => document.getElementById(id);
    function t(key) { return I18N[currentLang]?.[key] || I18N.pl[key] || key; }
    function applyLanguage() {
      document.documentElement.lang = currentLang;
      $("languageSelect").value = currentLang;
      for (const element of document.querySelectorAll("[data-i18n]")) {
        element.textContent = t(element.dataset.i18n);
      }
    }
    $("languageSelect").addEventListener("change", (event) => {
      currentLang = event.target.value;
      localStorage.setItem("aiDataMasterLang", currentLang);
      applyLanguage();
    });
    function addFiles(form, name, input) {
      [...input.files].forEach((file) => form.append(name, file));
    }
    function addFilesFromList(form, name, files) {
      [...(files || [])].forEach((file) => form.append(name, file));
    }
    function addRequiredFile(form, name, input, label) {
      const file = input.files[0];
      if (!file) throw new Error(t("status.missing") + label);
      form.append(name, file);
    }
    function addRequiredProjectFile(form, name, input, fallbackFile, label) {
      const file = input.files[0] || fallbackFile;
      if (!file) throw new Error(t("status.missing") + label);
      form.append(name, file);
    }
    function addOptionalFile(form, name, input) {
      const file = input.files[0] || null;
      if (file) form.append(name, file);
    }
    function addOptionalProjectFile(form, name, input, fallbackFile) {
      const file = input.files[0] || fallbackFile;
      if (file) form.append(name, file);
    }
    async function postForm(url, form) {
      const response = await fetch(url, { method: "POST", body: form });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || t("status.error"));
      return payload;
    }
    function safeProjectFilename(name) {
      const safe = String(name || "mapowanie-elementow-budowlanych")
        .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
        .replace(/[^a-zA-Z0-9._-]+/g, "-")
        .replace(/^-+|-+$/g, "")
        .toLowerCase();
      return `${safe || "mapowanie-elementow-budowlanych"}.json`;
    }
    function projectFileFromFile(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve({
          name: file.name,
          type: file.type || "application/octet-stream",
          size: file.size,
          lastModified: file.lastModified || Date.now(),
          dataUrl: reader.result,
        });
        reader.onerror = () => reject(reader.error);
        reader.readAsDataURL(file);
      });
    }
    function fileFromProjectFile(payload) {
      if (!payload?.dataUrl) return null;
      const [header, data] = String(payload.dataUrl).split(",");
      const mime = (header.match(/data:(.*?);base64/) || [])[1] || payload.type || "application/octet-stream";
      const binary = atob(data || "");
      const bytes = new Uint8Array(binary.length);
      for (let index = 0; index < binary.length; index += 1) bytes[index] = binary.charCodeAt(index);
      return new File([bytes], payload.name || "file", { type: mime, lastModified: payload.lastModified || Date.now() });
    }
    async function saveJsonFileToDisk(filename, payload) {
      const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
      if (window.showSaveFilePicker) {
        const handle = await window.showSaveFilePicker({
          suggestedName: filename,
          types: [{ description: "JSON", accept: { "application/json": [".json"] } }],
        });
        const writable = await handle.createWritable();
        await writable.write(blob);
        await writable.close();
        return { filename, mode: "saved" };
      }
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(link.href);
      return { filename, mode: "download" };
    }
    async function elementProjectPayload() {
      syncElementMappingState();
      const modelFiles = [...$("elementModelFiles").files];
      const effectiveModelFiles = modelFiles.length ? modelFiles : loadedElementProjectFiles.modelFiles;
      const sourceFile = $("elementSourceFile").files[0] || loadedElementProjectFiles.sourceFile;
      const productsReferenceFile = $("productReferenceFile").files[0] || loadedElementProjectFiles.productsReferenceFile;
      if (!effectiveModelFiles.length) throw new Error(t("project.missing"));
      return {
        name: $("elementProjectName").value || "mapowanie-elementow-budowlanych",
        model_version: "building-elements-mapping-project.v1",
        building_element_mapping: currentElementMapping || {},
        analysis: lastElementAnalysis,
        embedded_files: {
          model_files: await Promise.all(effectiveModelFiles.map(file => projectFileFromFile(file))),
          source_file: sourceFile ? await projectFileFromFile(sourceFile) : null,
          products_reference_file: productsReferenceFile ? await projectFileFromFile(productsReferenceFile) : null,
        },
        saved_at: new Date().toISOString(),
      };
    }
    async function saveElementProject() {
      try {
        const payload = await elementProjectPayload();
        const result = await saveJsonFileToDisk(safeProjectFilename(payload.name), payload);
        $("elementProjectStatus").textContent = `${t("project.saved")} ${result.filename}`;
      } catch (error) {
        $("elementProjectStatus").textContent = error?.message || t("project.failed");
      }
    }
    async function loadElementProjectFromFile(file) {
      try {
        loadedElementProject = JSON.parse(await file.text());
        const embedded = loadedElementProject.embedded_files || {};
        loadedElementProjectFiles = {
          modelFiles: (embedded.model_files || []).map(fileFromProjectFile).filter(Boolean),
          sourceFile: fileFromProjectFile(embedded.source_file),
          productsReferenceFile: fileFromProjectFile(embedded.products_reference_file),
        };
        currentElementMapping = loadedElementProject.building_element_mapping || {};
        $("elementProjectName").value = loadedElementProject.name || "mapowanie-elementow-budowlanych";
        $("elementProjectStatus").textContent = `${t("project.loaded")} ${loadedElementProject.name || file.name}`;
        if (loadedElementProjectFiles.sourceFile) {
          await analyzeElements();
        } else {
          await loadElementModelHierarchy();
        }
      } catch (error) {
        $("elementProjectStatus").textContent = error?.message || t("project.failed");
      }
    }
    async function loadElementModelHierarchy() {
      const form = new FormData();
      try {
        $("elementStatus").textContent = currentLang === "pl"
          ? "Proszę czekać, trwa odczyt hierarchii modelu."
          : "Please wait, model hierarchy is loading.";
        const selectedModelFiles = [...$("elementModelFiles").files];
        const modelFiles = selectedModelFiles.length ? selectedModelFiles : loadedElementProjectFiles.modelFiles;
        addFilesFromList(form, "files", modelFiles);
        const payload = await postForm("/api/building-elements/model", form);
        renderElementAnalysis({
          model: payload.model,
          tables: [],
          product_reference: { products_count: 0, message: "Wczytano hierarchię modelu. Dodaj plik importowany, aby mapować kolumny." },
        });
        $("elementStatus").textContent = t("status.ready");
      } catch (error) {
        $("elementStatus").textContent = error.message;
      }
    }
    async function analyzeElements() {
      const form = new FormData();
      try {
        $("elementStatus").textContent = currentLang === "pl"
          ? "Proszę czekać, trwa analiza pliku klienta."
          : "Please wait, customer file analysis is running.";
        const selectedModelFiles = [...$("elementModelFiles").files];
        const modelFiles = selectedModelFiles.length ? selectedModelFiles : loadedElementProjectFiles.modelFiles;
        addFilesFromList(form, "model_files", modelFiles);
        addOptionalProjectFile(form, "products_reference", $("productReferenceFile"), loadedElementProjectFiles.productsReferenceFile);
        addRequiredProjectFile(form, "file", $("elementSourceFile"), loadedElementProjectFiles.sourceFile, t("elements.importFile"));
        const payload = await postForm("/api/building-elements/analyze", form);
        renderElementAnalysis(payload);
        $("elementStatus").textContent = t("status.ready");
      } catch (error) {
        $("elementStatus").textContent = error.message;
      }
    }
    function escapeHtml(value) {
      return String(value ?? "").replace(/[&<>"']/g, (char) => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
      }[char]));
    }
    function renderElementMappingEditor(payload) {
      const tables = payload.tables || [];
      const fields = payload.model?.fields || [];
      const firstTable = tables[0]?.name || "";
      const tableOptions = (selected) => [
        `<option value="">-- tabela --</option>`,
        ...tables.map((table) => `<option value="${escapeHtml(table.name)}" ${table.name === selected ? "selected" : ""}>${escapeHtml(table.name)}</option>`)
      ].join("");
      const suggested = tables[0]?.suggested_mapping?.mapping || {};
      const suggestedByTarget = {};
      for (const [source, target] of Object.entries(suggested)) {
        if (!suggestedByTarget[target]) suggestedByTarget[target] = source;
      }
      if (!fields.length) {
        return `<div class="notice">Nie odczytano struktury pól z modelu elementów budowlanych.</div>`;
      }
      const columnOptions = (selected, tableName) => [
        `<option value="">-- nie mapuj teraz --</option>`,
        ...(columnsForElementTable(tableName) || []).map((column) => `<option value="${escapeHtml(column)}" ${column === selected ? "selected" : ""}>${escapeHtml(column)}</option>`)
      ].join("");
      function elementSourceValues(tableName, columnName) {
        if (!tableName || !columnName) return [];
        const table = (lastElementAnalysis?.tables || []).find((item) => item.name === tableName);
        const values = [];
        for (const row of table?.sample_rows || []) {
          const raw = row?.[columnName];
          if (raw === undefined || raw === null || raw === "") continue;
          for (const part of String(raw).split(/[;,]/).map((item) => item.trim()).filter(Boolean)) {
            if (!values.includes(part)) values.push(part);
          }
        }
        return values.slice(0, 30);
      }
      function elementOptionText(option) {
        return option?.label || option?.value || String(option?.id || "");
      }
      function elementOptionSelect(field, selected) {
        const options = (field.options || []).map((option) => {
          const value = elementOptionText(option);
          return `<option value="${escapeHtml(value)}" ${value === selected ? "selected" : ""}>${escapeHtml(value)}</option>`;
        }).join("");
        return `<option value="">-- nie importuj bez mapy --</option>${options}`;
      }
      function renderElementChoiceMap(field, tableName, columnName, choiceMap = {}) {
        if (!["single_choice", "multi_choice"].includes(field.kind)) return "";
        const values = elementSourceValues(tableName, columnName);
        const optionPills = (field.options || []).map((option) => `<span class="pill">${escapeHtml(elementOptionText(option))}</span>`).join(" ");
        const rows = values.map((value) => `
          <tr>
            <td class="choice-map-value">${escapeHtml(value)}</td>
            <td><select data-element-choice-source="${escapeHtml(field.key)}" data-choice-value="${escapeHtml(value)}" onchange="syncElementChoiceMap('${escapeHtml(field.key)}')">${elementOptionSelect(field, choiceMap[value] || "")}</select></td>
          </tr>
        `).join("");
        return `
          <div class="model-options" data-element-choice-container="${escapeHtml(field.key)}">
            <textarea hidden data-cleanup="${escapeHtml(field.key)}" data-cleanup-key="choiceMap">${escapeHtml(JSON.stringify(choiceMap || {}))}</textarea>
            <strong>Mapowanie opcji wyboru:</strong>
            <div class="helper">Opcje PIM: ${optionPills || "brak opcji w eksporcie modelu"}</div>
            ${columnName
              ? `<table class="choice-map-table"><thead><tr><th>Wartość z pliku klienta</th><th>Opcja PIM</th></tr></thead><tbody>${rows || `<tr><td colspan="2">Brak wartości w próbce danych.</td></tr>`}</tbody></table>`
              : `<div class="helper">Wybierz tabelę i kolumnę, aby zmapować wartości klienta na opcje PIM.</div>`}
          </div>
        `;
      }
      function fieldHtml(field) {
        const existing = currentElementMapping[field.key] || {};
        const selectedColumn = existing.column || suggestedByTarget[field.key] || "";
        const selectedTable = existing.table || (selectedColumn ? firstTable : "");
        const cleanup = existing.cleanup || {};
        return `
          <div class="model-map-row" data-element-field-row="${escapeHtml(field.key)}">
            <div class="model-map-label">
              <strong>${escapeHtml(field.label || field.key)}</strong>
              <span>${escapeHtml(field.key)}</span>
            </div>
            <div class="model-map-kind">${escapeHtml(field.kind || "")}${field.required ? " / wymagane" : ""}</div>
            <select data-element-table="${escapeHtml(field.key)}" onchange="refreshElementMappingState(this)">
              ${tableOptions(selectedTable)}
            </select>
            <select data-element-column="${escapeHtml(field.key)}" onchange="refreshElementFieldState('${escapeHtml(field.key)}')">
              ${columnOptions(selectedColumn, selectedTable)}
            </select>
            <details class="model-map-details">
              <summary>Szczegóły mapowania i czyszczenia</summary>
              <div class="model-cleanup">
                <label><input type="checkbox" data-cleanup="${escapeHtml(field.key)}" data-cleanup-key="trim" ${cleanup.trim === false ? "" : "checked"} onchange="syncElementMappingState()"> trim</label>
                <label><input type="checkbox" data-cleanup="${escapeHtml(field.key)}" data-cleanup-key="decimalComma" ${cleanup.decimalComma ? "checked" : ""} onchange="syncElementMappingState()"> przecinek -> kropka</label>
                <label><input type="checkbox" data-cleanup="${escapeHtml(field.key)}" data-cleanup-key="parseNumber" ${cleanup.parseNumber ? "checked" : ""} onchange="syncElementMappingState()"> tylko liczba</label>
                <label>usuń tekst<input data-cleanup="${escapeHtml(field.key)}" data-cleanup-key="removeText" value="${escapeHtml(cleanup.removeText || "")}" oninput="syncElementMappingState()"></label>
                <label>separator<input data-cleanup="${escapeHtml(field.key)}" data-cleanup-key="splitBy" value="${escapeHtml(cleanup.splitBy || "")}" oninput="syncElementMappingState()"></label>
                <label>część<input data-cleanup="${escapeHtml(field.key)}" data-cleanup-key="splitPart" type="number" min="1" value="${escapeHtml(cleanup.splitPart || "")}" oninput="syncElementMappingState()"></label>
                <label>przelicznik<input data-cleanup="${escapeHtml(field.key)}" data-cleanup-key="unitConversionFactor" value="${escapeHtml(cleanup.unitConversionFactor || "")}" oninput="syncElementMappingState()"></label>
                <label>jednostka docelowa<input data-cleanup="${escapeHtml(field.key)}" data-cleanup-key="targetUnit" value="${escapeHtml(cleanup.targetUnit || field.unit || "")}" oninput="syncElementMappingState()"></label>
                ${renderElementChoiceMap(field, selectedTable, selectedColumn, cleanup.choiceMap || {})}
              </div>
            </details>
          </div>
        `;
      }
      function nodeHtml(node) {
        const fieldsHtml = (node.fields || []).map(fieldHtml).join("");
        const childrenHtml = (node.children || []).map((child) => nodeHtml(child)).join("");
        const meta = node.type === "relation"
          ? `relacja, atrybut ${node.attribute_id}, model ${node.source_model_id} -> ${node.target_model_id}`
          : `model ${node.model_id}`;
        return `
          <div class="model-tree-node">
            <div class="model-tree-header">
              <strong>${escapeHtml(node.label || "Model")}</strong>
              <span>${escapeHtml(meta)}</span>
            </div>
            ${fieldsHtml || `<div class="model-tree-empty">Brak pól bezpośrednio w tej gałęzi.</div>`}
            ${childrenHtml ? `<div class="model-tree-children">${childrenHtml}</div>` : ""}
          </div>
        `;
      }
      const hierarchyHtml = payload.model?.hierarchy ? nodeHtml(payload.model.hierarchy) : fields.map(fieldHtml).join("");
      return `
        <h3>Struktura modelu PIM i mapowanie kolumn</h3>
        <p>Mapujesz pola w hierarchii odczytanej z plików Models i Attributes. Wybierz tabelę i kolumnę dla konkretnej cechy w danej gałęzi modelu.</p>
        <div class="model-map">${hierarchyHtml}</div>
      `;
    }
    function columnsForElementTable(tableName) {
      const table = (lastElementAnalysis?.tables || []).find((item) => item.name === tableName);
      return table?.columns || [];
    }
    function refreshElementColumnSelect(tableSelect) {
      const target = tableSelect.dataset.elementTable;
      const columnSelect = document.querySelector(`[data-element-column="${CSS.escape(target)}"]`);
      if (!columnSelect) return;
      const current = columnSelect.value;
      const columns = columnsForElementTable(tableSelect.value);
      columnSelect.innerHTML = [
        `<option value="">-- nie mapuj teraz --</option>`,
        ...columns.map((column) => `<option value="${escapeHtml(column)}" ${column === current ? "selected" : ""}>${escapeHtml(column)}</option>`)
      ].join("");
    }
    function elementFieldByKey(key) {
      return (lastElementAnalysis?.model?.fields || []).find((field) => field.key === key);
    }
    function syncElementChoiceMap(target) {
      const holder = document.querySelector(`textarea[data-cleanup="${CSS.escape(target)}"][data-cleanup-key="choiceMap"]`);
      if (!holder) return;
      const choiceMap = {};
      for (const select of document.querySelectorAll(`[data-element-choice-source="${CSS.escape(target)}"]`)) {
        const source = select.dataset.choiceValue || "";
        if (source && select.value) choiceMap[source] = select.value;
      }
      holder.value = JSON.stringify(choiceMap);
      syncElementMappingState();
    }
    function refreshElementFieldState(target) {
      const row = document.querySelector(`[data-element-field-row="${CSS.escape(target)}"]`);
      const field = elementFieldByKey(target);
      if (!row || !field) {
        syncElementMappingState();
        return;
      }
      const tableName = row.querySelector(`[data-element-table="${CSS.escape(target)}"]`)?.value || "";
      const columnName = row.querySelector(`[data-element-column="${CSS.escape(target)}"]`)?.value || "";
      const cleanup = cleanupForTarget(target);
      const container = row.querySelector(`[data-element-choice-container="${CSS.escape(target)}"]`);
      if (container) container.outerHTML = renderElementChoiceMap(field, tableName, columnName, cleanup.choiceMap || {});
      syncElementMappingState();
    }
    function refreshElementMappingState(tableSelect) {
      refreshElementColumnSelect(tableSelect);
      refreshElementFieldState(tableSelect.dataset.elementTable);
    }
    function cleanupForTarget(target) {
      const cleanup = {};
      for (const input of document.querySelectorAll(`[data-cleanup="${CSS.escape(target)}"]`)) {
        const key = input.dataset.cleanupKey;
        if (!key) continue;
        if (input.type === "checkbox") {
          if (input.checked) cleanup[key] = true;
        } else if (key === "choiceMap") {
          try {
            const parsed = JSON.parse(input.value || "{}");
            if (Object.keys(parsed).length) cleanup[key] = parsed;
          } catch (error) {
            cleanup[key] = {};
          }
        } else if (input.value) {
          cleanup[key] = input.value;
        }
      }
      return cleanup;
    }
    function collectElementMapping() {
      const mapping = {};
      for (const tableSelect of document.querySelectorAll("[data-element-table]")) {
        const target = tableSelect.dataset.elementTable;
        const columnSelect = document.querySelector(`[data-element-column="${CSS.escape(target)}"]`);
        if (!target || !tableSelect.value || !columnSelect?.value) continue;
        mapping[target] = {
          table: tableSelect.value,
          column: columnSelect.value,
          cleanup: cleanupForTarget(target),
        };
      }
      return mapping;
    }
    function syncElementMappingState() {
      currentElementMapping = collectElementMapping();
    }
    function renderElementAnalysis(payload) {
      lastElementAnalysis = payload;
      const tables = payload.tables || [];
      const fields = payload.model?.fields || [];
      const relations = payload.model?.relations || [];
      const rows = tables.reduce((sum, table) => sum + (table.rows || 0), 0);
      const reference = payload.product_reference || {};
      const tableItems = tables.map((table) => `<li>${escapeHtml(table.name)}: ${table.rows || 0} wierszy, ${(table.columns || []).length} kolumn</li>`).join("");
      const mappingEditor = renderElementMappingEditor(payload);
      $("elementSummary").className = "panel";
      $("elementSummary").innerHTML = `
        <h3>Analiza elementĂłw budowlanych</h3>
        <div class="summary-grid">
          <div class="summary-card"><strong>${tables.length}</strong><span>tabele</span></div>
          <div class="summary-card"><strong>${rows}</strong><span>wiersze</span></div>
          <div class="summary-card"><strong>${fields.length}</strong><span>pola modelu PIM</span></div>
          <div class="summary-card"><strong>${relations.length}</strong><span>relacje zagnieĹĽdĹĽone</span></div>
          <div class="summary-card"><strong>${reference.products_count || 0}</strong><span>produkty referencyjne</span></div>
        </div>
        <p>${escapeHtml(reference.message || "")}</p>
        <h3>Wczytane tabele</h3>
        <ul class="tree-list">${tableItems || "<li>Nie znaleziono tabel w pliku importowanym.</li>"}</ul>
        ${mappingEditor}
      `;
      syncElementMappingState();
    }
    $("elementProjectFile").addEventListener("change", () => {
      const file = $("elementProjectFile").files[0];
      if (file) loadElementProjectFromFile(file);
    });
    applyLanguage();
  </script>
</body>
</html>"""


def render_initial_model_report(initial_model: dict) -> str:
    if initial_model.get("error"):
        return f"""<div class="panel">
          <h2>BĹ‚Ä…d modelu produktu PIM</h2>
          <div class="warn">{html.escape(str(initial_model.get("error")))}</div>
        </div>"""
    fields = initial_model.get("target_fields") or []
    if not fields:
        return ""
    grouped: dict[str, list[dict]] = {}
    for field in fields:
        grouped.setdefault(str(field.get("group") or "Model"), []).append(field)
    groups_html = []
    for group, group_fields in grouped.items():
        rows = "".join(
            f"""<div class="structure-field">
              <div class="structure-field-label">{html.escape(str(field.get("label") or field.get("key") or ""))}</div>
              <div class="structure-field-key">{html.escape(str(field.get("key") or ""))}</div>
            </div>"""
            for field in group_fields
        )
        groups_html.append(f"""<div class="structure-group"><strong>{html.escape(group)}</strong>{rows}</div>""")
    files = ", ".join(html.escape(str(file)) for file in (initial_model.get("files") or []))
    return f"""<div class="panel">
      <h2>Model produktu PIM</h2>
      <div class="muted">Model zostaĹ‚ odczytany z plikĂłw PIM. ReguĹ‚y i mapowanie pojawiÄ… siÄ™ po wczytaniu pliku danych klienta.</div>
      <div class="mapping-check-meta">
        <span class="pill">Wczytane pola modelu: {len(fields)}</span>
        <span class="pill">{files}</span>
      </div>
      <div class="target-structure">{"".join(groups_html)}</div>
    </div>"""


def render_initial_analysis_report(initial_analysis: dict) -> str:
    analysis = initial_analysis.get("analysis") or {}
    tables = analysis.get("tables") or []
    if not tables:
        return """<div class="panel">
          <h2>Analiza danych klienta</h2>
          <div class="muted">Nie znaleziono tabel do mapowania w pliku importowanym.</div>
        </div>"""
    best = sorted(
        tables,
        key=lambda table: ((table.get("product_mapping") or {}).get("score") or 0),
        reverse=True,
    )[0]
    columns = best.get("columns") or []
    sample_rows = best.get("sample_rows") or []
    mapping_data = best.get("product_mapping") or {}
    target_fields = mapping_data.get("target_fields") or []
    mapping = mapping_data.get("mapping") or {}
    confidence = mapping_data.get("confidence") or {}
    quality = mapping_data.get("field_quality") or {}
    sample = sample_rows[0] if sample_rows else {}
    grouped: dict[str, list[dict]] = {}
    for field in target_fields:
        grouped.setdefault(str(field.get("group") or "Model"), []).append(field)
    target_groups = []
    for group, fields in grouped.items():
        if "type series" in group.lower() or any(str(field.get("key") or "").startswith("type_series") for field in fields):
            rows = "".join(
                f"""<tr>
                  <td><strong>{html.escape(str(field.get("label") or field.get("key") or ""))}</strong><br><span class="muted">{html.escape(str(field.get("key") or ""))}</span></td>
                  <td><span class="structure-status">puste</span></td>
                  <td>-</td>
                  <td>-</td>
                </tr>"""
                for field in fields
            )
            target_groups.append(f"""<div class="structure-group type-series-structure">
              <strong>{html.escape(group)}</strong>
              <table>
                <thead><tr><th>Cecha wariantu</th><th>Status</th><th>ĹąrĂłdĹ‚o</th><th>WartoĹ›Ä‡ po czyszczeniu</th></tr></thead>
                <tbody>{rows}</tbody>
              </table>
            </div>""")
        else:
            rows = "".join(
                f"""<div class="structure-field">
                  <div class="structure-field-label">{html.escape(str(field.get("label") or field.get("key") or ""))}</div>
                  <div class="structure-field-key">{html.escape(str(field.get("key") or ""))}</div>
                  <div class="structure-field-meta"><span class="structure-status">puste</span></div>
                </div>"""
                for field in fields
            )
            target_groups.append(f"""<div class="structure-group"><strong>{html.escape(group)}</strong>{rows}</div>""")

    def options_html(selected: str, include_category: bool = False) -> str:
        options = [("ignore", "PomiĹ„")]
        if include_category:
            options.append(("product.category[].value", "Grupa produktu / kategoria"))
        options.extend((str(field.get("key") or ""), str(field.get("label") or field.get("key") or "")) for field in target_fields)
        return "".join(
            f"""<option value="{html.escape(value)}"{' selected' if value == selected else ''}>{html.escape(label)}</option>"""
            for value, label in options
        )

    column_options = '<option value="">Brak</option>' + "".join(
        f"""<option value="{html.escape(str(column))}">{html.escape(str(column))}</option>"""
        for column in columns
    )
    all_type_values = []
    for row in sample_rows:
        for column in columns:
            value = str((row or {}).get(column, "")).strip()
            if value and value not in all_type_values:
                all_type_values.append(value)
            if len(all_type_values) >= 80:
                break
        if len(all_type_values) >= 80:
            break
    type_values_datalist = '<datalist id="serverRowTypeValues">' + "".join(
        f"""<option value="{html.escape(value)}"></option>"""
        for value in all_type_values
    ) + "</datalist>"
    row_rules = f"""<div class="mapping-tools">
      <button type="button" class="secondary" id="rowRulesToggle">Reguły wierszy i hierarchii</button>
      <button type="button" class="secondary" id="checkMappingBtn">SprawdĹş aktualne mapowanie</button>
      <span class="rule-summary" id="rowRulesSummary">Brak aktywnych reguĹ‚.</span>
    </div>
    <div id="rowRulesPanel" class="panel rule-menu">
      <div class="rule-menu-header">
        <div>
          <h2>Reguły wierszy i hierarchii</h2>
          <div class="muted">Ustal, ktĂłre wiersze sÄ… produktem, a ktĂłre wariantem typoszeregu.</div>
        </div>
        <button type="button" class="secondary" id="rowRulesClose">Zamknij menu</button>
      </div>
      <div id="rowRulesList">
        <div class="row-rule panel" data-rule-index="0">
          <h2>Reguła 1</h2>
          <div class="rule-grid">
            <label>Tryb reguĹ‚y
              <input type="hidden" data-row-rule="rowMode" value="product_variants">
              <div class="readonly-value">Produkt -> warianty typoszeregu</div>
            </label>
            <label>Kolumna typu wiersza <select data-row-rule="rowTypeColumn">{column_options}</select></label>
            <label>WartoĹ›Ä‡ w kolumnie oznaczajÄ…ca produkt <input type="text" data-row-rule="productRowValues" list="serverRowTypeValues" placeholder="Product"></label>
            <label>WartoĹ›Ä‡ w kolumnie oznaczajÄ…ca wariant <input type="text" data-row-rule="groupRowValues" list="serverRowTypeValues" placeholder="Article"></label>
            <label>Kolumna ID produktu <select data-row-rule="idColumn">{column_options}</select></label>
            <label>Kolumna Parent ID wariantu <select data-row-rule="parentIdColumn">{column_options}</select></label>
            {type_values_datalist}
            <div class="notice">NazwÄ™ produktu, kod produktu, nazwÄ™ wariantu i inne cechy przypisz niĹĽej w zwykĹ‚ym mapowaniu pĂłl modelu.</div>
          </div>
        </div>
      </div>
      <div class="mapping-tools">
        <button type="button" id="applyRowRulesBtn">Zastosuj reguĹ‚y</button>
      </div>
      <div id="mappingCheckResult"></div>
    </div>"""

    mapping_rows = []
    for column in columns:
        selected = str(mapping.get(column) or "ignore")
        sample_value = "" if sample is None else str(sample.get(column, ""))
        missing_rows = (quality.get(column) or {}).get("missing_rows", 0)
        confidence_value = round(float(confidence.get(column) or 0) * 100)
        mapping_rows.append(
            f"""<div class="mapping-row" data-source-column="{html.escape(str(column))}">
              <div>
                <div class="source-name">{html.escape(str(column))}</div>
                <div class="source-meta">PewnoĹ›Ä‡: {confidence_value}%<br>Braki: {html.escape(str(missing_rows))}</div>
              </div>
              <div>
                <label>Pole docelowe
                  <select data-map-mode="products" data-source-column="{html.escape(str(column))}">{options_html(selected)}</select>
                  <span class="helper" data-validation="duplicateTarget"></span>
                </label>
                <div class="rule-grid">
                  <label>Jednostka <input type="text" data-cleanup="unit" placeholder="np. mm, W/mK, kg/m3"></label>
                  <label>Jednostka z kolumny <select data-cleanup="unitSourceColumn">{column_options}</select></label>
                  <label>Jednostka w modelu <input type="hidden" data-cleanup="targetUnit" value=""><div class="readonly-unit">Brak jednostki w modelu</div></label>
                  <label>MnoĹĽnik do jednostki modelu <input type="text" data-cleanup="unitConversionFactor" placeholder="1"></label>
                  <label>Mapa sĹ‚ownikowa <textarea data-cleanup="choiceMap" placeholder="wartoĹ›Ä‡ klienta = opcja PIM"></textarea></label>
                  <label>UsuĹ„ tekst <input type="text" data-cleanup="removeText" placeholder="np. gruboĹ›Ä‡, ok., mm"></label>
                  <label>ZamieĹ„ tekst <input type="text" data-cleanup="replaceFrom" placeholder="tekst do zamiany"></label>
                  <label>Na <input type="text" data-cleanup="replaceTo" placeholder="nowa wartoĹ›Ä‡"></label>
                  <label>Podziel po <input type="text" data-cleanup="splitBy" placeholder="np. /, x, ;"></label>
                  <label>CzÄ™Ĺ›Ä‡ po podziale <input type="text" data-cleanup="splitPart" value="1"></label>
                  <div class="checkbox-row"><input type="checkbox" data-cleanup="trim" checked> UsuĹ„ spacje</div>
                  <div class="checkbox-row"><input type="checkbox" data-cleanup="decimalComma"> ZamieĹ„ przecinek dziesiÄ™tny</div>
                  <div class="checkbox-row"><input type="checkbox" data-cleanup="parseNumber"> Odczytaj liczbÄ™</div>
                </div>
              </div>
              <div>
                <div class="preview-box">
                  <div class="preview-line"><div class="preview-label">Przed</div><div class="preview-value">{html.escape(sample_value)}</div></div>
                  <div class="preview-line"><div class="preview-label">Po</div><div class="preview-value after-value">{html.escape(sample_value)}</div></div>
                </div>
              </div>
            </div>"""
        )
    source = html.escape(str(initial_analysis.get("filename") or "plik klienta"))
    return f"""<div class="panel mapping-check-panel">
      <h2>Mapowanie produktĂłw</h2>
      <div class="muted">Plik {source} zostaĹ‚ odczytany. PoniĹĽej jest docelowa struktura modelu oraz kolumny klienta z sugestiami mapowania.</div>
      <div class="mapping-check-meta">
        <span class="pill">Tabela: {html.escape(str(best.get("name") or ""))}</span>
        <span class="pill">Wiersze: {html.escape(str(best.get("rows") or 0))}</span>
        <span class="pill">Kolumny: {len(columns)}</span>
      </div>
      {row_rules}
      <div id="mappingCheckTopResult"></div>
      <h2 class="title">Docelowa struktura modelu</h2>
      <div class="target-structure" id="targetStructure">{"".join(target_groups)}</div>
      <div id="ruleOwnedNotice"></div>
      <h2 class="title">Kolumny klienta i mapowanie</h2>
      <div class="mapping-card">
        <div class="mapping-head">
          <div>Kolumna klienta</div>
          <div>Mapowanie i czyszczenie</div>
          <div>PodglÄ…d wartoĹ›ci</div>
        </div>
        {"".join(mapping_rows)}
      </div>
      <div id="productPreview"></div>
    </div>"""
