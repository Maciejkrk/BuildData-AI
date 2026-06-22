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
    <p class="intro">Wybierz niezależną sekcję pracy. Projekty produktów, elementów budowlanych i kolorów są prowadzone osobno.</p>
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
      <a class="choice" href="/colors">
        <strong>Import Kolorów</strong>
        <span>Mapowanie kolorów prostych i tekstur. Bitmapy pozostają zewnętrznymi plikami, a eksport zapisuje tylko ich referencje.</span>
        <span class="badge">BuildData AI Colors</span>
      </a>
    </div>
  </main>
</body>
</html>"""
