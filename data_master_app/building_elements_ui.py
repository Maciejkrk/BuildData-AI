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
        <p data-i18n="elements.help">Ten moduł służy do mapowania elementów budowlanych. Relacje do produktów wymagają referencyjnego pliku products.json z mapowania produktów.</p>
        <div class="notice" data-i18n="elements.notice">To jest ekran roboczy dla hierarchii elementów budowlanych: leveli, parentów, wariantów i pól modelu PIM.</div>
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
        <label><span data-i18n="elements.importFile">Plik importowany</span>
          <input id="elementSourceFile" type="file" accept=".xlsx,.xlsm,.json,.csv,.tsv">
        </label>
        <button type="button" onclick="analyzeElements()" data-i18n="elements.analyze">Analizuj elementy budowlane</button>
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
  <script>
    const I18N = {
      pl: {
        "nav.products": "Produkty",
        "nav.menu": "Wróć do menu głównego",
        "nav.buildingElements": "Elementy budowlane",
        "app.subtitle": "Mapowanie elementów budowlanych na podstawie modelu PIM",
        "elements.title": "Elementy budowlane",
        "elements.help": "Ten moduł służy do mapowania elementów budowlanych. Relacje do produktów wymagają referencyjnego pliku products.json z mapowania produktów.",
        "elements.notice": "To jest ekran roboczy dla hierarchii elementów budowlanych: leveli, parentów, wariantów i pól modelu PIM.",
        "elements.files": "Model, produkty i dane",
        "elements.modelsFile": "buildingElementsModels.json",
        "elements.attributesFile": "buildingElementsAttributes.json",
        "elements.loadModel": "Wczytaj hierarchię modelu",
        "elements.activeModel": "Edytowany model elementu",
        "elements.productsReference": "Referencyjne products.json (opcjonalne do analizy, wymagane do eksportu relacji)",
        "elements.importFile": "Plik importowany",
        "elements.analyze": "Analizuj elementy budowlane",
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
        "status.error": "Błąd żądania"
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
        "elements.modelsFile": "buildingElementsModels.json",
        "elements.attributesFile": "buildingElementsAttributes.json",
        "elements.loadModel": "Load model hierarchy",
        "elements.activeModel": "Edited element model",
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
    let elementRootModels = [];
    let activeElementRootModelId = "";
    let elementMappingsByModel = {};
    let loadedElementProject = null;
    let loadedElementProjectFiles = { modelFiles: [], sourceFile: null, productsReferenceFile: null };
    const ELEMENT_WORKSPACE_KEY = "buildDataAiBuildingElementsWorkspace";
    const ELEMENT_WORKSPACE_FILES_KEY = "building-elements-files";
    const $ = (id) => document.getElementById(id);
    function t(key) { return I18N[currentLang]?.[key] || I18N.pl[key] || key; }
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
          status: $("elementStatus")?.textContent || "",
          savedAt: new Date().toISOString(),
        };
        sessionStorage.setItem(ELEMENT_WORKSPACE_KEY, JSON.stringify(payload));
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
    async function saveElementWorkspaceFilesState() {
      try {
        const previous = await getElementWorkspaceItem(ELEMENT_WORKSPACE_FILES_KEY) || {};
        const modelFiles = selectedElementModelFiles();
        const sourceFile = $("elementSourceFile").files[0] || null;
        const productsReferenceFile = $("productReferenceFile").files[0] || null;
        const payload = {
          modelFiles: modelFiles.length
            ? await Promise.all(modelFiles.map(projectFileFromFile))
            : (loadedElementProjectFiles.modelFiles.length ? await Promise.all(loadedElementProjectFiles.modelFiles.map(projectFileFromFile)) : (previous.modelFiles || [])),
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
        const raw = sessionStorage.getItem(ELEMENT_WORKSPACE_KEY);
        if (!raw) return;
        const payload = JSON.parse(raw);
        currentElementMapping = payload.mapping || {};
        elementRootModels = payload.elementRootModels || elementRootModels;
        activeElementRootModelId = String(payload.activeElementRootModelId || activeElementRootModelId || "");
        elementMappingsByModel = payload.elementMappingsByModel || elementMappingsByModel;
        if (payload.projectName && $("elementProjectName")) $("elementProjectName").value = payload.projectName;
        if (payload.status && $("elementStatus")) $("elementStatus").textContent = payload.status;
        if (payload.analysis) renderElementAnalysis(payload.analysis);
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
      await saveElementWorkspaceFilesState();
      window.location.href = link.href;
    }
    for (const link of document.querySelectorAll(".top-nav a")) {
      link.addEventListener("click", persistElementWorkspaceBeforeNavigation);
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
    function elementModelFileFromCache(kind) {
      const pattern = kind === "models" ? /models[.]json$/i : /attributes[.]json$/i;
      return (loadedElementProjectFiles.modelFiles || []).find((file) => pattern.test(file?.name || "")) || null;
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
      storeElementMappingForActiveModel();
      const effectiveModelFiles = effectiveElementModelFiles();
      const sourceFile = $("elementSourceFile").files[0] || loadedElementProjectFiles.sourceFile;
      const productsReferenceFile = $("productReferenceFile").files[0] || loadedElementProjectFiles.productsReferenceFile;
      if (!effectiveModelFiles.length) throw new Error(t("project.missing"));
      return {
        name: $("elementProjectName").value || "mapowanie-elementow-budowlanych",
        model_version: "building-elements-mapping-project.v1",
        active_element_root_model_id: activeElementRootModelId || "",
        element_root_models: elementRootModels || [],
        element_mappings_by_model: elementMappingsByModel || {},
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
        elementRootModels = loadedElementProject.element_root_models || elementRootModels;
        activeElementRootModelId = String(loadedElementProject.active_element_root_model_id || activeElementRootModelId || "");
        elementMappingsByModel = loadedElementProject.element_mappings_by_model || elementMappingsByModel;
        currentElementMapping = loadedElementProject.building_element_mapping || {};
        if (activeElementRootModelId) elementMappingsByModel[activeElementRootModelId] = currentElementMapping;
        $("elementProjectName").value = loadedElementProject.name || "mapowanie-elementow-budowlanych";
        $("elementProjectStatus").textContent = `${t("project.loaded")} ${loadedElementProject.name || file.name}`;
        saveElementWorkspaceState();
        await saveElementWorkspaceFilesState();
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
        restoreElementMappingForActiveModel();
        renderElementRootModelSelect();
        renderElementAnalysis({
          model: payload.model,
          tables: [],
          product_reference: { products_count: 0, message: "Wczytano hierarchię modelu. Dodaj plik importowany, aby mapować kolumny." },
        });
        $("elementStatus").textContent = t("status.ready");
        saveElementWorkspaceState();
      } catch (error) {
        $("elementStatus").textContent = error.message;
        saveElementWorkspaceState();
      }
    }
    async function analyzeElements() {
      const form = new FormData();
      try {
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
        restoreElementMappingForActiveModel();
        renderElementRootModelSelect();
        renderElementAnalysis(payload);
        $("elementStatus").textContent = t("status.ready");
        saveElementWorkspaceState();
      } catch (error) {
        $("elementStatus").textContent = error.message;
        saveElementWorkspaceState();
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
      function levelConfig(levelKey) {
        return currentElementMapping._levels?.[levelKey] || {};
      }
      function levelTable(levelKey) {
        return levelConfig(levelKey).table || "";
      }
      function parentLevelKeyFor(node) {
        return node.parent_relation_key || (lastElementAnalysis?.model?.hierarchy?.key || `model.${lastElementAnalysis?.model?.root_model_id || "root"}`);
      }
      function levelNameMapped(levelKey) {
        const fieldKey = levelConfig(levelKey).level_name_field || "";
        return Boolean(fieldKey && currentElementMapping[fieldKey]?.column);
      }
      function nodeUnlocked(node) {
        return node.type !== "relation" || levelNameMapped(parentLevelKeyFor(node));
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
        return `
          <div class="model-map-row" data-element-field-row="${escapeHtml(field.key)}" data-element-field-level="${escapeHtml(nodeKey)}">
            <div class="model-map-label">
              <strong>${escapeHtml(field.label || field.key)}</strong>
              <span>${escapeHtml(field.key)}</span>
            </div>
            <div class="model-map-kind">${escapeHtml(field.kind || "")}${field.required ? " / wymagane" : ""}</div>
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
        const nameFieldOptions = [
          `<option value="">-- wybierz pole nazwy levela --</option>`,
          ...(node.fields || []).map((field) => `<option value="${escapeHtml(field.key)}" ${field.key === config.level_name_field ? "selected" : ""}>${escapeHtml(field.label || field.key)}</option>`)
        ].join("");
        const parentLevelKey = parentLevelKeyFor(node);
        const parentColumns = columnsForElementTable(levelTable(parentLevelKey));
        const parentColumnOptions = (selected) => [
          `<option value="">-- wybierz kolumnę --</option>`,
          ...parentColumns.map((column) => `<option value="${escapeHtml(column)}" ${column === selected ? "selected" : ""}>${escapeHtml(column)}</option>`)
        ].join("");
        const parentControls = node.type === "relation" ? `
          <label>Parent tego poziomu
            <select data-element-level="${escapeHtml(node.key)}" data-level-key="parent_level_key" onchange="syncElementMappingState()"${disabledAttr}>
              <option value="${escapeHtml(parentLevelKey)}">${escapeHtml(node.parent_relation_key ? "Poziom nadrzędny" : "Model główny")}</option>
            </select>
          </label>
          <label>Kolumna ID parenta w poziomie nadrzędnym
            <select data-element-level="${escapeHtml(node.key)}" data-level-key="parent_id_column" onchange="syncElementMappingState()"${disabledAttr}>${parentColumnOptions(config.parent_id_column || "")}</select>
          </label>
          <label>Kolumna wskazująca parenta w tym poziomie
            <select data-element-level="${escapeHtml(node.key)}" data-level-key="child_parent_id_column" onchange="syncElementMappingState()"${disabledAttr}>${columnOptionsForLevel(config.child_parent_id_column || "")}</select>
          </label>
        ` : "";
        return `
          <div class="model-level-config">
            ${unlocked ? "" : `<div class="notice">Najpierw zmapuj nazwę levela w poziomie nadrzędnym. Dopiero wtedy można parentować ten poziom.</div>`}
            <label>Arkusz / tabela dla tego levela
              <select data-element-level="${escapeHtml(node.key)}" data-level-key="table" onchange="refreshElementLevelState('${escapeHtml(node.key)}')"${disabledAttr}>
                ${tableOptions(selectedTable)}
              </select>
            </label>
            <label>Level name z mapowania
              <select data-element-level="${escapeHtml(node.key)}" data-level-key="level_name_field" onchange="refreshElementLevelState('${escapeHtml(node.key)}')"${disabledAttr}>
                ${nameFieldOptions}
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
      const levels = collectElementLevels();
      const mapping = { _levels: levels };
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
    function syncElementMappingState() {
      currentElementMapping = collectElementMapping();
      storeElementMappingForActiveModel();
      saveElementWorkspaceState();
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
        <h3>Analiza elementów budowlanych</h3>
        <div class="summary-grid">
          <div class="summary-card"><strong>${tables.length}</strong><span>tabele</span></div>
          <div class="summary-card"><strong>${rows}</strong><span>wiersze</span></div>
          <div class="summary-card"><strong>${fields.length}</strong><span>pola modelu PIM</span></div>
          <div class="summary-card"><strong>${relations.length}</strong><span>relacje zagnieżdżone</span></div>
          <div class="summary-card"><strong>${reference.products_count || 0}</strong><span>produkty referencyjne</span></div>
        </div>
        <p>${escapeHtml(reference.message || "")}</p>
        <h3>Wczytane tabele</h3>
        <ul class="tree-list">${tableItems || "<li>Nie znaleziono tabel w pliku importowanym.</li>"}</ul>
        ${mappingEditor}
      `;
      renderElementRootModelSelect();
      syncElementMappingState();
      saveElementWorkspaceState();
    }
    $("elementProjectName").addEventListener("input", saveElementWorkspaceState);
    $("elementRootModelSelect").addEventListener("change", (event) => changeElementRootModel(event.target.value));
    $("elementProjectFile").addEventListener("change", () => {
      const file = $("elementProjectFile").files[0];
      if (file) loadElementProjectFromFile(file);
    });
    for (const inputId of ["elementModelsFile", "elementAttributesFile", "productReferenceFile", "elementSourceFile"]) {
      $(inputId).addEventListener("change", async () => {
        await saveElementWorkspaceFilesState();
        saveElementWorkspaceState();
      });
    }
    restoreElementWorkspaceState();
    applyLanguage();
  </script>
</body>
</html>"""


