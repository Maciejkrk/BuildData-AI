const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync(0, 'utf8').replace(/\r\n/g, '\n');
const start = html.indexOf("document.addEventListener('change', async event => {\n      const editor");
const end = html.indexOf('    function renderProductTypeRule', start);
assert.ok(start >= 0 && end > start);
let handler, refreshed = false, collected = false, busy = false;
const status = {textContent: ''};
const group = {dataset: {nestedParent: '5101'}, querySelector: () => status};
const editor = {
  querySelectorAll: () => [{dataset: {nestedParent: '5101'}}],
  set outerHTML(value) { assert.equal(value, 'new editor'); refreshed = true; }
};
const event = {target: {
  files: [{webkitRelativePath: 'Root/P1/Karty/a.pdf'}],
  matches: selector => selector.split(',').map(s => s.trim()).includes('[data-nested-directory]'),
  closest: selector => selector === '#nestedRelationsEditor' ? editor : group
}};
const table = {name: 'Dokumenty zewnetrzne', columns: ['Katalog 1', 'Katalog 2', 'Sciezka pliku'],
  sample_rows: [{'Katalog 1': 'P1', 'Katalog 2': 'Karty', 'Sciezka pliku': 'P1/Karty/a.pdf'}]};
const context = {
  document: {addEventListener: (_, fn) => { handler = fn; }, querySelectorAll: () => []},
  collectNestedRelations: () => ({'5101': {source_mode: 'external', table: '', fields: {}}}),
  currentLang: 'pl', productMappingProfile: {}, activeMode: 'products', activeTable: {name: 'Products'},
  setBusy: () => { busy = true; }, clearBusy: () => { busy = false; },
  fetch: async (url, options) => {
    assert.equal(url, '/document-source');
    assert.deepEqual(JSON.parse(options.body), {paths: ['P1/Karty/a.pdf']});
    return {ok: true, json: async () => ({table})};
  },
  renderNestedRelations: () => {
    assert.equal(context.productMappingProfile._nested_relations['5101'].table, table.name);
    return 'new editor';
  },
  collectMapping: () => {
    assert.ok(refreshed, 'Directory fields must rerender before collecting the mapping');
    assert.equal(context.productMappingProfile._nested_relations['5101'].source.tables[0].sample_rows[0]['Katalog 1'], 'P1');
    collected = true;
  },
  sectionJoinStatus: () => '',
};
// Restoring a project can temporarily show only part of the model editor.
const savedRelation = {enabled: true, source_mode: 'external', use_primary_key: false,
  product_key: 'Name', child_key: 'Katalog 1', record_key: 'Sciezka pliku', table: table.name,
  source: {kind: 'documents', filename: 'Root', tables: [table]},
  fields: {'5102': 'Nazwa pliku', '5103': ''}, choice_maps: {'5105': {'Karty': '17'}}};
const savedProfile = {_nested_relations: {'5101': savedRelation, 'other-model': {enabled: false}}};
const controls = {
  '[data-nested-source-mode]': {value: 'documents'},
  '[data-document-join]': {value: '["Name","Katalog 1"]'},
};
const savedGroup = {dataset: {nestedParent: '5101'}, querySelector: s => controls[s], querySelectorAll: () => []};
const persistence = {
  productMappingProfile: JSON.parse(JSON.stringify(savedProfile)), loadedProject: null,
  document: {getElementById: () => ({querySelectorAll: () => [savedGroup]}), querySelector: () => null},
};
const collectStart = html.indexOf('    function collectNestedRelations()');
const collectEnd = html.indexOf('    function renderNestedRelations(', collectStart);
vm.runInNewContext(html.slice(collectStart, collectEnd), persistence);
assert.deepEqual(JSON.parse(JSON.stringify(persistence.collectNestedRelations())), savedProfile._nested_relations);
delete controls['[data-nested-source-mode]'];
assert.deepEqual(JSON.parse(JSON.stringify(persistence.collectNestedRelations())), savedProfile._nested_relations);
const candidateStart = html.indexOf('    function documentJoinCandidates(');
const candidateEnd = html.indexOf('    function documentChoiceEditor(', candidateStart);
vm.runInNewContext(html.slice(candidateStart, candidateEnd), context);
const candidates = context.documentJoinCandidates(table, {columns: ['Name', 'Other'], sample_rows: [{Name: 'P1', Other: 'unrelated'}]});
assert.equal(candidates.length, 1);
assert.equal(candidates[0].product_key, 'Name');
assert.equal(candidates[0].child_key, 'Katalog 1');
assert.equal(context.documentJoinCandidates(table, {columns: ['Name'], sample_rows: [{Name: 'P1'}, {Name: 'P1'}]}).length, 0);
vm.runInNewContext(html.slice(start, end), context);
handler(event).then(async () => {
  assert.ok(refreshed && collected);
  assert.equal(busy, false);
  assert.equal(status.textContent, '');
  const exportContext = {
    productMappingProfile: savedProfile, productMapping: {}, productMappingsByModel: {}, productMappingProfilesByModel: {},
    activeMode: 'products', activeTable: null, activeProductRootModelId: '5010', productRootModels: [],
    supplementMapping: null, supplementMappingProfile: null, supplementProductsUrl: '', enrichmentSession: {},
    loadedProjectFiles: {}, fileForInput: () => null, productModelFilesForProject: async () => [],
    storeProductMappingForActiveModel: () => {}, buildConnectionRegistry: () => ({}),
    $: () => ({value: 'directory-regression'}),
  };
  const payloadStart = html.indexOf('    async function projectPayload()');
  const payloadEnd = html.indexOf('    async function saveProject()', payloadStart);
  vm.runInNewContext(html.slice(payloadStart, payloadEnd), exportContext);
  const reopenedProject = JSON.parse(JSON.stringify(await exportContext.projectPayload()));
  assert.deepEqual(reopenedProject.product_mapping_profile._nested_relations, savedProfile._nested_relations);
}).catch(error => { console.error(error); process.exitCode = 1; });
