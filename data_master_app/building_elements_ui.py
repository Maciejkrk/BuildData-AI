from __future__ import annotations


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
    body.is-busy button { pointer-events:none; opacity:.62; }
    .busy-overlay {
      position:fixed;
      right:18px;
      bottom:18px;
      z-index:50;
      display:flex;
      align-items:center;
      gap:12px;
      max-width:min(420px, calc(100vw - 36px));
      padding:14px 16px;
      border:1px solid #99f6e4;
      border-radius:8px;
      background:#f0fdfa;
      color:#115e59;
      box-shadow:0 16px 38px rgba(15, 23, 42, .18);
      font-weight:700;
    }
    .busy-overlay[hidden] { display:none; }
    .busy-spinner {
      width:22px;
      height:22px;
      border:3px solid #99f6e4;
      border-top-color:var(--accent);
      border-radius:50%;
      animation:busy-spin .85s linear infinite;
      flex:0 0 auto;
    }
    .busy-overlay span { display:block; font-weight:600; line-height:1.35; }
    @keyframes busy-spin { to { transform:rotate(360deg); } }
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
    .model-level-config {
      display:grid;
      grid-template-columns:repeat(auto-fit, minmax(180px, 1fr));
      gap:10px;
      padding:10px 12px;
      background:#fbfcfd;
      border-bottom:1px solid #eef2f6;
    }
    .model-level-config label { margin:0; }
    .model-level-config select {
      width:100%;
      margin-top:5px;
      padding:8px;
      border:1px solid var(--line);
      border-radius:4px;
      background:#fff;
    }
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
    .live-preview {
      margin-top:14px;
      border:1px solid var(--line);
      border-radius:6px;
      background:#fff;
      overflow:hidden;
    }
    .live-preview-head {
      display:flex;
      justify-content:space-between;
      gap:12px;
      align-items:flex-start;
      padding:12px;
      background:#f8fafc;
      border-bottom:1px solid var(--line);
    }
    .live-preview-head p { margin:4px 0 0; }
    .live-preview-nav {
      display:flex;
      align-items:center;
      justify-content:flex-end;
      gap:8px;
      flex-wrap:wrap;
    }
    .live-preview-nav button {
      width:auto;
      margin:0;
      padding:8px 10px;
    }
    .live-preview-table-wrap { overflow:auto; }
    .live-preview-table {
      width:100%;
      border-collapse:collapse;
      min-width:760px;
      font-size:12px;
    }
    .live-preview-table th,
    .live-preview-table td {
      padding:8px 10px;
      border-bottom:1px solid #eef2f6;
      vertical-align:top;
      text-align:left;
    }
    .live-preview-table th {
      background:#fbfcfd;
      color:#344054;
      font-weight:700;
    }
    .element-visual-preview {
      display:grid;
      gap:12px;
      padding:12px;
      background:#fbfcfd;
    }
    .element-visual-card {
      border:1px solid var(--line);
      border-radius:6px;
      background:#fff;
      overflow:hidden;
    }
    .element-visual-title {
      padding:12px;
      background:#ecfdf5;
      border-bottom:1px solid #bbf7d0;
    }
    .element-visual-title strong { display:block; font-size:16px; color:#14532d; }
    .element-visual-title span { display:block; margin-top:3px; color:var(--muted); font-size:12px; }
    .variant-visual-grid {
      display:grid;
      grid-template-columns:repeat(auto-fit, minmax(260px, 1fr));
      gap:12px;
      padding:12px;
    }
    .variant-visual-card {
      border:1px solid #dbeafe;
      border-radius:6px;
      background:#f8fbff;
      overflow:hidden;
    }
    .variant-visual-head {
      padding:10px 12px;
      background:#eff6ff;
      border-bottom:1px solid #dbeafe;
      font-weight:700;
      color:#1e3a8a;
    }
    .layer-visual-card {
      margin:10px;
      border:1px solid #e5e7eb;
      border-radius:6px;
      background:#fff;
    }
    .layer-visual-head {
      padding:9px 10px;
      border-bottom:1px solid #eef2f6;
      font-weight:700;
      color:#344054;
    }
    .product-visual-list { display:grid; gap:8px; padding:10px; }
    .product-visual-chip {
      border:1px solid #e5e7eb;
      border-left:4px solid #9ca3af;
      border-radius:6px;
      padding:9px 10px;
      background:#fff;
    }
    .product-visual-chip.is-ok { border-left-color:#16a34a; background:#f0fdf4; }
    .product-visual-chip.is-warn { border-left-color:#ea580c; background:#fff7ed; }
    .product-visual-chip strong { display:block; color:var(--text); }
    .product-visual-chip span { display:block; margin-top:3px; color:var(--muted); font-size:12px; overflow-wrap:anywhere; }
    .visual-empty {
      padding:14px;
      color:var(--muted);
      background:#fff;
    }
    .status-ok { color:#166534; font-weight:700; }
    .status-warn { color:#9a3412; font-weight:700; }
    .preview-path { color:var(--muted); font-size:11px; }
    .model-builder-grid {
      display:grid;
      grid-template-columns:repeat(auto-fit, minmax(220px, 1fr));
      gap:10px;
      margin-top:12px;
    }
    .model-builder-grid label { margin:0; }
    .model-builder-grid input, .model-builder-grid textarea, .model-builder-grid select {
      width:100%;
      margin-top:5px;
      padding:8px;
      border:1px solid var(--line);
      border-radius:4px;
      background:#fff;
    }
    .model-builder-row {
      border:1px solid var(--line);
      border-radius:6px;
      padding:10px;
      margin-top:12px;
      background:#fff;
    }
    .model-builder-row-head {
      display:flex;
      justify-content:space-between;
      align-items:center;
      gap:10px;
      margin-bottom:8px;
    }
    .model-builder-row button { width:auto; margin:0; }
    .model-builder-preview {
      display:grid;
      grid-template-columns:repeat(auto-fit, minmax(180px, 1fr));
      gap:8px;
      font-size:12px;
      color:var(--muted);
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
      <a href="/colors" data-i18n="nav.colors">Kolory</a>
    </nav>
    <div class="header-actions">
      <span class="status" data-i18n="app.subtitle">Mapowanie elementów budowlanych na podstawie modelu PIM</span>
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
        <p data-i18n="elements.help">Ten moduł służy do mapowania elementów budowlanych. Referencyjne products.json jest opcjonalne i służy do kontroli dopasowania produktów po ID, kodzie albo nazwie.</p>
        <div class="notice" data-i18n="elements.notice">To jest ekran roboczy dla hierarchii elementów budowlanych: leveli, parentów, wariantów i pól modelu PIM.</div>
        <label><span data-i18n="workflow.mode">Tryb pracy</span>
          <select id="elementWorkflowMode">
            <option value="import" data-i18n="workflow.import">Importuj dane i edytuj później</option>
            <option value="modelBuilder" data-i18n="workflow.modelBuilder">Stwórz własne systemy z modelu</option>
          </select>
        </label>
      </div>
      <div class="panel">
        <h3 data-i18n="elements.files">Model, produkty i dane</h3>
        <label><span data-i18n="elements.modelsFile">buildingElementsModels.json</span>
          <input id="elementModelsFile" type="file" accept=".json">
        </label>
        <label><span data-i18n="elements.attributesFile">buildingElementsAttributes.json</span>
          <input id="elementAttributesFile" type="file" accept=".json">
        </label>
        <button type="button" class="secondary" onclick="loadElementModelHierarchy()" data-i18n="elements.loadModel">Wczytaj hierarchię modelu</button>
        <label><span data-i18n="elements.activeModel">Edytowany model elementu</span>
          <select id="elementRootModelSelect" disabled></select>
        </label>
        <label><span data-i18n="elements.productsReference">Referencyjne products.json</span>
          <input id="productReferenceFile" type="file" accept=".json">
        </label>
        <div class="notice" data-i18n="productIdentity.notice">Model produktu jest opcjonalny, ale zalecany. Pozwala wskazać, który atrybut produktu jest stabilnym identyfikatorem używanym przy warstwach.</div>
        <label><span data-i18n="productIdentity.modelsFile">productsModels.json</span>
          <input id="elementProductModelsFile" type="file" accept=".json">
        </label>
        <label><span data-i18n="productIdentity.attributesFile">productsAttributes.json</span>
          <input id="elementProductAttributesFile" type="file" accept=".json">
        </label>
        <button type="button" class="secondary" onclick="loadElementProductModel()" data-i18n="productIdentity.loadModel">Wczytaj model produktu</button>
        <label><span data-i18n="productIdentity.activeModel">Model produktu dla dopasowania</span>
          <select id="elementProductRootModelSelect" disabled></select>
        </label>
        <label><span data-i18n="productIdentity.field">Atrybut identyfikujący produkt</span>
          <select id="elementProductIdentityFieldSelect" disabled></select>
        </label>
        <div id="elementProductIdentityStatus" class="status"></div>
        <label><span data-i18n="elements.importFile">Plik importowany</span>
          <input id="elementSourceFile" type="file" accept=".xlsx,.xlsm,.json,.csv,.tsv">
        </label>
        <button type="button" onclick="analyzeElements()" data-i18n="elements.analyze">Analizuj elementy budowlane</button>
        <button type="button" class="secondary" onclick="generateBuildingElements()" data-i18n="elements.generate">Generuj building_elements.json</button>
        <div id="modelBuilderPanel" class="notice" hidden>
          <strong data-i18n="modelBuilder.title">Budowanie systemów z modelu</strong>
          <div data-i18n="modelBuilder.help">Najpierw wczytaj model elementów budowlanych. Edytor ręczny musi powstać z hierarchii modelu, więc nie używa pliku importowanego ani stałych pól.</div>
          <button type="button" class="secondary" onclick="loadElementModelHierarchy()" data-i18n="modelBuilder.load">Wczytaj / odśwież model</button>
          <div id="modelBuilderStatus" class="status"></div>
        </div>
        <div id="elementStatus" class="status"></div>
      </div>
      <div class="panel">
        <h3 data-i18n="project.title">Projekt mapowania</h3>
        <p data-i18n="project.help">Zapisuje pliki, model i aktualne mapowanie, aby można było wrócić do pracy bez ponownego ustawiania importu.</p>
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
        <span data-i18n="elements.modeBannerText">Na tym etapie importujemy strukturę systemów, wariantów i warstw. Produkty w warstwach można dopasować później.</span>
      </div>
      <h2 data-i18n="elements.result">Wynik analizy</h2>
      <div id="elementSummary" class="notice" data-i18n="elements.emptyResult">Wczytaj model elementów i plik importowany, a następnie kliknij analizę. Referencyjne products.json jest opcjonalne na tym etapie.</div>
    </section>
  </main>
  <div id="busyOverlay" class="busy-overlay" hidden>
    <div class="busy-spinner" aria-hidden="true"></div>
    <span id="busyMessage">Przetwarzam dane...</span>
  </div>
  <script>
    const I18N = {
      pl: {
        "nav.products": "Produkty",
        "nav.menu": "Wróć do menu głównego",
        "nav.buildingElements": "Elementy budowlane",
        "nav.colors": "Kolory",
        "app.subtitle": "Mapowanie elementów budowlanych na podstawie modelu PIM",
        "elements.title": "Elementy budowlane",
        "elements.help": "Ten moduł służy do mapowania elementów budowlanych. Referencyjne products.json jest opcjonalne i służy do kontroli dopasowania produktów po ID, kodzie albo nazwie.",
        "elements.notice": "To jest ekran roboczy dla hierarchii elementów budowlanych: leveli, parentów, wariantów i pól modelu PIM.",
        "workflow.mode": "Tryb pracy",
        "workflow.import": "Importuj dane i edytuj później",
        "workflow.modelBuilder": "Stwórz własne systemy z modelu",
        "modelBuilder.title": "Budowanie systemów z modelu",
        "modelBuilder.help": "Najpierw wczytaj model elementów budowlanych. Edytor ręczny musi powstać z hierarchii modelu, więc nie używa pliku importowanego ani stałych pól.",
        "modelBuilder.load": "Wczytaj / odśwież model",
        "elements.files": "Model, produkty i dane",
        "elements.modelsFile": "buildingElementsModels.json",
        "elements.attributesFile": "buildingElementsAttributes.json",
        "elements.loadModel": "Wczytaj hierarchię modelu",
        "elements.activeModel": "Edytowany model elementu",
        "elements.productsReference": "Referencyjne products.json (opcjonalne, do kontroli dopasowania produktów)",
        "productIdentity.notice": "Model produktu jest opcjonalny, ale zalecany. Pozwala wskazać, który atrybut produktu jest stabilnym identyfikatorem używanym przy warstwach.",
        "productIdentity.modelsFile": "productsModels.json",
        "productIdentity.attributesFile": "productsAttributes.json",
        "productIdentity.loadModel": "Wczytaj model produktu",
        "productIdentity.activeModel": "Model produktu dla dopasowania",
        "productIdentity.field": "Atrybut identyfikujący produkt",
        "productIdentity.ready": "Model produktu wczytany. Wybierz atrybut identyfikujący produkt.",
        "productIdentity.missing": "Wczytaj oba pliki modelu produktu: Models i Attributes.",
        "productIdentity.none": "Brak wczytanego modelu produktu",
        "elements.importFile": "Plik importowany",
        "elements.analyze": "Analizuj elementy budowlane",
        "elements.generate": "Generuj building_elements.json",
        "elements.result": "Wynik analizy",
        "elements.modeBannerTitle": "Aktualnie mapujesz: ELEMENTY BUDOWLANE",
        "elements.modeBannerText": "Na tym etapie importujemy strukturę systemów, wariantów i warstw. Produkty w warstwach można dopasować później.",
        "elements.emptyResult": "Wczytaj model elementów i plik importowany, a następnie kliknij analizę. Referencyjne products.json jest opcjonalne na tym etapie.",
        "project.title": "Projekt mapowania",
        "project.help": "Zapisuje pliki, model i aktualne mapowanie, aby można było wrócić do pracy bez ponownego ustawiania importu.",
        "project.name": "Nazwa projektu",
        "project.save": "Zapisz projekt mapowania",
        "project.load": "Wczytaj projekt mapowania",
        "project.saved": "Projekt zapisany:",
        "project.loaded": "Wczytano projekt:",
        "project.missing": "Najpierw wczytaj pliki modelu.",
        "project.failed": "Nie udało się obsłużyć projektu.",
        "status.ready": "Analiza gotowa.",
        "status.missing": "Brakuje pliku: ",
        "status.error": "Błąd żądania",
        "modelBuilder.add": "Dodaj obiekt z modelu",
        "modelBuilder.empty": "Nie dodano jeszcze żadnego obiektu. Uzupełnij pola z modelu i kliknij Dodaj obiekt z modelu.",
        "modelBuilder.saved": "Ręczne obiekty z modelu",
        "modelBuilder.remove": "Usuń",
        "modelBuilder.valueHelp": "Dla produktów w jednej komórce możesz wpisać kilka identyfikatorów po przecinku."
      },
      en: {
        "nav.products": "Products",
        "nav.menu": "Back to main menu",
        "nav.buildingElements": "Building elements",
        "nav.colors": "Colors",
        "app.subtitle": "Building-element mapping based on the PIM model",
        "elements.title": "Building elements",
        "elements.help": "This module maps building elements. Reference products.json is optional and is used to verify product matching by ID, code, or name.",
        "elements.notice": "This is the first working screen for building elements. It will be expanded to the same operational depth as product mapping.",
        "workflow.mode": "Workflow mode",
        "workflow.import": "Import data and edit later",
        "workflow.modelBuilder": "Create systems from the model",
        "modelBuilder.title": "Building systems from the model",
        "modelBuilder.help": "Load the building-element model first. The manual editor must be generated from the model hierarchy, so it does not use an imported file or fixed fields.",
        "modelBuilder.load": "Load / refresh model",
        "elements.files": "Model, products and data",
        "elements.modelsFile": "buildingElementsModels.json",
        "elements.attributesFile": "buildingElementsAttributes.json",
        "elements.loadModel": "Load model hierarchy",
        "elements.activeModel": "Edited element model",
        "elements.productsReference": "Reference products.json (optional, for product-match verification)",
        "productIdentity.notice": "The product model is optional but recommended. It lets you choose which product attribute is the stable identifier used in layers.",
        "productIdentity.modelsFile": "productsModels.json",
        "productIdentity.attributesFile": "productsAttributes.json",
        "productIdentity.loadModel": "Load product model",
        "productIdentity.activeModel": "Product model for matching",
        "productIdentity.field": "Product identity attribute",
        "productIdentity.ready": "Product model loaded. Choose the product identity attribute.",
        "productIdentity.missing": "Load both product model files: Models and Attributes.",
        "productIdentity.none": "No product model loaded",
        "elements.importFile": "Imported file",
        "elements.analyze": "Analyze building elements",
        "elements.generate": "Generate building_elements.json",
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
        "status.error": "Request error",
        "modelBuilder.add": "Add object from model",
        "modelBuilder.empty": "No model object has been added yet. Fill model fields and click Add object from model.",
        "modelBuilder.saved": "Manual model objects",
        "modelBuilder.remove": "Remove",
        "modelBuilder.valueHelp": "For product fields you can enter multiple identifiers separated by commas."
      }
    };
    let currentLang = localStorage.getItem("aiDataMasterLang") || "pl";
    let lastElementAnalysis = null;
    let currentElementMapping = {};
    let elementRootModels = [];
    let activeElementRootModelId = "";
    let elementMappingsByModel = {};
    let elementProductRootModels = [];
    let activeElementProductRootModelId = "";
    let elementProductIdentityFields = [];
    let selectedElementProductIdentityField = "";
    let elementWorkflowMode = "import";
    let modelBuilderRows = [];
    let loadedElementProject = null;
    let loadedElementProjectFiles = { modelFiles: [], productModelFiles: [], sourceFile: null, productsReferenceFile: null };
    let lastElementPreview = null;
    let elementPreviewIndex = 0;
    let elementPreviewTimer = null;
    let elementPreviewRequestId = 0;
    let elementPreviewInFlight = false;
    let elementPreviewPending = false;
    let busyOperationCount = 0;
    const ELEMENT_WORKSPACE_KEY = "buildDataAiBuildingElementsWorkspace";
    const ELEMENT_WORKSPACE_FILES_KEY = "building-elements-files";
    const WORKSPACE_NAVIGATION_KEY = "buildDataAiPreserveWorkspaceNavigation";
    const $ = (id) => document.getElementById(id);
    function t(key) { return I18N[currentLang]?.[key] || I18N.pl[key] || key; }
    function setBusy(message) {
      busyOperationCount += 1;
      document.body.classList.add("is-busy");
      const overlay = $("busyOverlay");
      const messageTarget = $("busyMessage");
      if (messageTarget) messageTarget.textContent = message || (currentLang === "pl" ? "Przetwarzam dane..." : "Processing data...");
      if (overlay) overlay.hidden = false;
    }
    function clearBusy() {
      busyOperationCount = Math.max(0, busyOperationCount - 1);
      if (busyOperationCount > 0) return;
      document.body.classList.remove("is-busy");
      const overlay = $("busyOverlay");
      if (overlay) overlay.hidden = true;
    }
    function applyLanguage() {
      document.documentElement.lang = currentLang;
      $("languageSelect").value = currentLang;
      for (const element of document.querySelectorAll("[data-i18n]")) {
        element.textContent = t(element.dataset.i18n);
      }
    }
    function saveElementWorkspaceState() {
      try {
        const payload = {
          projectName: $("elementProjectName")?.value || "",
          analysis: lastElementAnalysis,
          mapping: currentElementMapping,
          elementRootModels,
          activeElementRootModelId,
          elementMappingsByModel,
          elementProductRootModels,
          activeElementProductRootModelId,
          elementProductIdentityFields,
          selectedElementProductIdentityField,
          elementWorkflowMode,
          modelBuilderRows,
          status: $("elementStatus")?.textContent || "",
          productIdentityStatus: $("elementProductIdentityStatus")?.textContent || "",
          savedAt: new Date().toISOString(),
        };
        const serialized = JSON.stringify(payload);
        sessionStorage.setItem(ELEMENT_WORKSPACE_KEY, serialized);
        localStorage.setItem(ELEMENT_WORKSPACE_KEY, serialized);
      } catch (error) {
        console.warn("Could not save building-elements workspace state", error);
      }
    }
    function openElementWorkspaceDb() {
      return new Promise((resolve, reject) => {
        const request = indexedDB.open("BuildDataAIWorkspace", 1);
        request.onupgradeneeded = () => request.result.createObjectStore("items");
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
      });
    }
    async function setElementWorkspaceItem(key, value) {
      const db = await openElementWorkspaceDb();
      await new Promise((resolve, reject) => {
        const tx = db.transaction("items", "readwrite");
        tx.objectStore("items").put(value, key);
        tx.oncomplete = resolve;
        tx.onerror = () => reject(tx.error);
      });
      db.close();
    }
    async function getElementWorkspaceItem(key) {
      const db = await openElementWorkspaceDb();
      const value = await new Promise((resolve, reject) => {
        const tx = db.transaction("items", "readonly");
        const request = tx.objectStore("items").get(key);
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
      });
      db.close();
      return value;
    }
    async function deleteElementWorkspaceItem(key) {
      const db = await openElementWorkspaceDb();
      await new Promise((resolve, reject) => {
        const tx = db.transaction("items", "readwrite");
        tx.objectStore("items").delete(key);
        tx.oncomplete = resolve;
        tx.onerror = () => reject(tx.error);
      });
      db.close();
    }
    async function clearElementWorkspaceStorage() {
      sessionStorage.removeItem(ELEMENT_WORKSPACE_KEY);
      localStorage.removeItem(ELEMENT_WORKSPACE_KEY);
      try {
        await deleteElementWorkspaceItem(ELEMENT_WORKSPACE_FILES_KEY);
      } catch (error) {
        console.warn("Could not clear building-elements files state", error);
      }
    }
    function isPageReload() {
      const navigation = performance.getEntriesByType?.("navigation")?.[0];
      return navigation?.type === "reload";
    }
    function markWorkspaceNavigation() {
      sessionStorage.setItem(WORKSPACE_NAVIGATION_KEY, String(Date.now()));
    }
    function consumeWorkspaceNavigationMarker() {
      const raw = sessionStorage.getItem(WORKSPACE_NAVIGATION_KEY);
      sessionStorage.removeItem(WORKSPACE_NAVIGATION_KEY);
      if (!raw) return false;
      const ageMs = Date.now() - Number(raw);
      return Number.isFinite(ageMs) && ageMs < 30000;
    }
    async function saveElementWorkspaceFilesState() {
      try {
        const previous = await getElementWorkspaceItem(ELEMENT_WORKSPACE_FILES_KEY) || {};
        const modelFiles = selectedElementModelFiles();
        const productModelFiles = selectedElementProductModelFiles();
        const sourceFile = $("elementSourceFile").files[0] || null;
        const productsReferenceFile = $("productReferenceFile").files[0] || null;
        const payload = {
          modelFiles: modelFiles.length
            ? await Promise.all(modelFiles.map(projectFileFromFile))
            : (loadedElementProjectFiles.modelFiles.length ? await Promise.all(loadedElementProjectFiles.modelFiles.map(projectFileFromFile)) : (previous.modelFiles || [])),
          productModelFiles: productModelFiles.length
            ? await Promise.all(productModelFiles.map(projectFileFromFile))
            : (loadedElementProjectFiles.productModelFiles.length ? await Promise.all(loadedElementProjectFiles.productModelFiles.map(projectFileFromFile)) : (previous.productModelFiles || [])),
          sourceFile: sourceFile ? await projectFileFromFile(sourceFile) : (loadedElementProjectFiles.sourceFile ? await projectFileFromFile(loadedElementProjectFiles.sourceFile) : (previous.sourceFile || null)),
          productsReferenceFile: productsReferenceFile ? await projectFileFromFile(productsReferenceFile) : (loadedElementProjectFiles.productsReferenceFile ? await projectFileFromFile(loadedElementProjectFiles.productsReferenceFile) : (previous.productsReferenceFile || null)),
          savedAt: new Date().toISOString(),
        };
        await setElementWorkspaceItem(ELEMENT_WORKSPACE_FILES_KEY, payload);
      } catch (error) {
        console.warn("Could not save building-elements files state", error);
      }
    }
    async function restoreElementWorkspaceFilesState() {
      try {
        const payload = await getElementWorkspaceItem(ELEMENT_WORKSPACE_FILES_KEY);
        if (!payload) return;
        loadedElementProjectFiles = {
          modelFiles: (payload.modelFiles || []).map(fileFromProjectFile).filter(Boolean),
          productModelFiles: (payload.productModelFiles || []).map(fileFromProjectFile).filter(Boolean),
          sourceFile: fileFromProjectFile(payload.sourceFile),
          productsReferenceFile: fileFromProjectFile(payload.productsReferenceFile),
        };
      } catch (error) {
        console.warn("Could not restore building-elements files state", error);
      }
    }
    async function restoreElementWorkspaceState() {
      try {
        await restoreElementWorkspaceFilesState();
        const raw = sessionStorage.getItem(ELEMENT_WORKSPACE_KEY) || localStorage.getItem(ELEMENT_WORKSPACE_KEY);
        if (!raw) return;
        const payload = JSON.parse(raw);
        currentElementMapping = payload.mapping || {};
        elementRootModels = payload.elementRootModels || elementRootModels;
        activeElementRootModelId = String(payload.activeElementRootModelId || activeElementRootModelId || "");
        elementMappingsByModel = payload.elementMappingsByModel || elementMappingsByModel;
        elementProductRootModels = payload.elementProductRootModels || elementProductRootModels;
        activeElementProductRootModelId = String(payload.activeElementProductRootModelId || activeElementProductRootModelId || "");
        elementProductIdentityFields = payload.elementProductIdentityFields || elementProductIdentityFields;
        selectedElementProductIdentityField = payload.selectedElementProductIdentityField || selectedElementProductIdentityField;
        elementWorkflowMode = payload.elementWorkflowMode || elementWorkflowMode;
        modelBuilderRows = Array.isArray(payload.modelBuilderRows) ? payload.modelBuilderRows : modelBuilderRows;
        if ($("elementWorkflowMode")) $("elementWorkflowMode").value = elementWorkflowMode;
        updateElementWorkflowMode();
        if (payload.projectName && $("elementProjectName")) $("elementProjectName").value = payload.projectName;
        if (payload.status && $("elementStatus")) $("elementStatus").textContent = payload.status;
        if (payload.productIdentityStatus && $("elementProductIdentityStatus")) $("elementProductIdentityStatus").textContent = payload.productIdentityStatus;
        renderElementProductIdentityControls();
        if (payload.analysis) renderElementAnalysis(payload.analysis);
        else if (loadedElementProjectFiles.modelFiles.length >= 2) await loadElementModelHierarchy();
      } catch (error) {
        console.warn("Could not restore building-elements workspace state", error);
      }
    }
    $("languageSelect").addEventListener("change", (event) => {
      currentLang = event.target.value;
      localStorage.setItem("aiDataMasterLang", currentLang);
      applyLanguage();
      saveElementWorkspaceState();
    });
    async function persistElementWorkspaceBeforeNavigation(event) {
      const link = event.currentTarget;
      if (!link?.href) return;
      event.preventDefault();
      syncElementMappingState();
      saveElementWorkspaceState();
      await saveElementWorkspaceFilesState();
      markWorkspaceNavigation();
      window.location.href = link.href;
    }
    for (const link of document.querySelectorAll(".top-nav a")) {
      link.addEventListener("click", persistElementWorkspaceBeforeNavigation);
    }
    window.addEventListener("pagehide", () => {
      syncElementMappingState();
      saveElementWorkspaceState();
    });
    function updateElementWorkflowMode() {
      elementWorkflowMode = $("elementWorkflowMode")?.value || elementWorkflowMode || "import";
      const importMode = elementWorkflowMode === "import";
      if ($("elementSourceFile")) $("elementSourceFile").disabled = !importMode;
      if ($("modelBuilderPanel")) $("modelBuilderPanel").hidden = importMode;
      if ($("modelBuilderStatus")) {
        $("modelBuilderStatus").textContent = importMode
          ? ""
          : (lastElementAnalysis?.model ? (currentLang === "pl" ? "Model jest wczytany. Możesz dodawać obiekty z pól modelu." : "Model loaded. You can add objects from model fields.") : (currentLang === "pl" ? "Wczytaj model elementów, aby rozpocząć budowanie systemów." : "Load the element model to start building systems."));
      }
      if (lastElementAnalysis?.model) renderElementAnalysis(lastElementAnalysis);
      saveElementWorkspaceState();
    }
    function addFiles(form, name, input) {
      [...input.files].forEach((file) => form.append(name, file));
    }
    function addFilesFromList(form, name, files) {
      [...(files || [])].forEach((file) => form.append(name, file));
    }
    function elementRootModelKey() {
      return String(activeElementRootModelId || elementRootModels[0]?.id || "default");
    }
    function renderElementRootModelSelect() {
      const select = $("elementRootModelSelect");
      if (!select) return;
      select.innerHTML = elementRootModels.length
        ? elementRootModels.map(model => `<option value="${escapeHtml(model.id)}"${String(model.id) === String(activeElementRootModelId) ? " selected" : ""}>${escapeHtml(model.name || model.id)} (${escapeHtml(model.modelType || "Building_Element")})</option>`).join("")
        : `<option value="">${escapeHtml(currentLang === "pl" ? "Brak modeli elementów" : "No element models")}</option>`;
      select.disabled = !elementRootModels.length;
    }
    function storeElementMappingForActiveModel() {
      const key = elementRootModelKey();
      if (!key || key === "default") return;
      elementMappingsByModel[key] = JSON.parse(JSON.stringify(currentElementMapping || {}));
    }
    function restoreElementMappingForActiveModel() {
      currentElementMapping = elementMappingsByModel[elementRootModelKey()] || {};
    }
    async function changeElementRootModel(rootModelId) {
      if (!rootModelId || String(rootModelId) === String(activeElementRootModelId)) return;
      syncElementMappingState();
      storeElementMappingForActiveModel();
      activeElementRootModelId = String(rootModelId);
      restoreElementMappingForActiveModel();
      await loadElementModelHierarchy();
      saveElementWorkspaceState();
    }
    function selectedElementModelFiles() {
      return [
        $("elementModelsFile")?.files?.[0] || null,
        $("elementAttributesFile")?.files?.[0] || null,
      ].filter(Boolean);
    }
    function selectedElementProductModelFiles() {
      return [
        $("elementProductModelsFile")?.files?.[0] || null,
        $("elementProductAttributesFile")?.files?.[0] || null,
      ].filter(Boolean);
    }
    function elementModelFileFromCache(kind) {
      const pattern = kind === "models" ? /models[.]json$/i : /attributes[.]json$/i;
      return (loadedElementProjectFiles.modelFiles || []).find((file) => pattern.test(file?.name || "")) || null;
    }
    function elementProductModelFileFromCache(kind) {
      const pattern = kind === "models" ? /models[.]json$/i : /attributes[.]json$/i;
      return (loadedElementProjectFiles.productModelFiles || []).find((file) => pattern.test(file?.name || "")) || null;
    }
    function effectiveElementModelFiles() {
      const selected = selectedElementModelFiles();
      if (selected.length) {
        return [
          $("elementModelsFile")?.files?.[0] || elementModelFileFromCache("models"),
          $("elementAttributesFile")?.files?.[0] || elementModelFileFromCache("attributes"),
        ].filter(Boolean);
      }
      return loadedElementProjectFiles.modelFiles || [];
    }
    function effectiveElementProductModelFiles() {
      const selected = selectedElementProductModelFiles();
      if (selected.length) {
        return [
          $("elementProductModelsFile")?.files?.[0] || elementProductModelFileFromCache("models"),
          $("elementProductAttributesFile")?.files?.[0] || elementProductModelFileFromCache("attributes"),
        ].filter(Boolean);
      }
      return loadedElementProjectFiles.productModelFiles || [];
    }
    function renderElementProductIdentityControls() {
      const modelSelect = $("elementProductRootModelSelect");
      const fieldSelect = $("elementProductIdentityFieldSelect");
      if (!modelSelect || !fieldSelect) return;
      modelSelect.innerHTML = elementProductRootModels.length
        ? elementProductRootModels.map(model => `<option value="${escapeHtml(model.id)}"${String(model.id) === String(activeElementProductRootModelId) ? " selected" : ""}>${escapeHtml(model.name || model.id)} (${escapeHtml(model.modelType || "Product")})</option>`).join("")
        : `<option value="">${escapeHtml(t("productIdentity.none"))}</option>`;
      modelSelect.disabled = !elementProductRootModels.length;
      fieldSelect.innerHTML = elementProductIdentityFields.length
        ? elementProductIdentityFields.map(field => `<option value="${escapeHtml(field.key)}"${field.key === selectedElementProductIdentityField ? " selected" : ""}>${escapeHtml(field.label || field.key)} (${escapeHtml(field.key)})</option>`).join("")
        : `<option value="">${escapeHtml(t("productIdentity.none"))}</option>`;
      fieldSelect.disabled = !elementProductIdentityFields.length;
    }
    function scoreProductIdentityField(field) {
      const text = `${field.key || ""} ${field.label || ""}`.toLowerCase();
      if (/pim.*id|id.*pim/.test(text)) return 100;
      if (/external.*id|id.*external/.test(text)) return 95;
      if (/sku|sap|code|kod|indeks|index/.test(text)) return 90;
      if (/\bid\b/.test(text)) return 80;
      if (/name|nazwa/.test(text)) return 10;
      return 0;
    }
    function suggestProductIdentityField(fields) {
      return [...(fields || [])].sort((left, right) => scoreProductIdentityField(right) - scoreProductIdentityField(left))[0]?.key || "";
    }
    async function changeElementProductRootModel(rootModelId) {
      if (!rootModelId || String(rootModelId) === String(activeElementProductRootModelId)) return;
      activeElementProductRootModelId = String(rootModelId);
      await loadElementProductModel();
      saveElementWorkspaceState();
      await saveElementWorkspaceFilesState();
    }
    async function loadElementProductModel() {
      try {
        setBusy(currentLang === "pl" ? "Odczytuję model produktu..." : "Reading product model...");
        $("elementProductIdentityStatus").textContent = currentLang === "pl" ? "Odczytuję model produktu." : "Reading product model.";
        if (!selectedElementProductModelFiles().length && !loadedElementProjectFiles.productModelFiles.length) {
          await restoreElementWorkspaceFilesState();
        }
        const modelFiles = effectiveElementProductModelFiles();
        if (modelFiles.length < 2) throw new Error(t("productIdentity.missing"));
        const form = new FormData();
        addFilesFromList(form, "files", modelFiles);
        if (activeElementProductRootModelId) form.append("root_model_id", activeElementProductRootModelId);
        const payload = await postForm("/api/products/model", form);
        elementProductRootModels = payload.model?.root_models || [];
        activeElementProductRootModelId = String(payload.model?.root_model_id || activeElementProductRootModelId || elementProductRootModels[0]?.id || "");
        elementProductIdentityFields = payload.model?.fields || [];
        if (!selectedElementProductIdentityField || !elementProductIdentityFields.some(field => field.key === selectedElementProductIdentityField)) {
          selectedElementProductIdentityField = suggestProductIdentityField(elementProductIdentityFields);
        }
        renderElementProductIdentityControls();
        $("elementProductIdentityStatus").textContent = t("productIdentity.ready");
        saveElementWorkspaceState();
        await saveElementWorkspaceFilesState();
      } catch (error) {
        $("elementProductIdentityStatus").textContent = error.message;
        saveElementWorkspaceState();
      } finally {
        clearBusy();
      }
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
    async function saveGeneratedElementFile(url, suggestedName) {
      const response = await fetch(url);
      if (!response.ok) throw new Error(currentLang === "pl" ? "Nie udało się pobrać pliku wynikowego." : "Could not download generated file.");
      const blob = await response.blob();
      if (window.showSaveFilePicker) {
        const handle = await window.showSaveFilePicker({
          suggestedName,
          types: [{ description: "JSON", accept: { "application/json": [".json"] } }],
        });
        const writable = await handle.createWritable();
        await writable.write(blob);
        await writable.close();
        return handle.name || suggestedName;
      }
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = suggestedName;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(link.href);
      return suggestedName;
    }
    async function elementProjectPayload() {
      syncElementMappingState();
      storeElementMappingForActiveModel();
      const effectiveModelFiles = effectiveElementModelFiles();
      const productModelFiles = effectiveElementProductModelFiles();
      const sourceFile = $("elementSourceFile").files[0] || loadedElementProjectFiles.sourceFile;
      const productsReferenceFile = $("productReferenceFile").files[0] || loadedElementProjectFiles.productsReferenceFile;
      if (!effectiveModelFiles.length) throw new Error(t("project.missing"));
      return {
        name: $("elementProjectName").value || "mapowanie-elementow-budowlanych",
        model_version: "building-elements-mapping-project.v1",
        active_element_root_model_id: activeElementRootModelId || "",
        workflow_mode: elementWorkflowMode || "import",
        element_root_models: elementRootModels || [],
        element_mappings_by_model: elementMappingsByModel || {},
        product_identity: {
          active_product_root_model_id: activeElementProductRootModelId || "",
          identity_field_key: selectedElementProductIdentityField || "",
          identity_fields: elementProductIdentityFields || [],
          product_root_models: elementProductRootModels || [],
        },
        model_builder_rows: modelBuilderRows || [],
        building_element_mapping: currentElementMapping || {},
        analysis: lastElementAnalysis,
        embedded_files: {
          model_files: await Promise.all(effectiveModelFiles.map(file => projectFileFromFile(file))),
          product_model_files: await Promise.all(productModelFiles.map(file => projectFileFromFile(file))),
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
          productModelFiles: (embedded.product_model_files || []).map(fileFromProjectFile).filter(Boolean),
          sourceFile: fileFromProjectFile(embedded.source_file),
          productsReferenceFile: fileFromProjectFile(embedded.products_reference_file),
        };
        const productIdentity = loadedElementProject.product_identity || {};
        elementProductRootModels = productIdentity.product_root_models || elementProductRootModels;
        activeElementProductRootModelId = String(productIdentity.active_product_root_model_id || activeElementProductRootModelId || "");
        elementProductIdentityFields = productIdentity.identity_fields || elementProductIdentityFields;
        selectedElementProductIdentityField = productIdentity.identity_field_key || selectedElementProductIdentityField;
        elementRootModels = loadedElementProject.element_root_models || elementRootModels;
        activeElementRootModelId = String(loadedElementProject.active_element_root_model_id || activeElementRootModelId || "");
        elementWorkflowMode = loadedElementProject.workflow_mode || elementWorkflowMode || "import";
        if ($("elementWorkflowMode")) $("elementWorkflowMode").value = elementWorkflowMode;
        elementMappingsByModel = loadedElementProject.element_mappings_by_model || elementMappingsByModel;
        currentElementMapping = loadedElementProject.building_element_mapping || {};
        modelBuilderRows = Array.isArray(loadedElementProject.model_builder_rows) ? loadedElementProject.model_builder_rows : [];
        if (activeElementRootModelId) elementMappingsByModel[activeElementRootModelId] = currentElementMapping;
        $("elementProjectName").value = loadedElementProject.name || "mapowanie-elementow-budowlanych";
        $("elementProjectStatus").textContent = `${t("project.loaded")} ${loadedElementProject.name || file.name}`;
        saveElementWorkspaceState();
        await saveElementWorkspaceFilesState();
        renderElementProductIdentityControls();
        updateElementWorkflowMode();
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
        setBusy(currentLang === "pl" ? "Wczytuję hierarchię modelu..." : "Loading model hierarchy...");
        $("elementStatus").textContent = currentLang === "pl"
          ? "Proszę czekać, trwa odczyt hierarchii modelu."
          : "Please wait, model hierarchy is loading.";
        if (!selectedElementModelFiles().length && !loadedElementProjectFiles.modelFiles.length) {
          await restoreElementWorkspaceFilesState();
        }
        const modelFiles = effectiveElementModelFiles();
        if (modelFiles.length < 2) throw new Error(currentLang === "pl" ? "Wczytaj oba pliki modelu: Models i Attributes." : "Load both model files: Models and Attributes.");
        addFilesFromList(form, "files", modelFiles);
        if (activeElementRootModelId) form.append("root_model_id", activeElementRootModelId);
        const payload = await postForm("/api/building-elements/model", form);
        elementRootModels = payload.model?.root_models || [];
        activeElementRootModelId = String(payload.model?.root_model_id || activeElementRootModelId || elementRootModels[0]?.id || "");
        if (activeElementRootModelId && Object.keys(currentElementMapping || {}).length && !elementMappingsByModel[activeElementRootModelId]) {
          elementMappingsByModel[activeElementRootModelId] = JSON.parse(JSON.stringify(currentElementMapping));
        }
        restoreElementMappingForActiveModel();
        renderElementRootModelSelect();
        renderElementAnalysis({
          model: payload.model,
          tables: [],
          product_reference: {
            products_count: 0,
            message: elementWorkflowMode === "modelBuilder"
              ? "Wczytano hierarchię modelu. Możesz tworzyć elementy z pól modelu bez pliku importowanego."
              : "Wczytano hierarchię modelu. Dodaj plik importowany, aby mapować kolumny.",
          },
        });
        $("elementStatus").textContent = t("status.ready");
        saveElementWorkspaceState();
      } catch (error) {
        $("elementStatus").textContent = error.message;
        saveElementWorkspaceState();
      } finally {
        clearBusy();
      }
    }
    async function analyzeElements() {
      const form = new FormData();
      try {
        setBusy(currentLang === "pl" ? "Analizuję duży plik klienta..." : "Analyzing customer file...");
        $("elementStatus").textContent = currentLang === "pl"
          ? "Proszę czekać, trwa analiza pliku klienta."
          : "Please wait, customer file analysis is running.";
        if ((!selectedElementModelFiles().length && !loadedElementProjectFiles.modelFiles.length) || (!$("elementSourceFile").files[0] && !loadedElementProjectFiles.sourceFile)) {
          await restoreElementWorkspaceFilesState();
        }
        const modelFiles = effectiveElementModelFiles();
        if (modelFiles.length < 2) throw new Error(currentLang === "pl" ? "Wczytaj oba pliki modelu: Models i Attributes." : "Load both model files: Models and Attributes.");
        addFilesFromList(form, "model_files", modelFiles);
        if (activeElementRootModelId) form.append("root_model_id", activeElementRootModelId);
        addOptionalProjectFile(form, "products_reference", $("productReferenceFile"), loadedElementProjectFiles.productsReferenceFile);
        addRequiredProjectFile(form, "file", $("elementSourceFile"), loadedElementProjectFiles.sourceFile, t("elements.importFile"));
        const payload = await postForm("/api/building-elements/analyze", form);
        elementRootModels = payload.model?.root_models || elementRootModels;
        activeElementRootModelId = String(payload.model?.root_model_id || activeElementRootModelId || elementRootModels[0]?.id || "");
        if (activeElementRootModelId && Object.keys(currentElementMapping || {}).length && !elementMappingsByModel[activeElementRootModelId]) {
          elementMappingsByModel[activeElementRootModelId] = JSON.parse(JSON.stringify(currentElementMapping));
        }
        restoreElementMappingForActiveModel();
        renderElementRootModelSelect();
        renderElementAnalysis(payload);
        $("elementStatus").textContent = t("status.ready");
        saveElementWorkspaceState();
      } catch (error) {
        $("elementStatus").textContent = error.message;
        saveElementWorkspaceState();
      } finally {
        clearBusy();
      }
    }
    async function generateBuildingElements() {
      const form = new FormData();
      try {
        setBusy(currentLang === "pl" ? "Generuję building_elements.json..." : "Generating building_elements.json...");
        syncElementMappingState(false);
        $("elementStatus").textContent = currentLang === "pl"
          ? "Generuję building_elements.json."
          : "Generating building_elements.json.";
        const builderMode = elementWorkflowMode === "modelBuilder";
        if ((!selectedElementModelFiles().length && !loadedElementProjectFiles.modelFiles.length) || (!builderMode && !$("elementSourceFile").files[0] && !loadedElementProjectFiles.sourceFile)) {
          await restoreElementWorkspaceFilesState();
        }
        const modelFiles = effectiveElementModelFiles();
        if (modelFiles.length < 2) throw new Error(currentLang === "pl" ? "Wczytaj oba pliki modelu: Models i Attributes." : "Load both model files: Models and Attributes.");
        addFilesFromList(form, "model_files", modelFiles);
        addOptionalProjectFile(form, "products_reference", $("productReferenceFile"), loadedElementProjectFiles.productsReferenceFile);
        if (builderMode) {
          if (!modelBuilderRows.length) {
            throw new Error(currentLang === "pl" ? "Dodaj przynajmniej jeden obiekt z modelu." : "Add at least one object from the model.");
          }
          form.append("file", modelBuilderSourceFile());
        } else {
          addRequiredProjectFile(form, "file", $("elementSourceFile"), loadedElementProjectFiles.sourceFile, t("elements.importFile"));
        }
        if (activeElementRootModelId) form.append("root_model_id", activeElementRootModelId);
        form.append("mapping_json", JSON.stringify(builderMode ? modelBuilderMappingProfile() : (currentElementMapping || {})));
        const payload = await postForm("/api/building-elements/convert", form);
        const saved = await saveGeneratedElementFile(payload.files.building_elements_json, "building_elements.json");
        $("elementStatus").textContent = currentLang === "pl"
          ? `Gotowe. Zapisano ${saved}.`
          : `Done. Saved ${saved}.`;
        saveElementWorkspaceState();
      } catch (error) {
        $("elementStatus").textContent = error.message;
        saveElementWorkspaceState();
      } finally {
        clearBusy();
      }
    }
    function scheduleElementLivePreview(delay = 900) {
      if (elementPreviewTimer) clearTimeout(elementPreviewTimer);
      elementPreviewTimer = setTimeout(updateElementLivePreview, delay);
    }
    function setElementPreviewIndex(delta) {
      const quality = lastElementPreview?.quality || {};
      const total = Number(quality.systems || 0);
      if (!total) return;
      elementPreviewIndex = Math.min(Math.max(elementPreviewIndex + delta, 0), Math.max(total - 1, 0));
      scheduleElementLivePreview(0);
      saveElementWorkspaceState();
    }
    function renderElementVisualPreview(system, currentLabel) {
      if (!system) {
        return `<div class="element-visual-preview"><div class="visual-empty">Brak danych do podglądu.</div></div>`;
      }
      const variantCards = [];
      for (const variant of system.variants || []) {
        const layerCards = [];
        for (const layer of variant.layers || []) {
          const productCards = [];
          for (const product of layer.products || []) {
            const scopeLabel = product.variant_scope_label || (product.resolved
              ? (product.variant_hash ? "tylko wskazany wariant" : "wszystkie warianty produktu")
              : "brak dopasowania");
            const status = product.resolved
              ? (product.variant_hash ? "wariant produktu" : "produkt z wariantami")
              : "nie rozpoznano";
            const recognized = product.resolved
              ? `${product.variant_hash ? "Wariant" : "Produkt"}: ${product.product_name || product.product_id || ""}${product.variant_label ? ` / ${product.variant_label}` : ""}`
              : "Brak dopasowania w referencyjnym products.json";
            productCards.push(`
              <div class="product-visual-chip ${product.resolved ? "is-ok" : "is-warn"}">
                <strong>${escapeHtml(product.raw || "")}</strong>
                <span>${escapeHtml(recognized)}</span>
                <span>Zakres: ${escapeHtml(scopeLabel)}</span>
                <span>Status: ${escapeHtml(status)}${product.identity_source ? ` / dopasowanie: ${escapeHtml(product.identity_source)}` : ""}</span>
              </div>
            `);
          }
          if (!layer.products?.length) {
            productCards.push(`
              <div class="product-visual-chip is-warn">
                <strong>Brak produktu</strong>
                <span>Brak zmapowanych produktów dla tej warstwy.</span>
              </div>
            `);
          }
          layerCards.push(`
            <div class="layer-visual-card">
              <div class="layer-visual-head">${escapeHtml(layer.name || "Warstwa bez nazwy")}</div>
              <div class="product-visual-list">${productCards.join("")}</div>
            </div>
          `);
        }
        variantCards.push(`
          <div class="variant-visual-card">
            <div class="variant-visual-head">${escapeHtml(variant.name || "Wariant domyślny")}</div>
            ${layerCards.join("") || `<div class="visual-empty">Brak warstw w tym wariancie.</div>`}
          </div>
        `);
      }
      return `<div class="element-visual-preview">
        <div class="element-visual-card">
          <div class="element-visual-title">
            <strong>${escapeHtml(system.name || "System bez nazwy")}</strong>
            <span>${escapeHtml(currentLabel)} / warianty: ${(system.variants || []).length}</span>
          </div>
          <div class="variant-visual-grid">${variantCards.join("") || `<div class="visual-empty">Brak wariantów dla tego elementu.</div>`}</div>
        </div>
      </div>`;
    }
    function renderElementLivePreview(preview, message = "") {
      if (!preview) {
        return `<div class="live-preview" id="elementLivePreview">
          <div class="live-preview-head">
            <div>
              <h3>Podgląd na żywo mapowania</h3>
              <p>${escapeHtml(message || "Wybierz mapowanie kolumn, aby zobaczyć rozpoznane systemy, warstwy oraz produkty i warianty.")}</p>
            </div>
          </div>
        </div>`;
      }
      const quality = preview.quality || {};
      const systems = preview.systems || [];
      const system = systems[0] || null;
      const currentOffset = Number(quality.preview_offset ?? elementPreviewIndex ?? 0);
      const totalSystems = Number(quality.systems || systems.length || 0);
      elementPreviewIndex = currentOffset;
      const currentLabel = totalSystems
        ? (quality.systems_count_is_exact ? `Element ${currentOffset + 1} / ${totalSystems}` : `Element ${currentOffset + 1}`)
        : "Element 0";
      const rows = [];
      if (system) {
        for (const variant of system.variants || []) {
          for (const layer of variant.layers || []) {
            for (const product of layer.products || []) {
              const scopeLabel = product.variant_scope_label || (product.resolved
                ? (product.variant_hash ? "tylko wskazany wariant" : "wszystkie warianty produktu")
                : "brak dopasowania");
              const status = product.resolved
                ? (product.variant_hash ? "wariant produktu" : "produkt z wariantami")
                : "nie rozpoznano";
              const recognized = product.resolved
                ? `${product.variant_hash ? "Wariant" : "Produkt"}: ${product.product_name || product.product_id || ""}${product.variant_label ? ` / ${product.variant_label}` : ""}`
                : "Brak dopasowania w referencyjnym products.json";
              rows.push(`
                <tr>
                  <td>${escapeHtml(system.name || "")}<div class="preview-path">${escapeHtml(variant.name || "")}</div></td>
                  <td>${escapeHtml(layer.name || "")}</td>
                  <td>${escapeHtml(product.raw || "")}</td>
                  <td>${escapeHtml(recognized)}</td>
                  <td class="${product.resolved ? "status-ok" : "status-warn"}">${escapeHtml(status)}</td>
                  <td>${escapeHtml(scopeLabel)}${product.identity_source ? ` / ${escapeHtml(product.identity_source)}` : ""}</td>
                </tr>
              `);
            }
            if (!layer.products?.length) {
              rows.push(`
                <tr>
                  <td>${escapeHtml(system.name || "")}<div class="preview-path">${escapeHtml(variant.name || "")}</div></td>
                  <td>${escapeHtml(layer.name || "")}</td>
                  <td colspan="4" class="status-warn">Brak zmapowanych produktów dla tej warstwy</td>
                </tr>
              `);
            }
          }
        }
      }
      return `<div class="live-preview" id="elementLivePreview">
        <div class="live-preview-head">
          <div>
            <h3>Podgląd na żywo mapowania</h3>
            <p>Pokazuje, jak aktualne mapowanie zostanie odczytane przed wygenerowaniem building_elements.json.</p>
          </div>
          <div class="live-preview-nav">
            <button type="button" class="secondary" onclick="setElementPreviewIndex(-1)"${quality.has_previous ? "" : " disabled"}>Poprzedni element</button>
            <span class="pill">${escapeHtml(currentLabel)}</span>
            <button type="button" class="secondary" onclick="setElementPreviewIndex(1)"${quality.has_next ? "" : " disabled"}>Następny element</button>
            <span class="pill">${quality.systems_count_is_exact ? "systemy" : "systemy sprawdzone"}: ${escapeHtml(quality.systems || 0)}</span>
            <span class="pill">nierozpoznane produkty: ${escapeHtml(quality.unresolved_products_count || 0)}</span>
            <span class="pill">referencja produktów: ${quality.product_reference_loaded ? "wczytana" : "brak"}</span>
          </div>
        </div>
        ${renderElementVisualPreview(system, currentLabel)}
        <div class="live-preview-table-wrap" hidden>
          <table class="live-preview-table">
            <thead><tr><th>System / wariant</th><th>Warstwa</th><th>Wartość klienta</th><th>Rozpoznanie</th><th>Status</th><th>Dopasowanie</th></tr></thead>
            <tbody>${rows.join("") || `<tr><td colspan="6">Brak danych do podglądu.</td></tr>`}</tbody>
          </table>
        </div>
      </div>`;
    }
    async function updateElementLivePreview() {
      const holder = $("elementLivePreview");
      if (!holder || !lastElementAnalysis) return;
      if (elementPreviewInFlight) {
        elementPreviewPending = true;
        return;
      }
      elementPreviewInFlight = true;
      elementPreviewPending = false;
      const requestId = ++elementPreviewRequestId;
      try {
        setBusy(currentLang === "pl" ? "Odświeżam podgląd mapowania..." : "Refreshing mapping preview...");
        syncElementMappingState(false);
        const builderMode = elementWorkflowMode === "modelBuilder";
        const sourceFile = builderMode ? modelBuilderSourceFile() : ($("elementSourceFile").files[0] || loadedElementProjectFiles.sourceFile);
        if (!sourceFile) {
          holder.outerHTML = renderElementLivePreview(null, "Wczytaj plik klienta, aby zobaczyć podgląd na żywo.");
          return;
        }
        const form = new FormData();
        form.append("file", sourceFile);
        addOptionalProjectFile(form, "products_reference", $("productReferenceFile"), loadedElementProjectFiles.productsReferenceFile);
        form.append("mapping_json", JSON.stringify(builderMode ? modelBuilderMappingProfile() : (currentElementMapping || {})));
        form.append("preview_offset", String(elementPreviewIndex || 0));
        form.append("preview_limit", "1");
        const preview = await postForm("/api/building-elements/preview", form);
        if (requestId !== elementPreviewRequestId) return;
        lastElementPreview = preview;
        if (elementPreviewIndex >= Number(preview.quality?.systems || 0)) elementPreviewIndex = 0;
        const currentHolder = $("elementLivePreview");
        if (currentHolder) currentHolder.outerHTML = renderElementLivePreview(preview);
      } catch (error) {
        if (requestId !== elementPreviewRequestId) return;
        const currentHolder = $("elementLivePreview");
        if (currentHolder) currentHolder.outerHTML = renderElementLivePreview(null, error?.message || "Nie udało się odświeżyć podglądu.");
      } finally {
        elementPreviewInFlight = false;
        clearBusy();
        if (elementPreviewPending) {
          elementPreviewPending = false;
          scheduleElementLivePreview(150);
        }
      }
    }
    function escapeHtml(value) {
      return String(value ?? "").replace(/[&<>"']/g, (char) => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
      }[char]));
    }
    function modelBuilderFieldsFromHierarchy(model) {
      const fields = [];
      const seen = new Set();
      const levelLabels = Object.fromEntries(modelBuilderLevelsFromHierarchy(model).map((level) => [level.key, level.label]));
      function visit(node, trail = []) {
        if (!node) return;
        const labelTrail = [...trail, node.label || node.key || ""].filter(Boolean);
        for (const field of node.fields || []) {
          if (!field?.key || seen.has(field.key)) continue;
          seen.add(field.key);
          fields.push({ ...field, _level_label: labelTrail.join(" / "), _level_key: node.key || "" });
        }
        for (const child of node.children || []) visit(child, labelTrail);
      }
      visit(model?.hierarchy);
      if (!fields.length) {
        for (const field of model?.fields || []) {
          if (!field?.key || seen.has(field.key)) continue;
          seen.add(field.key);
          fields.push({
            ...field,
            _level_label: field.parent_relation_key ? (levelLabels[field.parent_relation_key] || field.parent_relation_key) : (model?.root_model_name || "Model"),
            _level_key: field.parent_relation_key || (model?.hierarchy?.key || `model.${model?.root_model_id || "root"}`),
          });
        }
      }
      return fields;
    }
    function modelBuilderLevelsFromHierarchy(model) {
      const levels = [];
      function visit(node, trail = []) {
        if (!node) return;
        const labelTrail = [...trail, node.label || node.key || ""].filter(Boolean);
        levels.push({
          key: node.key || "",
          label: labelTrail.join(" / ") || node.key || "",
          type: node.type || "model",
        });
        for (const child of node.children || []) visit(child, labelTrail);
      }
      visit(model?.hierarchy);
      if (!levels.length && model?.root_model_id) {
        levels.push({ key: `model.${model.root_model_id}`, label: model.root_model_name || "Model", type: "model" });
      }
      return levels.filter((level) => level.key);
    }
    function modelBuilderLevelControlsHtml(model) {
      const levels = modelBuilderLevelsFromHierarchy(model);
      if (!levels.length) return "";
      const controls = levels.map((level) => {
        const key = escapeHtml(level.key);
        const label = escapeHtml(level.label);
        const parentInput = level.type === "relation" ? `
          <label><strong>ID parenta</strong><span>${label}</span><input type="text" data-model-builder-parent-id="${key}" placeholder="parent id"></label>
        ` : "";
        return `
          <label><strong>ID levela</strong><span>${label}</span><input type="text" data-model-builder-level-id="${key}" placeholder="level id"></label>
          ${parentInput}
        `;
      }).join("");
      return `
        <h4>Identyfikatory leveli</h4>
        <p class="helper">Dla pierwszego poziomu podaj ID levela. Dla poziomów niższych podaj ID parenta oraz ID levela.</p>
        <div class="model-builder-grid">${controls}</div>
      `;
    }
    function modelBuilderInputHtml(field) {
      const key = escapeHtml(field.key);
      const label = escapeHtml(field.label || field.key);
      const level = field._level_label ? `<span>${escapeHtml(field._level_label)}</span>` : "";
      const help = field.kind === "product_ref" ? `<span class="helper">${escapeHtml(t("modelBuilder.valueHelp"))}</span>` : "";
      if (field.kind === "single_choice" && (field.options || []).length) {
        const options = (field.options || []).map((option) => {
          const value = option.label || option.value || option.id || "";
          return `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`;
        }).join("");
        return `<label><strong>${label}</strong>${level}<select data-model-builder-input="${key}"><option value=""></option>${options}</select>${help}</label>`;
      }
      if (field.kind === "multi_choice" || field.kind === "product_ref" || field.kind === "text") {
        return `<label><strong>${label}</strong>${level}<textarea data-model-builder-input="${key}" placeholder="${escapeHtml(field.key)}"></textarea>${help}</label>`;
      }
      return `<label><strong>${label}</strong>${level}<input type="text" data-model-builder-input="${key}" placeholder="${escapeHtml(field.key)}">${help}</label>`;
    }
    function renderModelBuilderEditor(model) {
      if (elementWorkflowMode !== "modelBuilder") return "";
      const fields = modelBuilderFieldsFromHierarchy(model);
      if (!fields.length) {
        return `<div class="notice">Nie odczytano pól modelu do ręcznego budowania elementów.</div>`;
      }
      return `
        <h3>Tworzenie elementów budowlanych z modelu</h3>
        <p>Uzupełnij pola odczytane z modelu PIM. Każdy dodany obiekt zostanie potraktowany jako wiersz danych wejściowych do wygenerowania building_elements.json.</p>
        ${modelBuilderLevelControlsHtml(model)}
        <h4>Pola modelu</h4>
        <div class="model-builder-grid">${fields.map(modelBuilderInputHtml).join("")}</div>
        <button type="button" class="secondary" onclick="addModelBuilderRow()">${escapeHtml(t("modelBuilder.add"))}</button>
        <div id="modelBuilderRows">${renderModelBuilderRows(model)}</div>
      `;
    }
    function addModelBuilderRow() {
      const row = {};
      for (const input of document.querySelectorAll("[data-model-builder-level-id]")) {
        const key = input.dataset.modelBuilderLevelId;
        if (key && input.value.trim()) row[`__level_id__${key}`] = input.value.trim();
      }
      for (const input of document.querySelectorAll("[data-model-builder-parent-id]")) {
        const key = input.dataset.modelBuilderParentId;
        if (key && input.value.trim()) row[`__parent_id__${key}`] = input.value.trim();
      }
      for (const input of document.querySelectorAll("[data-model-builder-input]")) {
        const key = input.dataset.modelBuilderInput;
        if (key && input.value.trim()) row[key] = input.value.trim();
      }
      if (!Object.keys(row).length) {
        $("elementStatus").textContent = currentLang === "pl" ? "Uzupełnij przynajmniej jedno pole modelu." : "Fill at least one model field.";
        return;
      }
      modelBuilderRows.push(row);
      for (const input of document.querySelectorAll("[data-model-builder-input], [data-model-builder-level-id], [data-model-builder-parent-id]")) input.value = "";
      syncElementMappingState();
      renderModelBuilderRowsIntoDom();
    }
    function removeModelBuilderRow(index) {
      modelBuilderRows.splice(index, 1);
      syncElementMappingState();
      renderModelBuilderRowsIntoDom();
    }
    function renderModelBuilderRows(model) {
      const fields = modelBuilderFieldsFromHierarchy(model || lastElementAnalysis?.model);
      const fieldByKey = Object.fromEntries(fields.map((field) => [field.key, field]));
      if (!modelBuilderRows.length) {
        return `<div class="notice" style="margin-top:12px;">${escapeHtml(t("modelBuilder.empty"))}</div>`;
      }
      const rows = modelBuilderRows.map((row, index) => {
        const items = Object.entries(row).map(([key, value]) => {
          if (key.startsWith("__level_id__")) {
            return `<div><strong>ID levela</strong><br>${escapeHtml(key.replace("__level_id__", ""))}: ${escapeHtml(value)}</div>`;
          }
          if (key.startsWith("__parent_id__")) {
            return `<div><strong>ID parenta</strong><br>${escapeHtml(key.replace("__parent_id__", ""))}: ${escapeHtml(value)}</div>`;
          }
          const field = fieldByKey[key] || { label: key, key };
          return `<div><strong>${escapeHtml(field.label || key)}</strong><br>${escapeHtml(value)}</div>`;
        }).join("");
        return `
          <div class="model-builder-row">
            <div class="model-builder-row-head">
              <strong>${escapeHtml(t("modelBuilder.saved"))} ${index + 1}</strong>
              <button type="button" class="secondary" onclick="removeModelBuilderRow(${index})">${escapeHtml(t("modelBuilder.remove"))}</button>
            </div>
            <div class="model-builder-preview">${items}</div>
          </div>
        `;
      }).join("");
      return rows;
    }
    function renderModelBuilderRowsIntoDom() {
      const holder = $("modelBuilderRows");
      if (holder) holder.innerHTML = renderModelBuilderRows(lastElementAnalysis?.model);
      if ($("modelBuilderStatus")) {
        $("modelBuilderStatus").textContent = modelBuilderRows.length
          ? `${t("modelBuilder.saved")}: ${modelBuilderRows.length}`
          : "";
      }
      saveElementWorkspaceState();
    }
    function modelBuilderMappingProfile() {
      const fields = modelBuilderFieldsFromHierarchy(lastElementAnalysis?.model);
      const mapping = JSON.parse(JSON.stringify(currentElementMapping || {}));
      if (!mapping._product_identity) {
        mapping._product_identity = {
          model_id: activeElementProductRootModelId || "",
          field_key: selectedElementProductIdentityField || "",
        };
      }
      const rootKey = lastElementAnalysis?.model?.hierarchy?.key || `model.${lastElementAnalysis?.model?.root_model_id || "root"}`;
      if (!mapping._levels) mapping._levels = {};
      for (const level of modelBuilderLevelsFromHierarchy(lastElementAnalysis?.model)) {
        mapping._levels[level.key] = {
          table: "json",
          id_column: `__level_id__${level.key}`,
        };
        if (level.type === "relation") {
          mapping._levels[level.key].parent_id_column = `__parent_id__${level.key}`;
        }
      }
      if (!mapping._levels[rootKey]) mapping._levels[rootKey] = { table: "json", id_column: `__level_id__${rootKey}` };
      for (const field of fields) {
        mapping[field.key] = {
          level: field._level_key || rootKey,
          table: "json",
          column: field.key,
          cleanup: { trim: true },
        };
      }
      return mapping;
    }
    function modelBuilderSourceFile() {
      const content = JSON.stringify(modelBuilderRows || [], null, 2);
      return new File([content], "manual-building-elements.json", { type: "application/json" });
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
      function levelConfig(levelKey) {
        return currentElementMapping._levels?.[levelKey] || {};
      }
      function levelTable(levelKey) {
        return levelConfig(levelKey).table || "";
      }
      function nodeUnlocked(node) {
        if (node.type !== "relation") return true;
        const config = levelConfig(node.key);
        return Boolean(config.table && config.parent_id_column);
      }
      function elementSourceValues(tableName, columnName) {
        if (!tableName || !columnName) return [];
        const table = (lastElementAnalysis?.tables || []).find((item) => item.name === tableName);
        const values = [];
        const sourceValues = table?.column_values?.[columnName] || (table?.sample_rows || []).map((row) => row?.[columnName]);
        for (const raw of sourceValues) {
          if (raw === undefined || raw === null || raw === "") continue;
          for (const part of String(raw).split(/[;,]/).map((item) => item.trim()).filter(Boolean)) {
            if (!values.includes(part)) values.push(part);
          }
        }
        return values.slice(0, 500);
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
      function renderElementChoiceMap(field, tableName, columnName, choiceMap = {}, disabled = false) {
        if (!["single_choice", "multi_choice"].includes(field.kind)) return "";
        const disabledAttr = disabled ? " disabled" : "";
        const values = elementSourceValues(tableName, columnName);
        const rows = values.map((value) => `
          <tr>
            <td class="choice-map-value">${escapeHtml(value)}</td>
            <td><select data-element-choice-source="${escapeHtml(field.key)}" data-choice-value="${escapeHtml(value)}" onchange="syncElementChoiceMap('${escapeHtml(field.key)}')"${disabledAttr}>${elementOptionSelect(field, choiceMap[value] || "")}</select></td>
          </tr>
        `).join("");
        return `
          <div class="model-options" data-element-choice-container="${escapeHtml(field.key)}">
            <textarea hidden data-cleanup="${escapeHtml(field.key)}" data-cleanup-key="choiceMap">${escapeHtml(JSON.stringify(choiceMap || {}))}</textarea>
            <strong>Mapowanie opcji wyboru:</strong>
            ${columnName
              ? `<table class="choice-map-table"><thead><tr><th>Wartość z pliku klienta</th><th>Opcja PIM</th></tr></thead><tbody>${rows || `<tr><td colspan="2">Brak wartości w próbce danych.</td></tr>`}</tbody></table>`
              : `<div class="helper">Wybierz kolumnę, aby zmapować wartości klienta na opcje PIM.</div>`}
          </div>
        `;
      }
      function fieldHtml(field, nodeKey, enabled = true) {
        const existing = currentElementMapping[field.key] || {};
        const selectedTable = levelTable(nodeKey);
        const selectedColumn = existing.column || (selectedTable === firstTable ? suggestedByTarget[field.key] || "" : "");
        const cleanup = existing.cleanup || {};
        const disabledAttr = enabled ? "" : " disabled";
        const selectedIdentity = elementProductIdentityFields.find(item => item.key === selectedElementProductIdentityField);
        const selectedIdentityText = selectedIdentity ? `${selectedIdentity.label || selectedIdentity.key} (${selectedIdentity.key})` : (currentLang === "pl" ? "nie wybrano" : "not selected");
        const productReferenceNotice = field.kind === "product_ref" ? `
          <div class="notice">
            To pole identyfikuje produkt w warstwie. Najlepiej mapować stabilny kod lub ID produktu; nazwa jest dopasowaniem awaryjnym.
            Jeśli klient wpisuje kilka produktów w jednej komórce, rozdziel je przecinkiem, średnikiem, pionową kreską albo nową linią.
            Nazwa produktu oznacza wszystkie jego warianty; nazwa albo kod wariantu oznacza tylko wskazany wariant.
            Aktualny identyfikator z modelu produktu: ${escapeHtml(selectedIdentityText)}.
          </div>
        ` : "";
        return `
          <div class="model-map-row" data-element-field-row="${escapeHtml(field.key)}" data-element-field-level="${escapeHtml(nodeKey)}">
            <div class="model-map-label">
              <strong>${escapeHtml(field.label || field.key)}</strong>
              <span>${escapeHtml(field.key)}</span>
            </div>
            <div class="model-map-kind">${escapeHtml(field.kind || "")}${field.required ? " / wymagane" : ""}</div>
            ${productReferenceNotice}
            <div class="model-map-kind">Arkusz levelu: <strong>${escapeHtml(selectedTable || "nie wybrano")}</strong></div>
            <select data-element-column="${escapeHtml(field.key)}" onchange="refreshElementFieldState('${escapeHtml(field.key)}')"${disabledAttr}>
              ${columnOptions(selectedColumn, selectedTable)}
            </select>
            <details class="model-map-details">
              <summary>Szczegóły mapowania i czyszczenia</summary>
              <div class="model-cleanup">
                <label><input type="checkbox" data-cleanup="${escapeHtml(field.key)}" data-cleanup-key="trim" ${cleanup.trim === false ? "" : "checked"} onchange="syncElementMappingState()"${disabledAttr}> usuń spacje z początku i końca</label>
                <label><input type="checkbox" data-cleanup="${escapeHtml(field.key)}" data-cleanup-key="decimalComma" ${cleanup.decimalComma ? "checked" : ""} onchange="syncElementMappingState()"${disabledAttr}> przecinek -> kropka</label>
                <label><input type="checkbox" data-cleanup="${escapeHtml(field.key)}" data-cleanup-key="parseNumber" ${cleanup.parseNumber ? "checked" : ""} onchange="syncElementMappingState()"${disabledAttr}> tylko liczba</label>
                <label>usuń tekst<input data-cleanup="${escapeHtml(field.key)}" data-cleanup-key="removeText" value="${escapeHtml(cleanup.removeText || "")}" oninput="syncElementMappingState()"${disabledAttr}></label>
                <label>separator<input data-cleanup="${escapeHtml(field.key)}" data-cleanup-key="splitBy" value="${escapeHtml(cleanup.splitBy || "")}" oninput="syncElementMappingState()"${disabledAttr}></label>
                <label>część<input data-cleanup="${escapeHtml(field.key)}" data-cleanup-key="splitPart" type="number" min="1" value="${escapeHtml(cleanup.splitPart || "")}" oninput="syncElementMappingState()"${disabledAttr}></label>
                <label>przelicznik<input data-cleanup="${escapeHtml(field.key)}" data-cleanup-key="unitConversionFactor" value="${escapeHtml(cleanup.unitConversionFactor || "")}" oninput="syncElementMappingState()"${disabledAttr}></label>
                <label>jednostka docelowa<input data-cleanup="${escapeHtml(field.key)}" data-cleanup-key="targetUnit" value="${escapeHtml(cleanup.targetUnit || field.unit || "")}" oninput="syncElementMappingState()"${disabledAttr}></label>
                ${renderElementChoiceMap(field, selectedTable, selectedColumn, cleanup.choiceMap || {}, !enabled)}
              </div>
            </details>
          </div>
        `;
      }
      function levelConfigHtml(node) {
        const config = levelConfig(node.key);
        const selectedTable = config.table || "";
        const columns = columnsForElementTable(selectedTable);
        const unlocked = nodeUnlocked(node);
        const disabledAttr = unlocked ? "" : " disabled";
        const columnOptionsForLevel = (selected) => [
          `<option value="">-- wybierz kolumnę --</option>`,
          ...columns.map((column) => `<option value="${escapeHtml(column)}" ${column === selected ? "selected" : ""}>${escapeHtml(column)}</option>`)
        ].join("");
        const parentControls = node.type === "relation" ? `
          <label>ID parenta
            <select data-element-level="${escapeHtml(node.key)}" data-level-key="parent_id_column" onchange="refreshElementLevelState('${escapeHtml(node.key)}')">
              ${columnOptionsForLevel(config.parent_id_column || "")}
            </select>
          </label>
        ` : "";
        return `
          <div class="model-level-config">
            ${unlocked ? "" : `<div class="notice">Dla tego poziomu wybierz arkusz / tabelę oraz ID parenta. Dopiero wtedy można edytować pola tego poziomu.</div>`}
            <label>Arkusz / tabela dla tego levela
              <select data-element-level="${escapeHtml(node.key)}" data-level-key="table" onchange="refreshElementLevelState('${escapeHtml(node.key)}')">
                ${tableOptions(selectedTable)}
              </select>
            </label>
            <label>Kolumna ID tego levela
              <select data-element-level="${escapeHtml(node.key)}" data-level-key="id_column" onchange="syncElementMappingState()"${disabledAttr}>${columnOptionsForLevel(config.id_column || "")}</select>
            </label>
            ${parentControls}
          </div>
        `;
      }
      function nodeHtml(node) {
        const unlocked = nodeUnlocked(node);
        const fieldsHtml = (node.fields || []).map((field) => fieldHtml(field, node.key, unlocked)).join("");
        const childrenHtml = (node.children || []).map((child) => nodeHtml(child)).join("");
        const meta = node.type === "relation"
          ? `relacja, atrybut ${node.attribute_id}, model ${node.source_model_id} -> ${node.target_model_id}`
          : `model ${node.model_id}`;
        return `
          <div class="model-tree-node" data-element-tree-node="${escapeHtml(node.key)}">
            <div class="model-tree-header">
              <strong>${escapeHtml(node.label || "Model")}</strong>
              <span>${escapeHtml(meta)}</span>
            </div>
            ${levelConfigHtml(node)}
            ${fieldsHtml || `<div class="model-tree-empty">Brak pól bezpośrednio w tej gałęzi.</div>`}
            ${childrenHtml ? `<div class="model-tree-children">${childrenHtml}</div>` : ""}
          </div>
        `;
      }
      const fallbackNode = { key: "model.fallback", type: "model", model_id: payload.model?.root_model_id || "", label: payload.model?.root_model_name || "Model", fields, children: [] };
      const hierarchyHtml = nodeHtml(payload.model?.hierarchy || fallbackNode);
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
    function rerenderElementMapping() {
      if (!lastElementAnalysis) return;
      syncElementMappingState();
      renderElementAnalysis(lastElementAnalysis);
    }
    function refreshElementFieldState(target) {
      rerenderElementMapping();
    }
    function refreshElementLevelState(levelKey) {
      rerenderElementMapping();
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
    function collectElementLevels() {
      const levels = {};
      for (const input of document.querySelectorAll("[data-element-level]")) {
        const level = input.dataset.elementLevel;
        const key = input.dataset.levelKey;
        if (!level || !key) continue;
        if (!levels[level]) levels[level] = {};
        if (input.value) levels[level][key] = input.value;
      }
      return levels;
    }
    function collectElementMapping() {
      if (!document.querySelector("[data-element-field-row]") && Object.keys(currentElementMapping || {}).length) {
        return currentElementMapping;
      }
      const levels = collectElementLevels();
      const mapping = {
        _levels: levels,
        _product_identity: {
          model_id: activeElementProductRootModelId || "",
          field_key: selectedElementProductIdentityField || "",
        },
      };
      for (const columnSelect of document.querySelectorAll("[data-element-column]")) {
        const target = columnSelect.dataset.elementColumn;
        const row = columnSelect.closest("[data-element-field-row]");
        const levelKey = row?.dataset.elementFieldLevel || "";
        const table = levels[levelKey]?.table || "";
        if (!target || !table || !columnSelect.value) continue;
        mapping[target] = {
          level: levelKey,
          table,
          column: columnSelect.value,
          cleanup: cleanupForTarget(target),
        };
      }
      return mapping;
    }
    function syncElementMappingState(schedulePreview = true) {
      currentElementMapping = collectElementMapping();
      storeElementMappingForActiveModel();
      saveElementWorkspaceState();
      if (schedulePreview) scheduleElementLivePreview();
    }
    function renderElementAnalysis(payload) {
      lastElementAnalysis = payload;
      const tables = payload.tables || [];
      const fields = payload.model?.fields || [];
      const relations = payload.model?.relations || [];
      const rows = tables.reduce((sum, table) => sum + (table.rows || 0), 0);
      const reference = payload.product_reference || {};
      const tableItems = tables.map((table) => `<li>${escapeHtml(table.name)}: ${table.rows || 0} wierszy, ${(table.columns || []).length} kolumn</li>`).join("");
      const mainTitle = elementWorkflowMode === "modelBuilder" ? "Tworzenie elementów budowlanych" : "Analiza elementów budowlanych";
      const mainEditor = elementWorkflowMode === "modelBuilder"
        ? renderModelBuilderEditor(payload.model)
        : renderElementMappingEditor(payload);
      $("elementSummary").className = "panel";
      $("elementSummary").innerHTML = `
        <h3>${escapeHtml(mainTitle)}</h3>
        <div class="summary-grid">
          <div class="summary-card"><strong>${tables.length}</strong><span>tabele</span></div>
          <div class="summary-card"><strong>${rows}</strong><span>wiersze</span></div>
          <div class="summary-card"><strong>${fields.length}</strong><span>pola modelu PIM</span></div>
          <div class="summary-card"><strong>${relations.length}</strong><span>relacje zagnieżdżone</span></div>
          <div class="summary-card"><strong>${reference.products_count || 0}</strong><span>produkty referencyjne</span></div>
        </div>
        <p>${escapeHtml(reference.message || "")}</p>
        ${elementWorkflowMode === "modelBuilder" ? "" : `
          <h3>Wczytane tabele</h3>
          <ul class="tree-list">${tableItems || "<li>Nie znaleziono tabel w pliku importowanym.</li>"}</ul>
        `}
        ${mainEditor}
        ${renderElementLivePreview(lastElementPreview)}
      `;
      renderElementRootModelSelect();
      syncElementMappingState();
      scheduleElementLivePreview(0);
      saveElementWorkspaceState();
    }
    $("elementProjectName").addEventListener("input", saveElementWorkspaceState);
    $("elementWorkflowMode").addEventListener("change", updateElementWorkflowMode);
    $("elementRootModelSelect").addEventListener("change", (event) => changeElementRootModel(event.target.value));
    $("elementProductRootModelSelect").addEventListener("change", (event) => changeElementProductRootModel(event.target.value));
    $("elementProductIdentityFieldSelect").addEventListener("change", (event) => {
      selectedElementProductIdentityField = event.target.value;
      saveElementWorkspaceState();
    });
    $("elementProjectFile").addEventListener("change", () => {
      const file = $("elementProjectFile").files[0];
      if (file) loadElementProjectFromFile(file);
    });
    for (const inputId of ["elementModelsFile", "elementAttributesFile", "elementProductModelsFile", "elementProductAttributesFile", "productReferenceFile", "elementSourceFile"]) {
      $(inputId).addEventListener("change", async () => {
        if (inputId === "elementProductModelsFile" || inputId === "elementProductAttributesFile") {
          elementProductRootModels = [];
          activeElementProductRootModelId = "";
          elementProductIdentityFields = [];
          selectedElementProductIdentityField = "";
          renderElementProductIdentityControls();
        }
        await saveElementWorkspaceFilesState();
        saveElementWorkspaceState();
      });
    }
    async function initializeElementPage() {
      const preserveWorkspace = consumeWorkspaceNavigationMarker();
      if (isPageReload() && !preserveWorkspace) {
        await clearElementWorkspaceStorage();
      } else {
        await restoreElementWorkspaceState();
      }
      applyLanguage();
    }
    initializeElementPage();
  </script>
</body>
</html>"""


