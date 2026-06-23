from __future__ import annotations

from .building_elements_ui import render_building_elements_home
from .colors_ui import render_colors_home
from .products_ui import render_home

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
    header { min-height:64px; display:flex; align-items:center; justify-content:space-between; gap:16px; padding:14px 24px; border-bottom:1px solid var(--line); background:var(--panel); }
    h1 { margin:0; font-size:22px; }
    select { width:auto; min-width:130px; padding:9px 10px; border:1px solid #cbd5e1; border-radius:4px; background:#fff; color:var(--text); font:inherit; }
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
    <select id="languageSelect" aria-label="Language">
      <option value="pl">Polski</option>
      <option value="en">English</option>
    </select>
  </header>
  <main>
    <p class="intro" data-i18n="intro">Wybierz niezależną sekcję pracy. Projekty produktów, elementów budowlanych i kolorów są prowadzone osobno.</p>
    <div class="choice-grid">
      <a class="choice" href="/products">
        <strong data-i18n="products.title">Mapowanie Produktów</strong>
        <span data-i18n="products.text">Import pliku klienta, mapowanie cech produktu i typoszeregu, czyszczenie danych oraz generowanie products.json.</span>
        <span class="badge">BuildData AI Products</span>
      </a>
      <a class="choice" href="/building-elements">
        <strong data-i18n="elements.title">Mapowanie Building Elementów</strong>
        <span data-i18n="elements.text">Mapowanie hierarchii systemów, wariantów, warstw i relacji odczytanej z modelu PIM elementów budowlanych.</span>
        <span class="badge">BuildData AI Building Elements</span>
      </a>
      <a class="choice" href="/colors">
        <strong data-i18n="colors.title">Import Kolorów</strong>
        <span data-i18n="colors.text">Mapowanie kolorów prostych i tekstur. Bitmapy pozostają zewnętrznymi plikami, a eksport zapisuje tylko ich referencje.</span>
        <span class="badge">BuildData AI Colors</span>
      </a>
    </div>
  </main>
  <script>
    const I18N = {
      pl: {
        intro: "Wybierz niezależną sekcję pracy. Projekty produktów, elementów budowlanych i kolorów są prowadzone osobno.",
        "products.title": "Mapowanie Produktów",
        "products.text": "Import pliku klienta, mapowanie cech produktu i typoszeregu, czyszczenie danych oraz generowanie products.json.",
        "elements.title": "Mapowanie Building Elementów",
        "elements.text": "Mapowanie hierarchii systemów, wariantów, warstw i relacji odczytanej z modelu PIM elementów budowlanych.",
        "colors.title": "Import Kolorów",
        "colors.text": "Mapowanie kolorów prostych i tekstur. Bitmapy pozostają zewnętrznymi plikami, a eksport zapisuje tylko ich referencje.",
      },
      en: {
        intro: "Choose an independent workspace. Product, building-element, and color projects are handled separately.",
        "products.title": "Product Mapping",
        "products.text": "Import a client file, map product and type-series attributes, clean data, and generate products.json.",
        "elements.title": "Building Element Mapping",
        "elements.text": "Map system, variant, layer, and nested relations from the PIM building-element model.",
        "colors.title": "Color Import",
        "colors.text": "Map simple colors and textures. Bitmap files remain external, and the export stores only their references.",
      }
    };
    let currentLang = localStorage.getItem("aiDataMasterLang") || "pl";
    const languageSelect = document.getElementById("languageSelect");
    function applyLanguage() {
      document.documentElement.lang = currentLang;
      languageSelect.value = currentLang;
      for (const element of document.querySelectorAll("[data-i18n]")) {
        element.textContent = I18N[currentLang]?.[element.dataset.i18n] || I18N.pl[element.dataset.i18n] || element.textContent;
      }
    }
    languageSelect.addEventListener("change", (event) => {
      currentLang = event.target.value;
      localStorage.setItem("aiDataMasterLang", currentLang);
      applyLanguage();
    });
    applyLanguage();
  </script>
</body>
</html>"""
