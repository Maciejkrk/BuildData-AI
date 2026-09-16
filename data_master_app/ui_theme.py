"""Shared presentation for the converter workspaces."""

WORKSPACE_THEME = r"""
<style id="builddata-theme">
:root { --bg:#f5f6f8; --panel:#fff; --soft:#fafbfc; --line:#e2e5e9; --text:#24282f; --muted:#68707d; --accent:#087f72; --accent-dark:#06685e; --secondary:#444c59; font-family:'Segoe UI',system-ui,sans-serif; }
* { box-sizing:border-box; letter-spacing:0; }
body { font-family:'Segoe UI',system-ui,sans-serif; font-size:14px; line-height:1.5; background:var(--bg); color:var(--text); }
body > header { padding:0 28px; min-height:72px; gap:24px; flex-wrap:wrap; background:#fff; }
header h1 { display:flex; align-items:center; gap:12px; font-size:18px; font-weight:650; white-space:nowrap; }
header h1::before { content:'B'; display:grid; place-items:center; flex:none; width:34px; height:34px; background:#24282f; color:#fff; border-radius:8px; font-size:21px; font-weight:750; }
.header-actions > [data-i18n='app.subtitle'] { display:none; }
.top-nav { gap:4px; flex-wrap:wrap; }
.top-nav a { border:0; border-radius:6px; padding:9px 12px; background:transparent; color:var(--muted); font-weight:600; }
.top-nav a:hover { background:#f4f5f7; color:var(--text); }
.top-nav a.active { background:#e9f5f1; color:#06685e; }
select.language-select, header > select { min-width:90px; width:auto; margin:0; border:0; background:#f5f6f8; font-size:12px; }
main { width:100%; max-width:1680px; margin:0 auto; padding:28px; gap:24px; }
h2,.title { font-size:16px; font-weight:650; }
h3 { font-size:14px; font-weight:650; }
main > aside { padding:0; gap:0; background:#fff; border:1px solid var(--line); border-radius:0; align-items:stretch; grid-template-columns:repeat(3,minmax(0,1fr)); }
main > aside > .panel { padding:22px; border:0; border-radius:0; background:transparent; margin:0; min-width:0; }
main > aside > .panel ~ .panel { border-left:1px solid var(--line); }
main > section, main > section.panel { border:0; border-top:1px solid var(--line); border-radius:0; background:#fff; margin:0; min-width:0; }
.panel .panel { border:0; border-top:1px solid var(--line); border-radius:0; box-shadow:none; }
label { font-size:12px; font-weight:600; color:#555d68; margin-top:14px; }
input[type=text], input[type=number], input[type=file], select, textarea { min-width:0; max-width:100%; border:1px solid #dce0e5; border-radius:6px; background:#fff; padding:9px 11px; font:inherit; font-size:13px; color:var(--text); }
input[type=file] { background:#fafbfc; padding:8px; font-size:12px; }
main > aside label > select { display:block; width:100%; margin-top:6px; }
input[type=file]::file-selector-button { border:1px solid #dce0e5; border-radius:4px; background:white; color:#444c59; padding:6px 9px; margin-right:9px; font:inherit; cursor:pointer; }
button { min-height:36px; border-radius:6px; padding:9px 14px; font-family:inherit; font-size:13px; font-weight:600; line-height:1.4; transition:background .15s,box-shadow .15s; overflow-wrap:anywhere; }
button:not(:disabled):hover { box-shadow:0 2px 5px #24282f14; filter:brightness(.96); }
button.secondary { border:1px solid #dce0e5; background:#fff; color:#444c59; }
button.secondary:not(:disabled):hover { background:#edf1f4; color:#24282f; }
button:disabled { opacity:1; color:#9299a3; background:#eef0f3; border-color:#e5e7eb; cursor:not-allowed; }
:is(button,a,input,select,textarea,summary):focus-visible { outline:3px solid #74c8bd; outline-offset:3px; }
.status { margin-top:10px; font-size:12px; overflow-wrap:anywhere; }
.gate-warning { font-size:12px; border:0; border-left:3px solid #dcad55; border-radius:0; background:#fffaf0; }
.toolbar { background:#fff; border-bottom:1px solid var(--line); padding:18px 22px; gap:12px; flex-wrap:wrap; }
.content { padding:22px; }
.file-status-list { overflow-wrap:anywhere; }
.file-status-item { border-radius:4px; }
table { font-size:13px; }
th { background:#f5f6f8; color:#555d68; font-size:12px; font-weight:600; }
td,th { padding:11px 12px; border-color:var(--line); }
tbody tr:hover { background:#f6faf9; }
.busy-overlay { backdrop-filter:blur(4px); background:rgba(36,40,47,.24); }
.busy-card { border:1px solid var(--line); border-radius:8px; background:#fff; box-shadow:0 16px 60px #24282f24; }
.setup-heading { grid-column:1/-1; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; padding:13px 22px; border-bottom:1px solid var(--line); }
.setup-heading strong { font-size:13px; font-weight:650; }
.setup-toggle { width:auto; margin:0; min-height:30px; padding:5px 10px; background:transparent; border:1px solid var(--line); color:var(--secondary); }
.setup-toggle:not(:disabled):hover { background:#f1f4f7; color:var(--text); }
aside.setup-collapsed > .panel { display:none; }
.setup-files { display:flex; flex-wrap:wrap; gap:8px; grid-column:1/-1; padding:10px 22px; border-top:1px solid var(--line); font-size:12px; color:var(--muted); }
.setup-files:empty { display:none; }
.setup-files .file-status-list { width:100%; margin:0; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); }
.setup-files .file-status { flex-direction:column; gap:3px; border:0; background:transparent; padding:2px 0; font-size:12px; }
.source-chip { max-width:100%; overflow-wrap:anywhere; padding:3px 8px; background:#f1f4f7; border-radius:4px; }
.workspace-intro { display:flex; align-items:center; justify-content:space-between; gap:16px; }
.workspace-intro h2 { margin:0; font-size:24px; }
.workspace-intro span { font-size:12px; color:var(--muted); }
#reportEmpty:not([hidden]) { min-height:170px; display:flex; align-items:center; justify-content:center; text-align:center; max-width:600px; margin:auto; font-size:14px; }
[data-i18n='model.help'],[data-i18n='products.help'],[data-i18n='project.help'],[data-i18n='elements.help'],[data-i18n='elements.notice'],.mode-banner { display:none; }
.home-workspace { max-width:1220px; padding-top:44px; display:block; }
.home-heading { display:flex; align-items:end; justify-content:space-between; gap:20px; margin-bottom:30px; }
.home-heading h2 { font-size:28px; margin:0; }
.home-heading p { margin:6px 0 0; font-size:14px; color:var(--muted); }
.home-label { font-size:12px; font-weight:600; color:var(--muted); }
.workspace-list { border-top:1px solid var(--line); background:white; }
.workspace-link { display:grid; grid-template-columns:56px minmax(0,1fr) minmax(150px,.6fr) 24px; gap:22px; align-items:center; padding:28px 24px; border-bottom:1px solid var(--line); text-decoration:none; color:var(--text); transition:background .15s; }
.workspace-link:hover { background:#f0f8f5; }
.workspace-link strong { display:block; font-size:18px; font-weight:650; margin-bottom:4px; }
.workspace-link small { color:var(--muted); font-size:13px; }
.workspace-link div > span { font-size:13px; color:var(--muted); }
.product-identity-settings { margin-top:16px; padding:10px 0; border-block:1px solid var(--line); }
.product-identity-settings summary { cursor:pointer; font-size:13px; font-weight:600; color:var(--secondary); }
.workspace-pane .mapping-card { border:0; border-top:1px solid var(--line); border-radius:0; margin-top:28px; }
.mapping-section-title { padding:18px 0; border-bottom:0; font-size:16px; font-weight:650; }
.product-type-layout { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:32px; padding:4px 0 24px; max-width:1200px; }
.product-type-layout fieldset { min-width:0; margin:0; border:0; padding:0 24px 0 0; }
.product-type-layout fieldset + fieldset { border-left:1px solid var(--line); padding:0 0 0 24px; }
.product-type-layout legend { padding:0; margin-bottom:18px; font-size:13px; font-weight:650; color:var(--accent-dark); }
.product-type-layout label, .rule-grid label { display:flex; flex-direction:column; align-items:stretch; min-width:0; gap:6px; font-size:12px; line-height:1.5; font-weight:500; }
.product-type-layout label { margin:0 0 16px; }
.product-type-layout :is(input,select), .rule-grid label > :is(input:not([type=hidden]),select,textarea) { display:block; width:100%; margin:0; min-height:40px; border-radius:6px; }
.product-type-layout input[type=number] { max-width:140px; }
.rule-grid { grid-template-columns:repeat(2,minmax(0,1fr)); gap:22px 28px; }
.rule-grid > .notice { grid-column:1/-1; }
.rule-grid .helper { margin:0; font-size:11px; color:var(--muted); }
.rule-menu-header { padding-bottom:20px; align-items:center; border-bottom:1px solid var(--line); }
.rule-menu-header .helper, .rule-menu-header .muted { display:none; }
.rule-menu-header h2 { margin:0; }
.panel.rule-menu { background:#fff; padding:24px 0; margin:0; border:0; }
.row-rule.panel { max-width:1000px; margin:0; padding:22px 0; border:0; background:transparent; }
.row-rule h2 { margin-bottom:20px; font-size:13px; color:var(--muted); }
.mapping-tools { padding:14px 0; margin:0; border-top:1px solid var(--line); gap:10px; }
.mapping-tools .rule-summary { margin-left:auto; }
.mapping-head,.mapping-row { grid-template-columns:minmax(150px,.65fr) minmax(240px,1.5fr) minmax(180px,1fr); gap:24px; padding:18px 16px; }
.mapping-head { background:#f4f6f8; border-block:1px solid var(--line); font-size:12px; font-weight:600; }
.mapping-row > * { min-width:0; }
.preview-box { border-radius:4px; box-shadow:none; }
.live-preview-panel { border:1px solid var(--line); border-top:3px solid var(--accent); box-shadow:none; border-radius:0; padding:20px; }
.readonly-value { border:1px solid var(--line); color:var(--text); font-size:13px; font-weight:500; }
.mapping-row.nested-owned-row { display:none; }
#nestedRelationsEditor { padding:24px; }
#nestedRelationsEditor > .mapping-section-title { padding:0 0 20px; margin:0; }
.nested-relation { border-top:1px solid var(--line); padding:24px 0; margin-top:24px; }
.nested-relation summary { cursor:pointer; font-weight:600; line-height:1.5; }
.nested-relation[open] > summary { margin-bottom:18px; }
.nested-relation > .inline-check { margin:0 0 20px; }
.nested-relation summary span { margin-left:12px; font-size:12px; }
.nested-relation summary .section-source-status { display:block; margin:8px 0 0 16px; font-weight:400; color:var(--muted); overflow-wrap:anywhere; }
.section-join-status { margin-top:24px; padding:14px 0; border-top:1px solid var(--line); line-height:1.6; font-size:13px; }
.nested-config-grid,.nested-field-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:24px; margin-top:20px; }
.nested-field-grid { border-top:1px solid var(--line); margin-top:28px; padding-top:24px; }
#nestedRelationsEditor label:not(.inline-check) { display:flex; flex-direction:column; gap:8px; margin:0; min-width:0; }
#nestedRelationsEditor label:not(.inline-check) > :is(input,select) { width:100%; min-width:0; margin:0; box-sizing:border-box; }
.nested-preview { margin-top:20px; border-top:1px solid var(--line); }
.nested-preview-heading { display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap; padding:16px 0; }
.nested-preview-heading h3 { margin:0; }
.nested-preview-heading button { width:auto; margin:0; }
.nested-table-scroll { overflow:auto; }
.nested-table-scroll td { min-width:110px; overflow-wrap:anywhere; }
@media(max-width:700px) { #nestedRelationsEditor { padding:16px; } .nested-config-grid,.nested-field-grid { grid-template-columns:minmax(0,1fr); } }
@media(max-width:900px) { .product-type-layout { grid-template-columns:1fr; gap:18px; } .product-type-layout fieldset, .product-type-layout fieldset + fieldset { padding:0; border:0; } .product-type-layout fieldset + fieldset { padding-top:18px; border-top:1px solid var(--line); } .mapping-row { grid-template-columns:1fr; gap:16px; } .mapping-head { display:none; } }
@media(max-width:600px) { .rule-grid { grid-template-columns:minmax(0,1fr); } .rule-menu-header { align-items:start; } .mapping-tools .rule-summary { width:100%; margin:0; } .content { padding:16px; } .content > #report > .panel { padding:0; border:0; } }
.workspace-symbol { display:grid; place-items:center; width:48px; height:48px; border-radius:8px; background:#e5f3ee; color:#087f72; font-size:24px; }
.workspace-link:nth-child(2) .workspace-symbol { background:#edf1fa; color:#526fbe; }
.workspace-link:nth-child(3) .workspace-symbol { background:#f8edf2; color:#ad5479; }
.home-footer { display:flex; gap:24px; margin-top:22px; color:var(--muted); font-size:12px; }
@media(min-width:1100px) { body > header { flex-wrap:nowrap; } .top-nav { margin-right:auto; } }
@media(max-width:1099px) { body > header { padding:16px 20px; } header h1 { font-size:16px; white-space:normal; } .top-nav { order:3; flex-basis:100%; } .header-actions { margin-left:auto; } main > aside { grid-template-columns:1fr; } main > aside > .panel { border-right:0; border-bottom:1px solid var(--line); } }
@media(max-width:600px) { main { padding:16px 12px; gap:16px; } body > header { padding:14px 12px; gap:12px; } .top-nav { gap:2px; } .top-nav a { padding:8px; font-size:12px; } .top-nav a[href='/'] { display:none; } main > aside > .panel { padding:16px; } .setup-heading { padding:12px 16px; } .workspace-intro h2 { font-size:21px; } .workspace-intro span { display:none; } .home-heading { align-items:start; flex-direction:column; gap:10px; } .home-heading h2 { font-size:24px; } .workspace-link { grid-template-columns:42px minmax(0,1fr) 16px; gap:14px; padding:22px 14px; } .workspace-symbol { width:40px; height:40px; } .workspace-link > small { display:none; } .workspace-link strong { font-size:16px; } .home-footer { flex-wrap:wrap; gap:8px 20px; } .grid { grid-template-columns:minmax(0,1fr); } }
@media(prefers-reduced-motion:reduce) { *,*::before,*::after { transition:none !important; } }
</style>
"""

