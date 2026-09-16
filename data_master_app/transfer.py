"""Build a portable transfer ZIP without connecting to PIM or Azure."""
import argparse
import json
from pathlib import Path
from .pim_bundle import DATA_FILES, build_bundle, build_transfer_folder, read_bundle, safe_path


def main():
    parser = argparse.ArgumentParser(description='Prepare a PIM transfer package offline')
    parser.add_argument('--data', required=True, type=Path)
    parser.add_argument('--files', required=True, type=Path)
    parser.add_argument('--links', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--folder-output', type=Path)
    args = parser.parse_args()
    if bool(args.output) == bool(args.folder_output):
        parser.error('Choose exactly one of --output ZIP or --folder-output directory')
    if args.output and args.output.exists():
        parser.error('Output already exists; choose a new filename')
    links = None
    if args.links:
        links = json.loads(args.links.read_text(encoding='utf-8-sig'))
        if isinstance(links, dict):
            if links.get('format') != 'pim-folder-plan.v1' or links.get('unresolved') != 0:
                raise ValueError('Resolve all folder mapping problems before export')
            links = links['links']
    root = args.files.resolve()
    files = {name: (args.data / name).read_bytes() for name in DATA_FILES if (args.data / name).is_file()}
    if args.folder_output:
        info = build_transfer_folder(files, root, args.folder_output, links=links)
        print(f"Transfer folder created: {args.folder_output} ({info['assets']} files)")
        return
    if links is None:
        raise ValueError('ZIP export requires --links. Use --folder-output to read sourcePath from products.json.')
    attachments = {}
    for link in links:
        relative = safe_path(link['file'])
        path = (root / relative).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError('Attachment must be a file within the selected root')
        attachments[relative] = path.read_bytes()
    content = build_bundle(files, attachments, links)
    read_bundle(content)
    with args.output.open('xb') as stream:
        stream.write(content)
    print(f'Package created: {args.output}')


if __name__ == '__main__':
    main()


TRANSFER_HTML = '''<!doctype html><html lang="pl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Paczka importu PIM</title>
<style>body{font:14px system-ui;margin:0;color:#202a30;background:#f4f6f7}header{padding:24px;background:white;border-bottom:1px solid #d6dce0}main{max-width:980px;margin:auto;padding:32px 24px}h1{font-size:24px}section{background:white;border:1px solid #d6dce0;border-radius:8px;padding:20px;margin:18px 0}label{display:block;margin:18px 0 8px}input{display:block;width:100%;box-sizing:border-box;padding:14px;background:white;border:1px solid #c9d1d6;border-radius:6px}button{padding:12px 20px;background:#087f72;color:white;border:0;border-radius:6px;margin-top:18px;cursor:pointer}.muted{color:#5c6b75}.secondary{background:#415160}a{color:#096da0}.status{margin-top:18px;line-height:1.6;white-space:pre-wrap}button:disabled{opacity:.5}#busy{position:fixed;inset:0;background:#ffffffeb;place-items:center;font-size:20px;display:grid}#busy[hidden]{display:none}</style></head>
<body><header><a href="/products">Produkty</a> / <a href="/building-elements">Elementy budowlane</a></header><main>
<h1>Paczka importu PIM</h1><p><a href="/transfer/folders">Mapowanie katalogów produktów i elementów budowlanych</a></p>
<section><h2>Duży eksport do folderu transferowego</h2><p class="muted">Użyj tego dla tysięcy plików i wielu GB. Mapper weźmie lokalne sourcePath z products.json, doklei je do katalogu bazowego plików i utworzy folder z data, assets, file-links.json oraz manifest.json.</p><form id="folderForm">
<label for="dataPath">Katalog z JSON-ami eksportu</label><input id="dataPath" name="data_path" placeholder="np. D:\\Projekty\\Fast_Dane\\Nowy_Model_Danych\\Nowy folder" required>
<label for="filesPath">Katalog bazowy plików</label><input id="filesPath" name="files_path" placeholder="np. D:\\Projekty\\Fast_Dane\\Dokumenty" required>
<label for="outputPath">Katalog wynikowy transferu</label><input id="outputPath" name="output_path" placeholder="np. C:\\Users\\Admin\\Documents\\PIM-Data-Importer\\pim-data-importer-app\\transfer" required>
<button type="submit">Utwórz folder transferowy</button></form><div id="folderStatus" class="status" role="status"></div></section>
<section><h2>Mała paczka ZIP</h2><p class="muted">Dla małych zestawów testowych. Dużych eksportów nie wysyłaj przez przeglądarkę.</p><form id="packageForm">
<label for="data">Wyeksportowane dane i modele PIM (JSON)</label><input id="data" name="data_files" type="file" accept=".json" multiple required>
<label for="links">Powiązania załączników (JSON)</label><input id="links" name="links_file" type="file" accept=".json" required>
<label for="assets">Załączniki</label><input id="assets" name="attachments" type="file" accept=".pdf,.jpg,.jpeg,.png,.gif,.bmp,.tiff" multiple>
<button type="submit" class="secondary">Przygotuj paczkę ZIP</button></form><div id="status" class="status" role="status"></div></section>
<p><a href="/transfer/example">Przykład powiązań załączników</a></p></main><div id="busy" hidden>Przygotowywanie i sprawdzanie paczki...</div>
<script>
async function submitForm(form,status,url,done){const busy=document.getElementById('busy'),button=form.querySelector('button');status.textContent='';busy.hidden=false;button.disabled=true;try{const response=await fetch(url,{method:'POST',body:new FormData(form)});if(!response.ok){const error=await response.json();throw new Error(error.detail||'Błąd paczki');}await done(response,status);}catch(error){status.textContent=error.message;}finally{busy.hidden=true;button.disabled=false;}}
document.getElementById('folderForm').addEventListener('submit',event=>{event.preventDefault();submitForm(event.currentTarget,document.getElementById('folderStatus'),'/transfer/folder-package',async(response,status)=>{const data=await response.json();status.textContent=`Utworzono folder transferowy: ${data.output_path}\\nDane: ${data.data_files.length}\\nPliki: ${data.assets}\\nPowiązania: ${data.links}`;});});
document.getElementById('packageForm').addEventListener('submit',event=>{event.preventDefault();submitForm(event.currentTarget,document.getElementById('status'),'/transfer/package',async(response,status)=>{const url=URL.createObjectURL(await response.blob());const link=document.createElement('a');link.href=url;link.download='pim-transfer.zip';link.textContent='Pobierz sprawdzoną paczkę ZIP';status.replaceChildren(link);});});
</script></body></html>'''
