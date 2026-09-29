from __future__ import annotations

from .building_elements_ui import render_building_elements_home
from .colors_ui import render_colors_home
from .products_ui import render_home
from .version import app_version_label

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
    .version-badge { display:inline-flex; align-items:center; min-height:28px; padding:5px 9px; border:1px solid var(--line); border-radius:6px; background:#f5f6f8; color:var(--muted); font-size:12px; font-weight:650; white-space:nowrap; }
  </style>
</head>
<body>
  <header>
    <h1>BuildData AI</h1>
    <div style="display:flex;align-items:center;gap:12px;">
      <span class="version-badge" title="BuildData AI version">__APP_VERSION_LABEL__</span>
      <select id="languageSelect" aria-label="Language">
        <option value="pl">Polski</option>
        <option value="en">English</option>
      </select>
    </div>
  </header>
  <main class="home-workspace">
    <div class="home-heading">
      <div><h2 data-i18n="workspace.title">Przestrzeń danych</h2><p data-i18n="workspace.subtitle">Projekty mapowania</p></div>
      <span class="home-label">EXCEL / CSV / JSON → PIM</span>
    </div>
    <div class="workspace-list">
      <a class="workspace-link" href="/products">
        <span class="workspace-symbol" aria-hidden="true">▦</span>
        <div>
        <strong data-i18n="products.title">Mapowanie Produktów</strong>
        <span data-i18n="products.text">Import pliku klienta, mapowanie cech produktu i typoszeregu, czyszczenie danych oraz generowanie products.json.</span>
        </div><small>products.json</small><span aria-hidden="true">→</span>
      </a>
      <a class="workspace-link" href="/building-elements">
        <span class="workspace-symbol" aria-hidden="true">▤</span>
        <div>
        <strong data-i18n="elements.title">Mapowanie Building Elementów</strong>
        <span data-i18n="elements.text">Mapowanie hierarchii systemów, wariantów, warstw i relacji odczytanej z modelu PIM elementów budowlanych.</span>
        </div><small>building_elements.json</small><span aria-hidden="true">→</span>
      </a>
      <a class="workspace-link" href="/colors">
        <span class="workspace-symbol" aria-hidden="true">◐</span>
        <div>
        <strong data-i18n="colors.title">Import Kolorów</strong>
        <span data-i18n="colors.text">Mapowanie kolorów prostych i tekstur. Bitmapy pozostają zewnętrznymi plikami, a eksport zapisuje tylko ich referencje.</span>
        </div><small>colors.json</small><span aria-hidden="true">→</span>
      </a>
    </div>
    <div class="home-footer"><span>BuildData AI</span><span data-i18n="workspace.footer">Modele · Dane źródłowe · Mapowanie · Eksport</span></div>
  </main>
  <script>
    const I18N = {
      pl: {
        "workspace.title": "Przestrzeń danych",
        "workspace.subtitle": "Projekty mapowania",
        "workspace.footer": "Modele · Dane źródłowe · Mapowanie · Eksport",
        intro: "Wybierz niezależną sekcję pracy. Projekty produktów, elementów budowlanych i kolorów są prowadzone osobno.",
        "products.title": "Produkty",
        "products.text": "Cechy produktów, typoszeregi i warianty",
        "elements.title": "Elementy budowlane",
        "elements.text": "Systemy, warianty, warstwy i produkty",
        "colors.title": "Kolory i tekstury",
        "colors.text": "Palety, grupy kolorów i materiały",
      },
      en: {
        "workspace.title": "Data workspace",
        "workspace.subtitle": "Mapping projects",
        "workspace.footer": "Models · Source data · Mapping · Export",
        intro: "Choose an independent workspace. Product, building-element, and color projects are handled separately.",
        "products.title": "Products",
        "products.text": "Product attributes, type series and variants",
        "elements.title": "Building elements",
        "elements.text": "Systems, variants, layers and products",
        "colors.title": "Colors and textures",
        "colors.text": "Palettes, color groups and materials",
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
</html>""".replace("__APP_VERSION_LABEL__", app_version_label())
