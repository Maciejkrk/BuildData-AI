from __future__ import annotations


def render_studio() -> str:
    return """<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>BuildData AI Mapping Studio</title>
  <style>
    :root { color-scheme: light; font-family: Inter, Segoe UI, Arial, sans-serif; --ink:#17202a; --muted:#5d6a75; --line:#d8dee5; --soft:#f5f7fa; --accent:#0f766e; --warn:#a16207; }
    body { margin:0; color:var(--ink); background:#ffffff; }
    header { border-bottom:1px solid var(--line); padding:18px 28px; display:flex; align-items:center; justify-content:space-between; gap:20px; }
    h1 { margin:0; font-size:22px; font-weight:700; }
    main { display:grid; grid-template-columns: 280px 1fr; min-height:calc(100vh - 70px); }
    nav { border-right:1px solid var(--line); background:var(--soft); padding:18px; }
    .tab { width:100%; border:1px solid var(--line); background:#fff; padding:12px 14px; text-align:left; margin-bottom:10px; border-radius:6px; cursor:pointer; font-weight:650; }
    .tab.active { border-color:var(--accent); color:var(--accent); }
    section { padding:24px 30px; max-width:1120px; }
    h2 { margin:0 0 6px; font-size:20px; }
    p { color:var(--muted); margin:0 0 18px; line-height:1.45; }
    .grid { display:grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap:16px; }
    .panel { border:1px solid var(--line); border-radius:8px; padding:16px; background:#fff; }
    .panel h3 { margin:0 0 12px; font-size:15px; }
    label { display:block; font-size:13px; color:var(--muted); margin:10px 0 6px; }
    input[type=file], textarea { width:100%; box-sizing:border-box; border:1px solid var(--line); border-radius:6px; padding:9px; background:#fff; }
    textarea { min-height:92px; font-family: ui-monospace, Consolas, monospace; }
    button { border:0; border-radius:6px; padding:10px 14px; background:var(--accent); color:#fff; font-weight:700; cursor:pointer; margin-top:12px; }
    button.secondary { background:#1f2937; }
    button:disabled { background:#a7b1b8; cursor:not-allowed; }
    pre { overflow:auto; background:#101820; color:#e8eef2; border-radius:8px; padding:14px; max-height:420px; }
    .status { font-size:13px; color:var(--muted); margin-top:10px; }
    .locked { color:var(--warn); font-weight:650; }
    @media (max-width: 860px) { main { grid-template-columns:1fr; } nav { border-right:0; border-bottom:1px solid var(--line); } .grid { grid-template-columns:1fr; } }
  </style>
</head>
<body>
  <header>
    <h1>BuildData AI Mapping Studio</h1>
    <div class="status">Modele są wczytywane z eksportów PIM. Studio ich nie tworzy.</div>
  </header>
  <main>
    <nav>
      <button class="tab active" data-view="products">Produkty</button>
      <button class="tab" data-view="elements">Elementy budowlane</button>
      <p id="gate" class="locked">Elementy wymagają zakończonego mapowania produktów albo referencyjnego products.json.</p>
    </nav>
    <section id="products">
      <h2>Mapowanie produktów</h2>
      <p>Wczytaj istniejący model PIM produktu i plik klienta. Docelowe pola pochodzą wyłącznie z zaakceptowanego modelu.</p>
      <div class="grid">
        <div class="panel">
          <h3>Model i dane</h3>
          <label>productsModels.json + productsAttributes.json</label>
          <input id="productModelFiles" type="file" multiple accept=".json">
          <label>Plik klienta</label>
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
      <p>Wczytaj model elementów budowlanych, referencyjne products.json i dane klienta. Relacje wariantów, warstw i produktów są odczytywane z modelu.</p>
      <div class="grid">
        <div class="panel">
          <h3>Model, produkty, dane</h3>
          <label>buildingsElementsModels.json + buildingsElementsAttributes.json</label>
          <input id="elementModelFiles" type="file" multiple accept=".json">
          <label>Referencyjne products.json</label>
          <input id="productReferenceFile" type="file" accept=".json">
          <label>Plik elementów klienta</label>
          <input id="elementSourceFile" type="file" accept=".xlsx,.xlsm,.json,.csv,.tsv">
          <button onclick="analyzeElements()">Analizuj elementy</button>
          <label>Mapowanie JSON do podglądu</label>
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
    document.querySelectorAll('.tab').forEach(btn => btn.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach(item => item.classList.remove('active'));
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
      [...input.files].forEach(file => form.append(name, file));
    }
    async function analyzeProducts() {
      const form = new FormData();
      addFiles(form, 'model_files', document.getElementById('productModelFiles'));
      form.append('file', document.getElementById('productSourceFile').files[0]);
      try {
        const payload = await postForm('/api/products/analyze', form);
        productOutput.textContent = JSON.stringify(payload, null, 2);
        productStatus.textContent = 'Analiza gotowa.';
      } catch (error) { productStatus.textContent = error.message; }
    }
    async function analyzeElements() {
      const form = new FormData();
      addFiles(form, 'model_files', document.getElementById('elementModelFiles'));
      form.append('products_reference', document.getElementById('productReferenceFile').files[0]);
      form.append('file', document.getElementById('elementSourceFile').files[0]);
      try {
        const payload = await postForm('/api/building-elements/analyze', form);
        elementOutput.textContent = JSON.stringify(payload, null, 2);
        elementStatus.textContent = 'Analiza gotowa.';
      } catch (error) { elementStatus.textContent = error.message; }
    }
    async function previewElements() {
      const form = new FormData();
      form.append('products_reference', document.getElementById('productReferenceFile').files[0]);
      form.append('file', document.getElementById('elementSourceFile').files[0]);
      form.append('mapping_json', document.getElementById('elementMapping').value || '{}');
      try {
        const payload = await postForm('/api/building-elements/preview', form);
        elementOutput.textContent = JSON.stringify(payload, null, 2);
        elementStatus.textContent = 'Podgląd gotowy.';
      } catch (error) { elementStatus.textContent = error.message; }
    }
  </script>
</body>
</html>"""

