from __future__ import annotations


def render_colors_home() -> str:
    return """<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>BuildData AI Colors</title>
  <style>
    :root { --bg:#f3f5f7; --panel:#fff; --line:#d8dde6; --text:#182230; --muted:#667085; --accent:#0f766e; --warn:#b45309; font-family:Arial,sans-serif; }
    * { box-sizing:border-box; }
    body { margin:0; background:var(--bg); color:var(--text); font-size:14px; }
    header { min-height:64px; display:flex; align-items:center; justify-content:space-between; gap:16px; padding:14px 24px; border-bottom:1px solid var(--line); background:var(--panel); }
    h1 { margin:0; font-size:22px; }
    h2 { margin:0 0 12px; font-size:18px; }
    h3 { margin:18px 0 10px; font-size:15px; }
    main { max-width:1180px; margin:0 auto; padding:22px 18px 40px; display:grid; gap:16px; }
    .top-nav { display:flex; flex-wrap:wrap; gap:8px; align-items:center; }
    .top-nav a { padding:8px 10px; border:1px solid var(--line); border-radius:4px; background:#fff; color:#344054; text-decoration:none; font-weight:700; font-size:13px; }
    .top-nav a.active { border-color:var(--accent); background:#f0fdfa; color:var(--accent); }
    .language-select { width:auto; min-width:130px; }
    section { background:var(--panel); border:1px solid var(--line); border-radius:6px; padding:16px; }
    .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:14px; }
    label { display:block; margin-top:12px; color:#344054; font-weight:700; font-size:12px; }
    input, select, button { margin-top:6px; width:100%; padding:9px 10px; border:1px solid #cbd5e1; border-radius:4px; background:#fff; color:var(--text); font:inherit; }
    button { width:auto; background:var(--accent); color:#fff; border-color:var(--accent); font-weight:700; cursor:pointer; }
    button.secondary { background:#fff; color:var(--accent); }
    button:disabled { opacity:.55; cursor:not-allowed; }
    .status, .muted { color:var(--muted); line-height:1.45; }
    .notice { border:1px solid #fed7aa; background:#fff7ed; color:var(--warn); border-radius:6px; padding:10px 12px; line-height:1.45; }
    .summary-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:10px; margin:12px 0; }
    .summary-card { border:1px solid var(--line); background:#f8fafc; border-radius:6px; padding:12px; }
    .summary-card strong { display:block; font-size:20px; }
    table { width:100%; border-collapse:collapse; margin-top:12px; }
    th, td { border-bottom:1px solid var(--line); padding:9px; text-align:left; vertical-align:top; }
    th { font-size:12px; color:#344054; background:#f8fafc; }
    .field-type { display:inline-block; padding:3px 7px; border-radius:999px; background:#eef2ff; color:#3730a3; font-size:12px; font-weight:700; }
    .file-field { background:#f0fdfa; color:#0f766e; }
    .choice-map { margin-top:16px; border:1px solid var(--line); border-radius:6px; padding:12px; background:#f8fafc; }
    .choice-map table { background:#fff; }
    .links { display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }
    .links a { color:var(--accent); font-weight:700; }
  </style>
</head>
<body>
  <header>
    <h1>BuildData AI Colors</h1>
    <nav class="top-nav">
      <a href="/">Menu główne</a>
      <a href="/products">Produkty</a>
      <a href="/building-elements">Elementy budowlane</a>
      <a class="active" href="/colors">Kolory</a>
    </nav>
    <select id="languageSelect" class="language-select" aria-label="Language">
      <option value="pl">Polski</option>
      <option value="en">English</option>
    </select>
  </header>
  <main>
    <section>
      <h2>Import kolorów</h2>
      <div class="notice" id="colorsNotice">Bitmapy nie są wczytywane do aplikacji. Pola tekstur i map są eksportowane jako zewnętrzne referencje: URL, ścieżka albo nazwa pliku.</div>
      <div class="grid">
        <label><span id="colorsFileLabel">Plik klienta z kolorami (.xlsx, .json, .csv, .tsv)</span>
          <input id="colorsFile" type="file" accept=".xlsx,.xlsm,.json,.csv,.tsv">
        </label>
        <label><span id="colorParametersLabel">colorParameters.json (opcjonalnie)</span>
          <input id="colorParametersFile" type="file" accept=".json">
        </label>
      </div>
      <div style="margin-top:14px; display:flex; gap:10px; flex-wrap:wrap;">
        <button type="button" id="analyzeColorsBtn">Analizuj plik</button>
        <button type="button" id="generateColorsBtn" class="secondary" disabled>Generuj colors.json</button>
      </div>
      <div id="colorsStatus" class="status">Wczytaj plik klienta z kolorami.</div>
      <div id="colorsLinks" class="links"></div>
    </section>
    <section id="colorsWorkspace">
      <h2>Mapowanie pól koloru</h2>
      <div id="colorsSummary" class="muted">Po analizie pojawią się pola z modelu kolorów i kolumny z pliku klienta.</div>
      <div id="colorsMapping"></div>
    </section>
  </main>
  <script>
    const $ = (id) => document.getElementById(id);
    let colorsAnalysis = null;
    let colorsMapping = {};
    let colorsChoiceMapping = {};
    let selectedTableName = "";
    let currentLang = localStorage.getItem("aiDataMasterLang") || "pl";
    let loadedColorFiles = { colorsFile: null, parametersFile: null };
    const COLORS_WORKSPACE_KEY = "buildDataAiColorsWorkspace";
    const COLORS_WORKSPACE_FILES_KEY = "colors-files";
    const WORKSPACE_NAVIGATION_KEY = "buildDataAiPreserveWorkspaceNavigation";
    const I18N = {
      pl: {
        initialStatus: "Wczytaj plik klienta z kolorami.",
        analyzeWait: "Proszę czekać, trwa analiza pliku kolorów.",
        analyzeReady: "Analiza gotowa. Sprawdź mapowanie pól koloru.",
        generateWait: "Generuję colors.json.",
        chooseFile: "Wybierz plik klienta z kolorami.",
        operationError: "Błąd operacji.",
        downloadError: "Nie udało się pobrać pliku.",
        saved: "Gotowe. Wygenerowano {count} kolorów. Zapisano: {file}",
        tables: "tabele",
        rows: "wiersze w aktywnej tabeli",
        fields: "pola koloru",
        files: "referencje bitmap",
        noMap: "-- nie mapuj --",
        skipOption: "-- pomiń / brak dopasowania --",
        noValues: "Brak wartości do mapowania w tej kolumnie.",
        chooseColumn: "Najpierw wybierz kolumnę źródłową dla tego pola.",
        choiceHelp: "Pole wyboru z modelu. Przypisz nazwy z pliku klienta do wartości dozwolonych w PIM.",
        clientValue: "Wartość z pliku klienta",
        modelOption: "Opcja z modelu",
        navMenu: "Menu główne",
        navProducts: "Produkty",
        navElements: "Elementy budowlane",
        navColors: "Kolory",
        title: "Import kolorów",
        mappingTitle: "Mapowanie pól koloru",
        notice: "Bitmapy nie są wczytywane do aplikacji. Pola tekstur i map są eksportowane jako zewnętrzne referencje: URL, ścieżka albo nazwa pliku.",
        colorsFileLabel: "Plik klienta z kolorami (.xlsx, .json, .csv, .tsv)",
        colorParametersLabel: "colorParameters.json (opcjonalnie)",
        tableLabel: "Arkusz / tabela",
        rowsSuffix: "wierszy",
        parameterHeader: "Parametr colors.json",
        typeHeader: "Typ",
        sourceColumnHeader: "Kolumna z pliku klienta",
        choiceTitleSuffix: "wartości klienta → opcje modelu",
        downloadColors: "Pobierz colors.json",
        downloadReport: "Pobierz raport mapowania",
        analyze: "Analizuj plik",
        generate: "Generuj colors.json",
        emptySummary: "Po analizie pojawią się pola z modelu kolorów i kolumny z pliku klienta.",
      },
      en: {
        initialStatus: "Load a client color file.",
        analyzeWait: "Please wait, color file analysis is running.",
        analyzeReady: "Analysis ready. Review color field mapping.",
        generateWait: "Generating colors.json.",
        chooseFile: "Choose a client color file.",
        operationError: "Operation error.",
        downloadError: "Could not download the file.",
        saved: "Done. Generated {count} colors. Saved: {file}",
        tables: "tables",
        rows: "rows in active table",
        fields: "color fields",
        files: "bitmap references",
        noMap: "-- do not map --",
        skipOption: "-- skip / no match --",
        noValues: "No values to map in this column.",
        chooseColumn: "Choose the source column for this field first.",
        choiceHelp: "Choice field from the model. Assign client-file names to values allowed in PIM.",
        clientValue: "Client-file value",
        modelOption: "Model option",
        navMenu: "Main menu",
        navProducts: "Products",
        navElements: "Building elements",
        navColors: "Colors",
        title: "Color import",
        mappingTitle: "Color field mapping",
        notice: "Bitmap files are not loaded into the app. Texture and map fields are exported as external references: URL, path, or file name.",
        colorsFileLabel: "Client color file (.xlsx, .json, .csv, .tsv)",
        colorParametersLabel: "colorParameters.json (optional)",
        tableLabel: "Sheet / table",
        rowsSuffix: "rows",
        parameterHeader: "colors.json parameter",
        typeHeader: "Type",
        sourceColumnHeader: "Client-file column",
        choiceTitleSuffix: "client values → model options",
        downloadColors: "Download colors.json",
        downloadReport: "Download mapping report",
        analyze: "Analyze file",
        generate: "Generate colors.json",
        emptySummary: "After analysis, color model fields and client-file columns will appear here.",
      }
    };

    function esc(value) {
      return String(value ?? "").replace(/[&<>"]/g, (char) => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;" }[char]));
    }
    function t(key) { return I18N[currentLang]?.[key] || I18N.pl[key] || key; }
    function applyLanguage() {
      document.documentElement.lang = currentLang;
      $("languageSelect").value = currentLang;
      const navLinks = document.querySelectorAll(".top-nav a");
      if (navLinks[0]) navLinks[0].textContent = t("navMenu");
      if (navLinks[1]) navLinks[1].textContent = t("navProducts");
      if (navLinks[2]) navLinks[2].textContent = t("navElements");
      if (navLinks[3]) navLinks[3].textContent = t("navColors");
      document.querySelector("main section h2").textContent = t("title");
      $("colorsWorkspace").querySelector("h2").textContent = t("mappingTitle");
      $("colorsNotice").textContent = t("notice");
      $("colorsFileLabel").textContent = t("colorsFileLabel");
      $("colorParametersLabel").textContent = t("colorParametersLabel");
      $("analyzeColorsBtn").textContent = t("analyze");
      $("generateColorsBtn").textContent = t("generate");
      if (!colorsAnalysis) $("colorsStatus").textContent = t("initialStatus");
      if (!colorsAnalysis) $("colorsSummary").textContent = t("emptySummary");
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
      for (let i = 0; i < binary.length; i += 1) bytes[i] = binary.charCodeAt(i);
      return new File([bytes], payload.name || "file", { type: mime, lastModified: payload.lastModified || Date.now() });
    }
    function openColorsWorkspaceDb() {
      return new Promise((resolve, reject) => {
        const request = indexedDB.open("BuildDataAIWorkspace", 1);
        request.onupgradeneeded = () => request.result.createObjectStore("items");
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
      });
    }
    async function setColorsWorkspaceItem(key, value) {
      const db = await openColorsWorkspaceDb();
      await new Promise((resolve, reject) => {
        const tx = db.transaction("items", "readwrite");
        tx.objectStore("items").put(value, key);
        tx.oncomplete = resolve;
        tx.onerror = () => reject(tx.error);
      });
      db.close();
    }
    async function getColorsWorkspaceItem(key) {
      const db = await openColorsWorkspaceDb();
      const value = await new Promise((resolve, reject) => {
        const tx = db.transaction("items", "readonly");
        const request = tx.objectStore("items").get(key);
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
      });
      db.close();
      return value;
    }
    async function deleteColorsWorkspaceItem(key) {
      const db = await openColorsWorkspaceDb();
      await new Promise((resolve, reject) => {
        const tx = db.transaction("items", "readwrite");
        tx.objectStore("items").delete(key);
        tx.oncomplete = resolve;
        tx.onerror = () => reject(tx.error);
      });
      db.close();
    }
    function normalize(value) {
      return String(value || "").toLowerCase()
        .normalize("NFD").replace(/[\\u0300-\\u036f]/g, "")
        .replace(/[^a-z0-9]+/g, "");
    }
    function fileOrError(id, message) {
      const fallback = id === "colorsFile" ? loadedColorFiles.colorsFile : loadedColorFiles.parametersFile;
      const file = $(id).files[0] || fallback;
      if (!file) throw new Error(message);
      return file;
    }
    function addOptionalFile(form, name, id) {
      const fallback = id === "colorParametersFile" ? loadedColorFiles.parametersFile : null;
      const file = $(id).files[0] || fallback;
      if (file) form.append(name, file);
    }
    async function saveColorsWorkspaceState() {
      try {
        sessionStorage.setItem(COLORS_WORKSPACE_KEY, JSON.stringify({
          analysis: colorsAnalysis,
          mapping: colorsMapping,
          choiceMapping: colorsChoiceMapping,
          selectedTableName,
          status: $("colorsStatus")?.textContent || "",
          links: $("colorsLinks")?.innerHTML || "",
          savedAt: new Date().toISOString(),
        }));
      } catch (error) {
        console.warn("Could not save colors workspace state", error);
      }
    }
    async function saveColorsWorkspaceFilesState() {
      try {
        const colorsFile = $("colorsFile")?.files?.[0] || loadedColorFiles.colorsFile || null;
        const parametersFile = $("colorParametersFile")?.files?.[0] || loadedColorFiles.parametersFile || null;
        await setColorsWorkspaceItem(COLORS_WORKSPACE_FILES_KEY, {
          colorsFile: colorsFile ? await projectFileFromFile(colorsFile) : null,
          parametersFile: parametersFile ? await projectFileFromFile(parametersFile) : null,
          savedAt: new Date().toISOString(),
        });
      } catch (error) {
        console.warn("Could not save colors files state", error);
      }
    }
    async function restoreColorsWorkspaceFilesState() {
      try {
        const payload = await getColorsWorkspaceItem(COLORS_WORKSPACE_FILES_KEY);
        if (!payload) return;
        loadedColorFiles = {
          colorsFile: fileFromProjectFile(payload.colorsFile),
          parametersFile: fileFromProjectFile(payload.parametersFile),
        };
      } catch (error) {
        console.warn("Could not restore colors files state", error);
      }
    }
    async function clearColorsWorkspaceStorage() {
      sessionStorage.removeItem(COLORS_WORKSPACE_KEY);
      try {
        await deleteColorsWorkspaceItem(COLORS_WORKSPACE_FILES_KEY);
      } catch (error) {
        console.warn("Could not clear colors files state", error);
      }
    }
    async function restoreColorsWorkspaceState() {
      try {
        await restoreColorsWorkspaceFilesState();
        const raw = sessionStorage.getItem(COLORS_WORKSPACE_KEY);
        if (!raw) return;
        const payload = JSON.parse(raw);
        colorsAnalysis = payload.analysis || null;
        colorsMapping = payload.mapping || {};
        colorsChoiceMapping = payload.choiceMapping || {};
        selectedTableName = payload.selectedTableName || "";
        if (payload.status) $("colorsStatus").textContent = payload.status;
        if (payload.links) $("colorsLinks").innerHTML = payload.links;
        if (colorsAnalysis) renderAnalysis();
      } catch (error) {
        console.warn("Could not restore colors workspace state", error);
      }
    }
    async function postForm(url, form) {
      const response = await fetch(url, { method:"POST", body:form });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || t("operationError"));
      return payload;
    }
    function tableColumns() {
      const table = (colorsAnalysis?.tables || []).find(item => item.name === selectedTableName) || colorsAnalysis?.tables?.[0];
      return table?.columns || [];
    }
    function activeColorTable() {
      return (colorsAnalysis?.tables || []).find(item => item.name === selectedTableName) || colorsAnalysis?.tables?.[0] || { columns:[], rows:0, column_values:{} };
    }
    function suggestColumn(field, columns) {
      const keys = [field.key, field.label, ...(field.options || []).flatMap(option => [option.name, option.value])].map(normalize).filter(Boolean);
      return columns.find(column => keys.includes(normalize(column)))
        || columns.find(column => keys.some(key => normalize(column).includes(key) || key.includes(normalize(column))))
        || "";
    }
    function isSelectField(field) {
      return normalize(field.type) === "select" || normalize(field.type) === "checkboxes";
    }
    function optionValue(option) {
      return String(option?.value ?? option?.name ?? "").trim();
    }
    function optionLabel(option) {
      const value = optionValue(option);
      const name = String(option?.name ?? value).trim();
      return value && name && value !== name ? `${name} (${value})` : (name || value);
    }
    function suggestChoice(field, sourceValue) {
      const sourceKey = normalize(sourceValue);
      const options = field.options || [];
      const exact = options.find(option => [option.name, option.value].some(item => normalize(item) === sourceKey));
      if (exact) return optionValue(exact);
      return "";
    }
    function renderChoiceMapping(field, activeTable) {
      if (!isSelectField(field) || !(field.options || []).length) return "";
      const column = colorsMapping[field.key] || "";
      const values = column ? (activeTable.column_values?.[column] || []) : [];
      const map = colorsChoiceMapping[field.key] || {};
      const optionItems = field.options || [];
      const rows = values.length
        ? values.map(value => {
            const selected = map[value] || map[normalize(value)] || suggestChoice(field, value);
            if (selected && !map[value]) map[value] = selected;
            return `<tr>
              <td>${esc(value)}</td>
              <td>
                <select data-color-choice-field="${esc(field.key)}" data-color-choice-value="${esc(value)}">
                  <option value="">${esc(t("skipOption"))}</option>
                  ${optionItems.map(option => `<option value="${esc(optionValue(option))}"${optionValue(option) === selected ? " selected" : ""}>${esc(optionLabel(option))}</option>`).join("")}
                </select>
              </td>
            </tr>`;
          }).join("")
        : `<tr><td colspan="2" class="muted">${column ? esc(t("noValues")) : esc(t("chooseColumn"))}</td></tr>`;
      colorsChoiceMapping[field.key] = map;
      return `<div class="choice-map" data-color-choice-map="${esc(field.key)}">
        <h3>${esc(field.label || field.key)}: ${esc(t("choiceTitleSuffix"))}</h3>
        <div class="muted">${esc(t("choiceHelp"))}</div>
        <table>
          <thead><tr><th>${esc(t("clientValue"))}</th><th>${esc(t("modelOption"))}</th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>`;
    }
    function renderAnalysis() {
      const tables = colorsAnalysis.tables || [];
      selectedTableName = selectedTableName || tables[0]?.name || "";
      const activeTable = activeColorTable();
      const columns = activeTable.columns || [];
      const fields = colorsAnalysis.fields || [];
      for (const field of fields) {
        if (!(field.key in colorsMapping)) colorsMapping[field.key] = suggestColumn(field, columns);
      }
      $("colorsSummary").innerHTML = `
        <div class="summary-grid">
          <div class="summary-card"><strong>${esc(tables.length)}</strong><span>${esc(t("tables"))}</span></div>
          <div class="summary-card"><strong>${esc(activeTable.rows || 0)}</strong><span>${esc(t("rows"))}</span></div>
          <div class="summary-card"><strong>${esc(fields.length)}</strong><span>${esc(t("fields"))}</span></div>
          <div class="summary-card"><strong>${esc(fields.filter(item => item.is_file).length)}</strong><span>${esc(t("files"))}</span></div>
        </div>
        <label>${esc(t("tableLabel"))}
          <select id="colorsTableSelect">${tables.map(table => `<option value="${esc(table.name)}"${table.name === selectedTableName ? " selected" : ""}>${esc(table.name)} (${esc(table.rows || 0)} ${esc(t("rowsSuffix"))})</option>`).join("")}</select>
        </label>`;
      $("colorsMapping").innerHTML = `
        <table>
          <thead><tr><th>${esc(t("parameterHeader"))}</th><th>${esc(t("typeHeader"))}</th><th>${esc(t("sourceColumnHeader"))}</th></tr></thead>
          <tbody>
            ${fields.map(field => `
              <tr>
                <td><strong>${esc(field.label || field.key)}</strong><div class="muted">${esc(field.key)}${field.unit ? ` [${esc(field.unit)}]` : ""}</div></td>
                <td><span class="field-type ${field.is_file ? "file-field" : ""}">${esc(field.type || "")}</span></td>
                <td>
                  <select data-color-field="${esc(field.key)}">
                    <option value="">${esc(t("noMap"))}</option>
                    ${columns.map(column => `<option value="${esc(column)}"${colorsMapping[field.key] === column ? " selected" : ""}>${esc(column)}</option>`).join("")}
                  </select>
                </td>
              </tr>`).join("")}
          </tbody>
        </table>
        ${fields.map(field => renderChoiceMapping(field, activeTable)).join("")}`;
      $("colorsTableSelect").addEventListener("change", (event) => {
        selectedTableName = event.target.value;
        colorsMapping = {};
        colorsChoiceMapping = {};
        renderAnalysis();
        saveColorsWorkspaceState();
      });
      for (const select of document.querySelectorAll("[data-color-field]")) {
        select.addEventListener("change", () => {
          colorsMapping[select.dataset.colorField] = select.value;
          if (colorsChoiceMapping[select.dataset.colorField]) colorsChoiceMapping[select.dataset.colorField] = {};
          renderAnalysis();
          saveColorsWorkspaceState();
        });
      }
      for (const select of document.querySelectorAll("[data-color-choice-field]")) {
        select.addEventListener("change", () => {
          const field = select.dataset.colorChoiceField;
          const value = select.dataset.colorChoiceValue;
          colorsChoiceMapping[field] = colorsChoiceMapping[field] || {};
          if (select.value) colorsChoiceMapping[field][value] = select.value;
          else delete colorsChoiceMapping[field][value];
          saveColorsWorkspaceState();
        });
      }
      $("generateColorsBtn").disabled = false;
      saveColorsWorkspaceState();
    }
    async function analyzeColors() {
      try {
        $("colorsStatus").textContent = t("analyzeWait");
        const form = new FormData();
        form.append("file", fileOrError("colorsFile", t("chooseFile")));
        addOptionalFile(form, "color_parameters", "colorParametersFile");
        await saveColorsWorkspaceFilesState();
        colorsAnalysis = await postForm("/api/colors/analyze", form);
        colorsMapping = {};
        colorsChoiceMapping = {};
        selectedTableName = "";
        renderAnalysis();
        $("colorsStatus").textContent = t("analyzeReady");
        saveColorsWorkspaceState();
      } catch (error) {
        $("colorsStatus").textContent = error.message;
      }
    }
    async function saveGeneratedFile(url, suggestedName) {
      const response = await fetch(url);
      if (!response.ok) throw new Error(t("downloadError"));
      const blob = await response.blob();
      if (window.showSaveFilePicker) {
        const handle = await window.showSaveFilePicker({
          suggestedName,
          types: [{ description:"JSON", accept:{ "application/json":[".json"] } }],
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
    async function generateColors() {
      try {
        $("colorsStatus").textContent = t("generateWait");
        const form = new FormData();
        form.append("file", fileOrError("colorsFile", t("chooseFile")));
        addOptionalFile(form, "color_parameters", "colorParametersFile");
        form.append("table_name", selectedTableName || "");
        form.append("color_mapping", JSON.stringify(colorsMapping));
        form.append("color_choice_mapping", JSON.stringify(colorsChoiceMapping));
        const result = await postForm("/api/colors/convert", form);
        $("colorsLinks").innerHTML = `<a href="${esc(result.files.colors_json)}" download="colors.json">${esc(t("downloadColors"))}</a> <a href="${esc(result.files.mapping_report_json)}" download="colors_mapping_report.json">${esc(t("downloadReport"))}</a>`;
        const saved = await saveGeneratedFile(result.files.colors_json, "colors.json");
        $("colorsStatus").innerHTML = `<span>${esc(t("saved").replace("{count}", result.colors_count).replace("{file}", saved))}</span>`;
        saveColorsWorkspaceState();
      } catch (error) {
        $("colorsStatus").textContent = error.message;
      }
    }
    $("languageSelect").addEventListener("change", (event) => {
      currentLang = event.target.value;
      localStorage.setItem("aiDataMasterLang", currentLang);
      applyLanguage();
      if (colorsAnalysis) renderAnalysis();
      saveColorsWorkspaceState();
    });
    for (const link of document.querySelectorAll(".top-nav a")) {
      link.addEventListener("click", async (event) => {
        const target = event.currentTarget;
        if (!target?.href) return;
        event.preventDefault();
        await saveColorsWorkspaceFilesState();
        await saveColorsWorkspaceState();
        markWorkspaceNavigation();
        window.location.href = target.href;
      });
    }
    for (const inputId of ["colorsFile", "colorParametersFile"]) {
      $(inputId).addEventListener("change", async () => {
        await saveColorsWorkspaceFilesState();
        await saveColorsWorkspaceState();
      });
    }
    window.addEventListener("pagehide", () => {
      saveColorsWorkspaceState();
    });
    async function initializeColorsPage() {
      const preserveWorkspace = consumeWorkspaceNavigationMarker();
      if (isPageReload() && !preserveWorkspace) {
        await clearColorsWorkspaceStorage();
      } else {
        await restoreColorsWorkspaceState();
      }
      applyLanguage();
    }
    $("analyzeColorsBtn").addEventListener("click", analyzeColors);
    $("generateColorsBtn").addEventListener("click", generateColors);
    initializeColorsPage();
  </script>
</body>
</html>"""
