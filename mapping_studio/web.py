from __future__ import annotations


def render_studio() -> str:
    return """<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>BuildData AI</title>
  <style>
    :root {
      color-scheme: light;
      font-family: Inter, "Segoe UI", Arial, sans-serif;
      --ink:#17202a; --muted:#5d6a75; --line:#d8dee5; --soft:#f5f7fa;
      --accent:#0f766e; --dark:#1f2937; --warn:#a16207;
    }
    * { box-sizing:border-box; }
    body { margin:0; color:var(--ink); background:#fff; }
    header {
      border-bottom:1px solid var(--line); padding:18px 28px;
      display:flex; align-items:center; justify-content:space-between; gap:20px;
    }
    h1 { margin:0; font-size:22px; font-weight:700; }
    main { display:grid; grid-template-columns:280px 1fr; min-height:calc(100vh - 70px); }
    nav { border-right:1px solid var(--line); background:var(--soft); padding:18px; }
    section { padding:24px 30px; max-width:1180px; }
    h2 { margin:0 0 6px; font-size:20px; }
    h3 { margin:0 0 12px; font-size:15px; }
    p { color:var(--muted); margin:0 0 18px; line-height:1.45; }
    label { display:block; font-size:13px; color:var(--muted); margin:10px 0 6px; }
    input[type=file], textarea {
      width:100%; border:1px solid var(--line); border-radius:6px; padding:9px; background:#fff;
    }
    textarea { min-height:92px; font-family:ui-monospace, Consolas, monospace; }
    button {
      border:0; border-radius:6px; padding:10px 14px; background:var(--accent);
      color:#fff; font-weight:700; cursor:pointer; margin-top:12px;
    }
    button.secondary { background:var(--dark); }
    button:disabled { background:#a7b1b8; cursor:not-allowed; }
    pre { overflow:auto; background:#101820; color:#e8eef2; border-radius:8px; padding:14px; max-height:430px; }
    .tab {
      width:100%; border:1px solid var(--line); background:#fff; padding:12px 14px;
      text-align:left; margin-bottom:10px; border-radius:6px; cursor:pointer; font-weight:650; color:var(--ink);
    }
    .tab.active { border-color:var(--accent); color:var(--accent); background:#edfdfa; }
    .grid { display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:16px; }
    .panel { border:1px solid var(--line); border-radius:8px; padding:16px; background:#fff; }
    .status { font-size:13px; color:var(--muted); margin-top:10px; }
    .locked { color:var(--warn); font-weight:650; }
    @media (max-width:860px) {
      main { grid-template-columns:1fr; }
      nav { border-right:0; border-bottom:1px solid var(--line); }
      .grid { grid-template-columns:1fr; }
    }
  </style>
</head>
<body>
  <header>
    <h1>BuildData AI</h1>
    <div class="status">Modele są wczytywane z eksportów PIM. Studio ich nie tworzy.</div>
  </header>
  <main>
    <nav>
      <button class="tab active" data-view="products">Produkty</button>
      <button class="tab" data-view="elements">Elementy budowlane</button>
      <p class="locked">Mapowanie elementów budowlanych wymaga referencyjnego pliku products.json.</p>
    </nav>
    <section id="products">
      <h2>Mapowanie produktów</h2>
      <p>Wczytaj model produktu z PIM oraz plik importowany od klienta. Pola docelowe pochodzą wyłącznie z zaakceptowanego modelu.</p>
      <div class="grid">
        <div class="panel">
          <h3>Model i dane</h3>
          <label>productsModels.json + productsAttributes.json</label>
          <input id="productModelFiles" type="file" multiple accept=".json">
          <label>Plik importowany</label>
          <input id="productSourceFile" type="file" accept=".xlsx,.xlsm,.json,.csv,.tsv">
          <button onclick="analyzeProducts()">Analizuj produkty</button>
          <div id="productStatus" class="status"></div>
        </div>
        <div class="panel">
          <h3>Wynik analizy</h3>
          <pre id="productOutput">{}</pre>
        </div>
      </div>
    </section>
    <section id="elements" hidden>
      <h2>Mapowanie elementów budowlanych</h2>
      <p>Wczytaj model elementów budowlanych z PIM, referencyjny products.json i plik importowany. Relacje wariantów, warstw i produktów są odczytywane z modelu.</p>
      <div class="grid">
        <div class="panel">
          <h3>Model, produkty i dane</h3>
          <label>buildingElementsModels.json + buildingElementsAttributes.json</label>
          <input id="elementModelFiles" type="file" multiple accept=".json">
          <label>Referencyjne products.json</label>
          <input id="productReferenceFile" type="file" accept=".json">
          <label>Plik importowany</label>
          <input id="elementSourceFile" type="file" accept=".xlsx,.xlsm,.json,.csv,.tsv">
          <button onclick="analyzeElements()">Analizuj systemy</button>
          <label>Mapowanie JSON do podglądu drzewa</label>
          <textarea id="elementMapping">{}</textarea>
          <button class="secondary" onclick="previewElements()">Podgląd drzewa</button>
          <div id="elementStatus" class="status"></div>
        </div>
        <div class="panel">
          <h3>Wynik analizy</h3>
          <pre id="elementOutput">{}</pre>
        </div>
      </div>
    </section>
  </main>
  <script>
    document.querySelectorAll('.tab').forEach((btn) => btn.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach((item) => item.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById('products').hidden = btn.dataset.view !== 'products';
      document.getElementById('elements').hidden = btn.dataset.view !== 'elements';
    }));

    async function postForm(url, form) {
      const response = await fetch(url, { method: 'POST', body: form });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || 'Błąd żądania');
      return payload;
    }

    function addFiles(form, name, input) {
      [...input.files].forEach((file) => form.append(name, file));
    }

    function addRequiredFile(form, name, input, label) {
      const file = input.files[0];
      if (!file) throw new Error(`Brakuje pliku: ${label}`);
      form.append(name, file);
    }

    async function analyzeProducts() {
      const form = new FormData();
      try {
        addFiles(form, 'model_files', document.getElementById('productModelFiles'));
        addRequiredFile(form, 'file', document.getElementById('productSourceFile'), 'plik importowany');
        const payload = await postForm('/api/products/analyze', form);
        productOutput.textContent = JSON.stringify(payload, null, 2);
        productStatus.textContent = 'Analiza gotowa.';
      } catch (error) {
        productStatus.textContent = error.message;
      }
    }

    async function analyzeElements() {
      const form = new FormData();
      try {
        addFiles(form, 'model_files', document.getElementById('elementModelFiles'));
        addRequiredFile(form, 'products_reference', document.getElementById('productReferenceFile'), 'products.json');
        addRequiredFile(form, 'file', document.getElementById('elementSourceFile'), 'plik importowany');
        const payload = await postForm('/api/building-elements/analyze', form);
        elementOutput.textContent = JSON.stringify(payload, null, 2);
        elementStatus.textContent = 'Analiza gotowa.';
      } catch (error) {
        elementStatus.textContent = error.message;
      }
    }

    async function previewElements() {
      const form = new FormData();
      try {
        addRequiredFile(form, 'products_reference', document.getElementById('productReferenceFile'), 'products.json');
        addRequiredFile(form, 'file', document.getElementById('elementSourceFile'), 'plik importowany');
        form.append('mapping_json', document.getElementById('elementMapping').value || '{}');
        const payload = await postForm('/api/building-elements/preview', form);
        elementOutput.textContent = JSON.stringify(payload, null, 2);
        elementStatus.textContent = 'Podgląd gotowy.';
      } catch (error) {
        elementStatus.textContent = error.message;
      }
    }
  </script>
</body>
</html>"""
