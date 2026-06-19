# Dokumentacja przekazania do kolejnego narzedzia

Ten dokument opisuje, co z prototypu `BuildData AI Products` warto wykorzystac
przy budowie kolejnego narzedzia w nowym repozytorium.

Obecne repo traktujemy jako prototyp i zrodlo wiedzy, nie jako idealna baze
produkcyjna. W trakcie pracy zmienial sie kierunek UI i workflow, dlatego w
nowym narzedziu lepiej przeniesc tylko sprawdzone moduly oraz decyzje
projektowe, a interfejs zbudowac od nowa.

## Cel obecnego narzedzia

`BuildData AI Products` sluzy do przygotowania danych produktowych do struktury
zgodnej z eksportem PIM uzywanym przez agenta.

Glowny przeplyw:

```text
model PIM -> plik importowany klienta -> mapowanie -> podglad produktu
          -> uzupelnianie danych -> products.json
```

Narzedzie obsluguje:

- wczytanie modelu produktu PIM z plikow `productsModels.json` i
  `productsAttributes.json`,
- wczytanie pliku klienta `.xlsx`, `.json`, `.csv`, `.tsv`,
- mapowanie danych klienta do pol modelu PIM,
- obsluge typoszeregu jako tabeli wariantow produktu,
- czyszczenie wartosci, przeliczanie jednostek i mapowanie odpowiedzi
  slownikowych,
- reguly wierszy dla plikow, w ktorych jedne wiersze sa produktem, a inne
  wariantami,
- zapis projektu mapowania,
- uzupelnianie zmapowanych danych z dodatkowego pliku,
- generowanie `products.json`.

## Najwazniejsze decyzje projektowe

### 1. Model PIM jest punktem startowym

Program nie powinien pozwalac na mapowanie danych klienta bez zaakceptowanego
modelu PIM.

W nowym repo warto zachowac zasade:

```text
najpierw model PIM -> potem plik klienta -> potem mapowanie
```

Minimalny zestaw modelu dla produktow:

```text
productsModels.json
productsAttributes.json
```

Plik `products.json` nie jest konieczny do zbudowania samego modelu mapowania.
Moze byc przydatny tylko jako przyklad danych lub do testow zgodnosci eksportu.

### 2. Wszystkie cechy musza pochodzic z modelu

W obecnym kierunku nie dodajemy juz "cech wlasnych" z poziomu importera.

Nowe narzedzie powinno mapowac tylko do:

- pol standardowych produktu,
- atrybutow PIM z zaakceptowanego modelu,
- pol typoszeregu wynikajacych z modelu PIM.

Jesli brakuje cechy, powinna byc najpierw dodana w PIM, a dopiero potem
widoczna w narzedziu importu.

### 3. Typoszereg jest tabela, nie lista plaskich pol

Typoszereg powinien byc traktowany jako osobna tabela wariantow produktu.

Przyklad:

```text
Produkt: Plyta izolacyjna X

Typoszereg:
  wariant | grubosc | lambda | gestosc | cieplo wlasciwe | PIM ID
  1       | 50      | 0.035  | 120     | 1030             | AR001
  2       | 100     | 0.035  | 120     | 1030             | AR002
```

W podgladzie nie nalezy mieszac cech produktu i cech typoszeregu.

### 4. Jednostki sa osobne od wartosci

Dla danych liczbowych nalezy osobno przechowywac:

- wartosc,
- jednostke z pliku,
- jednostke docelowa z modelu,
- formule lub wspolczynnik przeliczenia.

Przyklad:

```text
kolumna klienta: "Grubosc [mm]"
wartosc: 50
jednostka zrodla: mm
jednostka modelu: m
mnoznik: 0.001
wynik: 0.05
```

### 5. Pola wyboru wymagaja mapowania wartosci

Jesli cecha w PIM jest polem wyboru jednokrotnego lub wielokrotnego, a klient
ma inne wartosci tekstowe, import nie powinien automatycznie zgadywac wyniku.

Operator musi ustawic mape:

```text
wartosc klienta -> opcja PIM
```

Bez tej mapy dana nie powinna byc importowana do pola slownikowego.

Ta sama zasada dotyczy recznej edycji i recznego uzupelniania danych. UI nie
moze pokazac zwyklego pola tekstowego dla cechy slownikowej.

Wymagane kontrolki:

```text
free_text      -> input/textarea
single_choice  -> select z jedna opcja PIM
multi_choice   -> select wielokrotny albo checkboxy
```

Wartosc zapisywana w sesji uzupelniania powinna byc zgodna z opcja PIM, najlepiej
jako obiekt zawierajacy co najmniej:

```json
{
  "id": 123,
  "label": "Izolacja termiczna",
  "value": "Izolacja termiczna"
}
```

Dla `multi_choice` sesja powinna zapisac tablice takich obiektow. Podglad
produktu powinien pokazywac etykiety opcji, nie surowy JSON.

### 6. Uzupelnianie danych jest osobnym etapem

Uzupelnianie nie powinno byc czescia glownego mapowania. Powinno miec osobny
tryb pracy po zmapowaniu produktu.

W obecnym narzedziu sa dwa sensowne scenariusze:

