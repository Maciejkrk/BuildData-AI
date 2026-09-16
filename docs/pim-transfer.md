# Paczka wymiany mapper - importer

Ekran `/transfer` (link "Paczka PIM" w produktach i elementach budowlanych)
tworzy przenosny ZIP. Nie laczy sie z SQL ani z Azure.

Wybierz wyeksportowane JSON-y danych wraz z ich modelami/atrybutami, JSON
powiazan oraz zalaczniki. Nazwy JSON-ow sa takie same jak w dotychczasowym
eksporcie, np. products.json, productsModels.json, productsAttributes.json.
Nie wgrywaj do tej paczki konfiguracji ani hasel.

Powiazania zalacznikow sa obecnie jawnie przygotowanym JSON-em. Nie ma jeszcze
automatycznego rozpoznawania produktow z nazw folderow. `owner_id` oznacza Id
obiektu w WYEKSPORTOWANYM JSON, nie kod produktu z Excela. `attribute_id` musi
wskazywac rzeczywisty atrybut typu Files, a nie nazwe/typ/jezyk dokumentu.

```json
[
  {
    "file": "karta.pdf",
    "module": "products",
    "owner_id": 101,
    "version_id": 1,
    "attribute_id": 17,
    "order": 0,
    "display_name": "Karta techniczna"
  }
]
```

Kazdy kolejny plik tej samej cechy ma osobny wpis i inny `order`.
Plik nalezacy do dokumentu w Model_Array dodatkowo wskazuje:

```json
{
  "parent_hash": "hash-wiersza-dokumentu-z-JSON",
  "parent_attribute_id": 740,
  "main_attribute_id": 151,
  "row_i": 1
}
```

Powyzsze ID sa przykladowe, nie stanowia ustawien domyslnych.
Dla kolorow i grup kolorow zamiast attribute_id stosuje sie parameter_name
(np. MainTexture albo Cover), zgodnie z modelem PIM.

## Pliki w podfolderach

CLI moze pobrac zalaczniki z katalogu. Pole `file` zawiera wtedy sciezke
wzgledna, np. `PROD-001/karta.pdf`. Sciezki wychodzace poza katalog sa blokowane.

```powershell
python -m data_master_app.transfer --data C:\Import\Dane --files C:\Import\Dokumenty --links C:\Import\powiazania.json --output C:\Import\pim-transfer.zip
```

Eksport nie nadpisuje istniejacego ZIP. Limit paczki: 512 MiB danych.
Webowy wybor zalacznikow uzywa nazw plikow bez podfolderow; przy powtarzajacych
sie nazwach nalezy uzyc CLI ze sciezkami wzglednymi.

## Kontrakt pim-transfer.v1

- `manifest.json`: format, package_id UUID, rozmiary i SHA-256 kazdego pliku.
- `data/`: niezmienione JSON-y katalogu i modeli.
- `assets/`: binarne pliki nazwane SHA-256 i rozszerzeniem.
- `file-links.json`: zweryfikowane relacje, oryginalne nazwy i metadane.

SHA-256 wykrywa uszkodzenie, NIE stanowi podpisu/autoryzacji paczki. Docelowy
tenant i decyzja o zapisie sa wybierane niezaleznie w importerze.
Importer odrzuca niebezpieczne sciezki ZIP, duplikaty i niespojne metadane.
Nigdy nie ustawia lokalnych sciezek jako fileUrl. Docelowy URL powstaje dopiero
po uploadzie do Azure w osobnym procesie.

Wspolny modul pim_bundle.py jest kopiowany do nowej wersji importera. Test
zgodnosci sprawdza identycznosc obu kopii; zmiana kontraktu wymaga ich aktualizacji.
Nowy importer: ../PIM-Data-Importer-next (obok repo mappera), instrukcja TRANSFER.md.