WORKSPACE_SCRIPT = r"""
<script>
(() => {
  const brand = document.querySelector('body > header h1');
  if (brand) { brand.textContent = 'BuildData AI'; brand.setAttribute('aria-label', 'BuildData AI'); }
  const aside = document.querySelector('main > aside');
  if (!aside) return;
  const english = () => document.documentElement.lang === 'en';
  const intro = document.createElement('div');
  intro.className = 'workspace-intro';
  const title = document.createElement('h2');
  const format = document.createElement('span');
  format.textContent = 'Excel / CSV / JSON → PIM';
  intro.append(title, format);
  aside.before(intro);
  const bar = document.createElement('div');
  bar.className = 'setup-heading';
  const label = document.createElement('strong');
  const toggle = document.createElement('button');
  toggle.type = 'button';
  toggle.className = 'setup-toggle';
  toggle.setAttribute('aria-expanded', 'true');
  const panels = [...aside.children].filter(el => el.classList.contains('panel'));
  panels.forEach((panel, index) => { if (!panel.id) panel.id = `workspace-setup-${index}`; });
  toggle.setAttribute('aria-controls', panels.map(panel => panel.id).join(' '));
  bar.append(label, toggle);
  aside.prepend(bar);
  const files = document.createElement('div');
  files.className = 'setup-files';
  files.setAttribute('aria-live', 'polite');
  aside.append(files);
  const fileLists = [...aside.querySelectorAll('.file-status-list')];
  fileLists.forEach(list => files.append(list));
  const updateLanguage = () => {
    const isProducts = Boolean(document.getElementById('productModelPanel'));
    title.textContent = isProducts ? (english() ? 'Products' : 'Produkty') : (english() ? 'Building elements' : 'Elementy budowlane');
    label.textContent = english() ? 'Project settings' : 'Ustawienia projektu';
    const collapsed = aside.classList.contains('setup-collapsed');
    toggle.textContent = collapsed ? (english() ? 'Show settings ↓' : 'Rozwiń ustawienia ↓') : (english() ? 'Hide settings ↑' : 'Zwiń ustawienia ↑');
  };
  toggle.addEventListener('click', () => {
    const collapsed = aside.classList.toggle('setup-collapsed');
    toggle.setAttribute('aria-expanded', String(!collapsed));
    updateLanguage();
  });
  const updateFiles = () => {
    if (fileLists.length) return;
    const names = new Set();
    aside.querySelectorAll('input[type=file]').forEach(input => {
      for (const file of input.files || []) names.add(file.name);
    });
    files.replaceChildren(...[...names].map(name => {
      const chip = document.createElement('span');
      chip.className = 'source-chip';
      chip.textContent = name;
      return chip;
    }));
  };
  aside.addEventListener('change', updateFiles);
  document.getElementById('languageSelect')?.addEventListener('change', updateLanguage);
  updateLanguage();
  updateFiles();
})();
</script>
"""


def apply_workspace_theme(content: str) -> str:
    return content.replace('</head>', WORKSPACE_THEME + '</head>', 1).replace(
        '</body>', WORKSPACE_SCRIPT + '</body>', 1
    )