```text
1. Dane typowe
   Jeden rekord z pliku uzupelnien dopisuje wybrane cechy do wielu produktow.

2. Dane dopasowane po tej samej cesze
   Plik uzupelnien zawiera te same produkty i dodatkowe dane, np. linki do
   obrazkow. Program dopasowuje rekordy po wspolnej cesze, np. nazwa produktu.
```

Drugi scenariusz jest wazny dla przypadkow typu:

```text
mapowanie glowne:
  nazwa produktu
  opis
  typoszereg

plik uzupelnien:
  nazwa produktu
  link do packshotu
  link do karty technicznej
```

Operator powinien wskazac:

```text
cecha w mapowaniu glownym: Nazwa
cecha w pliku uzupelnien: Nazwa
cecha do dopisania: Link do obrazka
```

System powinien dopasowac produkty po wartosci nazwy i dopisac wskazane dane.

## Co warto przeniesc do nowego repo

### Moduly

Najbardziej wartosciowe do przeniesienia:

```text
data_master_app/mapping.py
data_master_app/converter.py
data_master_app/canonical_model.py
data_master_app/mapping_model.py
tests/test_converter.py
tests/test_mapping_model.py
tests/test_canonical_model.py
```

Nie trzeba przenosic ich 1:1. Lepiej potraktowac je jako zrodlo logiki i testow.

### Funkcje warte zachowania

Z `mapping.py`:

- odczyt modelu PIM z plikow,
- budowanie listy pol docelowych,
- wykrywanie typoszeregu,
- sugestie mapowania kolumn,
- czyszczenie wartosci,
- przeliczanie jednostek,
- mapowanie odpowiedzi slownikowych,
- reguly wierszy i hierarchii.

Z `converter.py`:

- odczyt `.xlsx`, `.json`, `.csv`, `.tsv`,
- flattenowanie struktur JSON,
- generowanie struktury `products.json`,
- tworzenie atrybutow PIM,
- dopisywanie danych z sesji uzupelniania,
- raporty eksportu.

Z testow:

- testy mapowania kolumn,
- testy typoszeregu,
- testy reguly Product/Article,
- testy uzupelniania danych,
- testy eksportu `products.json`.

## Czego nie przenosic 1:1

### 1. Obecny `web_ui.py`

Plik `data_master_app/web_ui.py` ma bardzo duzo logiki UI i historii zmian.
Jest dobry jako dokumentacja tego, czego potrzebowalismy, ale nie jako baza dla
nowego interfejsu.

W nowym repo lepiej zrobic UI modulowo:

```text
frontend/
  model-import
  main-mapping
  product-preview
  enrichment
  project-save-load
```

albo w prostym wariancie FastAPI + osobne szablony:

```text
templates/
  layout.html
  model_import.html
  mapping.html
  enrichment.html
  preview.html
```

### 2. Funkcji zwiazanych z systemami i elementami budowlanymi

Obecne narzedzie ma byc produktowe. Elementy budowlane i systemy powinny byc
oddzielnymi narzedziami albo oddzielnymi modulami w przyszlosci.

Do nowego narzedzia produktowego nie przenosic:

- mapowania systemow,
- mapowania building elements,
- logiki warstw systemow.

### 3. Cech wlasnych tworzonych w importerze

Kierunek docelowy: importer nie tworzy nowych cech. Importer mapuje do
zaakceptowanego modelu PIM.

## Proponowana architektura nowego repo

```text
builddata-products-tool/
  app/
    main.py
    services/
      pim_model_loader.py
      source_reader.py
      mapping_engine.py
      product_builder.py
      enrichment_engine.py
      project_store.py
    models/
      pim_model.py
      mapping_profile.py
      enrichment_session.py
      product_preview.py
    api/
      model.py
      mapping.py
      enrichment.py
      export.py
  frontend/
    ...
  tests/
    test_pim_model_loader.py
    test_source_reader.py
    test_mapping_engine.py
    test_enrichment_engine.py
    test_product_export.py
  docs/
    PRODUCT_WORKFLOW.md
    DATA_MODEL.md
    ENRICHMENT.md
```

Jesli narzedzie ma byc proste i lokalne, mozna zostac przy FastAPI. Jesli UI ma
byc mocniej interaktywny, warto rozwazyc frontend osobno, np. React/Vite, a
FastAPI zostawic jako API.

## Proponowany workflow UI

### Ekran 1. Model PIM

Widoczne:

- wczytaj `productsModels.json`,
- wczytaj `productsAttributes.json`,
- zaakceptuj model,
- podsumowanie: liczba modeli, wybrany model, liczba cech, liczba cech
  typoszeregu.

Zasada:

```text
bez zaakceptowanego modelu nie ma dalszych krokow
```

### Ekran 2. Mapowanie produktu

Widoczne:

- wczytaj plik klienta,
- reguly Product/Article,
- mapowanie cech produktu,
- mapowanie typoszeregu,
- podglad produktu,
- eksport `products.json`.

Nie pokazywac:

- pustych komunikatow technicznych,
- calego JSON-a jako glownego widoku,
- duplikatow przyciskow zapisu.

