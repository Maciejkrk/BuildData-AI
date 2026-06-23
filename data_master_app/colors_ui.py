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
  </header>
  <main>
    <section>
      <h2>Import kolorów</h2>
      <div class="notice">Bitmapy nie są wczytywane do aplikacji. Pola tekstur i map są eksportowane jako zewnętrzne referencje: URL, ścieżka albo nazwa pliku.</div>
      <div class="grid">
        <label>Plik klienta z kolorami (.xlsx, .json, .csv, .tsv)
          <input id="colorsFile" type="file" accept=".xlsx,.xlsm,.json,.csv,.tsv">
        </label>
        <label>colorParameters.json (opcjonalnie)
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

    function esc(value) {
      return String(value ?? "").replace(/[&<>"]/g, (char) => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;" }[char]));
    }
    function normalize(value) {
      return String(value || "").toLowerCase()
        .normalize("NFD").replace(/[\\u0300-\\u036f]/g, "")
        .replace(/[^a-z0-9]+/g, "");
    }
    function fileOrError(id, message) {
      const file = $(id).files[0];
      if (!file) throw new Error(message);
      return file;
    }
    function addOptionalFile(form, name, id) {
      const file = $(id).files[0];
      if (file) form.append(name, file);
    }
    async function postForm(url, form) {
      const response = await fetch(url, { method:"POST", body:form });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "Błąd operacji.");
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
                  <option value="">-- pomiń / brak dopasowania --</option>
                  ${optionItems.map(option => `<option value="${esc(optionValue(option))}"${optionValue(option) === selected ? " selected" : ""}>${esc(optionLabel(option))}</option>`).join("")}
                </select>
              </td>
            </tr>`;
          }).join("")
        : `<tr><td colspan="2" class="muted">${column ? "Brak wartości do mapowania w tej kolumnie." : "Najpierw wybierz kolumnę źródłową dla tego pola."}</td></tr>`;
      colorsChoiceMapping[field.key] = map;
      return `<div class="choice-map" data-color-choice-map="${esc(field.key)}">
        <h3>${esc(field.label || field.key)}: wartości klienta → opcje modelu</h3>
        <div class="muted">Pole wyboru z modelu. Przypisz nazwy z pliku klienta do wartości dozwolonych w PIM.</div>
        <table>
          <thead><tr><th>Wartość z pliku klienta</th><th>Opcja z modelu</th></tr></thead>
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
          <div class="summary-card"><strong>${esc(tables.length)}</strong><span>tabele</span></div>
          <div class="summary-card"><strong>${esc(activeTable.rows || 0)}</strong><span>wiersze w aktywnej tabeli</span></div>
          <div class="summary-card"><strong>${esc(fields.length)}</strong><span>pola koloru</span></div>
          <div class="summary-card"><strong>${esc(fields.filter(item => item.is_file).length)}</strong><span>referencje bitmap</span></div>
        </div>
        <label>Arkusz / tabela
          <select id="colorsTableSelect">${tables.map(table => `<option value="${esc(table.name)}"${table.name === selectedTableName ? " selected" : ""}>${esc(table.name)} (${esc(table.rows || 0)} wierszy)</option>`).join("")}</select>
        </label>`;
      $("colorsMapping").innerHTML = `
        <table>
          <thead><tr><th>Parametr colors.json</th><th>Typ</th><th>Kolumna z pliku klienta</th></tr></thead>
          <tbody>
            ${fields.map(field => `
              <tr>
                <td><strong>${esc(field.label || field.key)}</strong><div class="muted">${esc(field.key)}${field.unit ? ` [${esc(field.unit)}]` : ""}</div></td>
                <td><span class="field-type ${field.is_file ? "file-field" : ""}">${esc(field.type || "")}</span></td>
                <td>
                  <select data-color-field="${esc(field.key)}">
                    <option value="">-- nie mapuj --</option>
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
      });
      for (const select of document.querySelectorAll("[data-color-field]")) {
        select.addEventListener("change", () => {
          colorsMapping[select.dataset.colorField] = select.value;
          if (colorsChoiceMapping[select.dataset.colorField]) colorsChoiceMapping[select.dataset.colorField] = {};
          renderAnalysis();
        });
      }
      for (const select of document.querySelectorAll("[data-color-choice-field]")) {
        select.addEventListener("change", () => {
          const field = select.dataset.colorChoiceField;
          const value = select.dataset.colorChoiceValue;
          colorsChoiceMapping[field] = colorsChoiceMapping[field] || {};
          if (select.value) colorsChoiceMapping[field][value] = select.value;
          else delete colorsChoiceMapping[field][value];
        });
      }
      $("generateColorsBtn").disabled = false;
    }
    async function analyzeColors() {
      try {
        $("colorsStatus").textContent = "Proszę czekać, trwa analiza pliku kolorów.";
        const form = new FormData();
        form.append("file", fileOrError("colorsFile", "Wybierz plik klienta z kolorami."));
        addOptionalFile(form, "color_parameters", "colorParametersFile");
        colorsAnalysis = await postForm("/api/colors/analyze", form);
        colorsMapping = {};
        colorsChoiceMapping = {};
        selectedTableName = "";
        renderAnalysis();
        $("colorsStatus").textContent = "Analiza gotowa. Sprawdź mapowanie pól koloru.";
      } catch (error) {
        $("colorsStatus").textContent = error.message;
      }
    }
    async function saveGeneratedFile(url, suggestedName) {
      const response = await fetch(url);
      if (!response.ok) throw new Error("Nie udało się pobrać pliku.");
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
        $("colorsStatus").textContent = "Generuję colors.json.";
        const form = new FormData();
        form.append("file", fileOrError("colorsFile", "Wybierz plik klienta z kolorami."));
        addOptionalFile(form, "color_parameters", "colorParametersFile");
        form.append("table_name", selectedTableName || "");
        form.append("color_mapping", JSON.stringify(colorsMapping));
        form.append("color_choice_mapping", JSON.stringify(colorsChoiceMapping));
        const result = await postForm("/api/colors/convert", form);
        $("colorsLinks").innerHTML = `<a href="${esc(result.files.colors_json)}" download="colors.json">Pobierz colors.json</a> <a href="${esc(result.files.mapping_report_json)}" download="colors_mapping_report.json">Pobierz raport mapowania</a>`;
        const saved = await saveGeneratedFile(result.files.colors_json, "colors.json");
        $("colorsStatus").innerHTML = `<span>Gotowe. Wygenerowano ${esc(result.colors_count)} kolorów. Zapisano: ${esc(saved)}</span>`;
      } catch (error) {
        $("colorsStatus").textContent = error.message;
      }
    }
    $("analyzeColorsBtn").addEventListener("click", analyzeColors);
    $("generateColorsBtn").addEventListener("click", generateColors);
  </script>
</body>
</html>"""