### Ekran 3. Uzupelnianie danych

Widoczne dopiero po zmapowaniu produktu.

Krok 1:

- wybierz plik uzupelnien,
- mapuj plik uzupelnien do tego samego modelu,
- zaakceptuj mapowanie.

Krok 2, widoczny dopiero po zaakceptowaniu mapowania:

- wybierz tryb uzupelniania:
  - aktualny produkt,
  - wybrane produkty,
  - wszystkie produkty,
  - produkty wedlug cechy i wartosci,
  - dopasuj po tej samej cesze,
- wybierz cechy do dopisania,
- zastosuj zmiane,
- cofnij ostatnia zmiane,
- usun dopisane dane.

Jesli operator wlaczy reczna edycje produktu, formularz musi respektowac typ
cechy z modelu PIM:

```text
pole tekstowe       - mozna wpisac wartosc
wybor jednokrotny   - trzeba wybrac jedna opcje PIM
wybor wielokrotny   - trzeba wybrac wiele opcji PIM
```

Nie wolno pozwalac na reczne wpisanie dowolnego tekstu do pola wyboru.

Podglad powinien pokazywac wynik w tabeli produktu i typoszeregu, a dane
dopisane powinny byc oznaczone innym kolorem.

## Format projektu mapowania

Projekt mapowania powinien byc jednym plikiem JSON.

Powinien zawierac:

```json
{
  "model_version": "mapping-project.v1",
  "name": "projekt-klienta",
  "product_model_id": "...",
  "product_mapping": {},
  "product_mapping_profile": {},
  "supplement_mapping": {},
  "supplement_mapping_profile": {},
  "enrichment_session": {},
  "embedded_files": {
    "product_model_files": [],
    "customer_data_file": null
  }
}
```

Uwagi:

- projekt powinien pozwalac wrocic do pracy bez ponownego wybierania plikow,
- jesli plikow brakuje lub zmienily sie, UI powinno pokazac jasny komunikat,
- sesja uzupelniania powinna byc osobna od mapowania glownego.

## Sesja uzupelniania

Sesja uzupelniania powinna zapamietywac:

- jakie dane dodano,
- z jakiego pliku uzupelnien pochodza,
- czy byly dodane recznie czy z pliku,
- do ktorych produktow zostaly dodane,
- czy nadpisywaly istniejace dane,
- czy mozna je cofnac.

Przykladowe akcje:

```json
{
  "source": "same_feature_match",
  "scope": "match_by_feature",
  "match_field": "product.name.value",
  "supplement_match_field": "product.name.value",
  "selected_attributes": ["303:0:0"],
  "preserve_existing": true
}
```

## Najwazniejsze lekcje z prototypu

1. Nie zaczynac od UI z wszystkimi opcjami naraz.
2. Kazdy etap powinien pokazywac tylko te funkcje, ktore sa juz aktywne.
3. Nie pokazywac pustych sekcji typu "brak danych", jesli nic nie wnosza.
4. Nie mieszac mapowania glownego z uzupelnianiem danych.
5. Nie dublowac przyciskow zapisu.
6. Podglad produktu jest wazniejszy niz podglad JSON.
7. Typoszereg musi byc osobna tabela.
8. Wartosci slownikowe musza miec jawna mape odpowiedzi.
9. Reczna edycja musi respektowac typ pola PIM: tekst, wybor jednokrotny albo
   wybor wielokrotny.
10. Plik uzupelnien moze byc:
   - produktem typowym,
   - tabela z tymi samymi produktami i dodatkowymi danymi.
11. Nowe repo powinno zaczac od testow i malych modulow, nie od jednego duzego
    pliku UI.

## Minimalny zakres MVP dla nowego repo

Pierwsza wersja powinna miec tylko:

```text
1. Wczytaj model PIM.
2. Wczytaj plik klienta.
3. Zmapuj cechy produktu i typoszeregu.
4. Pokaz podglad produktu.
5. Zapisz products.json.
6. Zapisz/otworz projekt mapowania.
```

Dopiero drugi etap:

```text
7. Wczytaj plik uzupelnien.
8. Zmapuj plik uzupelnien.
9. Dopisz dane do wybranych produktow.
10. Dopasuj dane po tej samej cesze.
```

## Rekomendacja

Budowac nowe narzedzie w nowym repozytorium.

Obecne repo zostawic jako:

- prototyp funkcjonalny,
- zrodlo przypadkow testowych,
- zrodlo decyzji mapowania,
- magazyn sprawdzonych funkcji parsowania i eksportu.

Nie przenosic obecnego interfejsu 1:1. Przeniesc logike domenowa i testy,
a UI napisac od nowa wedlug prostszego workflow.

## Osobny projekt dla systemow

Systemy i elementy budowlane maja osobna specyfikacje startowa:

```text
docs/SYSTEMS_MAPPING_PROJECT.md
```

Ten dokument opisuje osobne narzedzie `BuildData AI Systems`, ktore powinno
wczytywac referencyjny `products.json`, mapowac systemy, warianty, warstwy i
produkty w warstwach, a nastepnie eksportowac strukture systemow niezaleznie od
narzedzia produktowego.
