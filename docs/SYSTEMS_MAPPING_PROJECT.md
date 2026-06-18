# BuildData AI - Elementy budowlane - dokument startowy nowego projektu

Ten dokument opisuje zalozenia do otwarcia osobnego projektu dla mapowania
systemow budowlanych. Traktujemy go jako specyfikacje startowa dla nowego repo
albo nowego narzedzia obok modulu produktowego `BuildData AI`.

Obecny modul produktowy `BuildData AI` pozostaje narzedziem produktowym. Systemy i
elementy budowlane powinny byc rozwijane osobno, bo maja inna logike danych:
relacje, warianty, warstwy, skladniki i powiazanie z produktami.

## Cel narzedzia

Modul `Elementy budowlane` w `BuildData AI` ma przygotowywac dane systemow budowlanych do importu do
PIM albo do formatu uzywanego dalej przez agenta.

Glowny przeplyw:

```text
model PIM systemow -> zmapowane produkty -> plik systemow klienta
                   -> mapowanie systemow -> podglad systemu
                   -> building_elements.json / systems.json
```

Narzedzie nie powinno tworzyc produktow. Produkty powinny byc przygotowane
wczesniej przez modul produktowy `BuildData AI` i wczytane jako referencja.

## Dlaczego osobne narzedzie

Produkt jest jedna jednostka danych z opcjonalnym typoszeregiem.

System jest struktura relacyjna:

```text
System
  warianty systemu
    warstwy
      produkty albo grupy produktow
      ilosci / zuzycia / role
      produkt domyslny
```

Z tego powodu UI i reguly mapowania powinny byc inne niz w produkcie.

## Dane wejsciowe

### 1. Model PIM systemow

Najpierw trzeba wczytac model PIM dla systemow lub elementow budowlanych.

Nazwy plikow eksportu z PIM trzeba jeszcze potwierdzic, ale zasada powinna byc
taka sama jak w produktach:

```text
models.json      - lista modeli PIM
attributes.json  - lista atrybutow PIM
```

Nie nalezy kodowac na sztywno ID atrybutow. Narzedzie musi odczytywac:

- ID modelu systemu,
- ID atrybutow glownych systemu,
- ID tabel zagniezdzonych,
- ID atrybutow wariantow,
- ID atrybutow warstw,
- ID atrybutow produktow dostepnych w warstwie,
- typ pola: tekst, liczba, wybor jednokrotny, wybor wielokrotny, plik,
- opcje slownikowe,
- jednostki.

Lekcja z narzedzia produktowego: eksport nie moze opierac sie na stalych typu
`280`, `283`, `285`, `289`, jezeli aktualny model PIM ma inne ID.

### 2. Zmapowane produkty

Systemy musza miec dostep do listy produktow, do ktorych beda sie odnosic.

Zrodlem powinna byc jedna z opcji:

```text
products.json wygenerowany z BuildData AI
albo
aktualny eksport produktow z PIM
```

Narzedzie musi zbudowac indeks produktow po:

- PIM ID,
- kodzie produktu,
- nazwie produktu,
- nazwie wariantu,
- SAP ID / article ID,
- ewentualnie grupie produktow.

Bez indeksu produktow system nie powinien eksportowac danych do PIM, bo nie da
sie jednoznacznie zbudowac relacji system -> produkt.

### 3. Plik systemow klienta

Formaty analogiczne do produktu:

```text
.xlsx
.json
.csv
.tsv
```

Plik klienta moze miec rozne struktury:

```text
1. Jeden wiersz = jedna warstwa systemu.
2. Jeden wiersz = system, wariant, warstwa albo produkt, rozrozniane kolumna typu.
3. Wiersze maja ID i Parent ID.
4. System wskazuje grupe produktow, a nie konkretny produkt.
5. System wskazuje produkt domyslny oraz produkty alternatywne.
```

## Model kanoniczny systemu

Przed eksportem do PIM dane powinny trafic do modelu kanonicznego.

Proponowana struktura:

```text
System
  source_record_id
  pim_system_id
  name
  code
  type
  application
  description
  standards[]
  variants[]

SystemVariant
  code
  name
  description
  layers[]

SystemLayer
  position
  name
  layer_type
  required
  products[]

SystemLayerProduct
  product_reference
  product_group_reference
  role
  quantity
  quantity_unit
  is_default
  conditions
```

Wazne: `product_reference` powinien byc rozstrzygany dopiero po wczytaniu
indeksu produktow. Jesli klient podal tylko nazwe grupy produktow, narzedzie
powinno oznaczyc to jako referencje do grupy, a nie zgadywac jednego produktu.

## Podstawowe pojecia

### System

Glowna jednostka, np. system ocieplen, system suchej zabudowy, system posadzki.

Minimalne pola:

```text
nazwa systemu
typ systemu / zastosowanie
opis
normy / klasyfikacje
```

### Wariant systemu

System moze miec warianty, np. rozne wykonczenia albo konfiguracje.

Przyklad:

```text
System ETICS
  wariant: tynk silikonowy
  wariant: tynk mineralny
```

Jesli klient nie ma wariantow, narzedzie powinno utworzyc wariant domyslny.

### Warstwa

Warstwa jest pozycja w wariancie systemu.

Minimalne pola:

```text
pozycja warstwy
nazwa warstwy
typ warstwy
```

Warstwy musza miec kolejnosc. Jesli klient jej nie podaje, operator musi moc ja
ustawic albo narzedzie powinno nadac kolejnosc zgodnie z wystapieniem w pliku.

### Produkt w warstwie

Warstwa moze miec:

- jeden konkretny produkt,
- wiele produktow alternatywnych,
- produkt domyslny,
- odwolanie do grupy produktow.

Nie wolno cicho pominac nierozpoznanych produktow. Trzeba pokazac raport:

```text
nierozpoznane produkty
nierozpoznane grupy produktow
produkty pasujace do wielu pozycji
warstwy bez produktu
```

## Reguly wierszy i hierarchii

Narzedzie powinno wspierac reguly podobne do produktu, ale osobne dla systemow.

Minimalna regula:

```text
kolumna typu wiersza
wartosc oznaczajaca system
wartosc oznaczajaca wariant
wartosc oznaczajaca warstwe
wartosc oznaczajaca produkt w warstwie
kolumna ID
kolumna Parent ID
```

Przyklad:

```text
Object Type Name = System
Object Type Name = Variant
Object Type Name = Layer
Object Type Name = Product
ID
Parent ID
Name
```

Zasada:

```text
wiersz System tworzy system
wiersz Variant tworzy wariant systemu
wiersz Layer tworzy warstwe w wariancie
wiersz Product tworzy produkt w warstwie
```

Jesli klient ma plaski plik, reguly hierarchii moga byc pominiete, a system
powinien byc skladany z kolumn w jednym wierszu.

## Mapowanie

Mapowanie powinno byc prowadzone wzgledem docelowego modelu PIM systemow.

Glowne sekcje UI:

```text
1. Cechy systemu
2. Warianty systemu
3. Warstwy
4. Produkty w warstwach
5. Reguly rozpoznawania produktow i grup produktow
```

Kazde pole musi miec:

```text
kolumna z pliku importowanego
docelowe pole modelu PIM
czyszczenie wartosci
jednostka zrodla
jednostka docelowa
mapowanie odpowiedzi slownikowych
```

Jesli pole PIM jest slownikowe, operator musi zmapowac wartosci:

```text
wartosc klienta -> opcja PIM
```

Bez tego eksport powinien blokowac import tego pola albo oznaczyc je jako
wymagajace decyzji.

## Powiazanie z produktami

Najwazniejsza czesc systemow to rozpoznanie, ktore produkty sa uzyte w
warstwach.

Operator powinien moc wybrac:

```text
kolumna z identyfikatorem produktu
kolumna z nazwa produktu
kolumna z SAP ID / Article ID
kolumna z grupa produktow
tryb dopasowania
```

Tryby dopasowania:

```text
1. Dokladne dopasowanie po PIM ID.
2. Dokladne dopasowanie po kodzie/SAP ID.
3. Dokladne dopasowanie po nazwie.
4. Dopasowanie po grupie produktow.
5. Dopasowanie wspomagane sugestia, ale zatwierdzane przez operatora.
```

AI albo fuzzy matching moze byc pomocne tylko jako sugestia. Eksport relacji
system -> produkt powinien wymagac jednoznacznego wyniku.

## Podglad systemu

Podglad powinien byc wazniejszy niz JSON.

Proponowany widok:

```text
System: ETICS TEST

Cechy systemu:
  nazwa
  typ
  opis
  normy

Warianty:
  Wariant: Tynk silikonowy
    1. Zaprawa klejaca
       - Produkt A
       - Produkt B
    2. Izolacja
       - Produkt C
    3. Warstwa zbrojona
       - Produkt D
```

W podgladzie trzeba oznaczac:

- produkt rozpoznany jednoznacznie,
- produkt nierozpoznany,
- dopasowanie po grupie produktow,
- brak obowiazkowego pola,
- wartosc spoza slownika,
- warstwe bez kolejnosci.

## Eksport

Docelowy eksport powinien byc uzgodniony z PIM.

Prawdopodobne pliki:

```text
building_elements.json
mapping_report.json
```

Mozliwy docelowy payload:

```json
{
  "buildingElementsCount": 1,
  "buildingElements": [
    {
      "Id": 910001,
      "elementTypeId": 1,
      "ModelType": 74,
      "dataVersions": [
        {
          "VersionId": 1,
          "productAttributes": []
        }
      ]
    }
  ]
}
```

To jest tylko przyklad historyczny z prototypu. Nowe narzedzie musi budowac ID
atrybutow, parenty i typy wartosci z aktualnego modelu PIM, nie ze stalych w
kodzie.

## Raport jakosci

Kazdy eksport powinien tworzyc raport:

```text
liczba systemow
liczba wariantow
liczba warstw
liczba produktow w warstwach
nierozpoznane produkty
nierozpoznane grupy
duplikaty
braki wymaganych pol
wartosci spoza slownikow
warstwy bez kolejnosci
systemy bez warstw
warianty bez warstw
```

Eksport powinien moc powstac tylko wtedy, gdy krytyczne bledy sa rozwiazane
albo jawnie zaakceptowane przez operatora.

## Projekt mapowania

Projekt mapowania systemow powinien byc jednym plikiem JSON.

Powinien zawierac:

```json
{
  "model_version": "systems-mapping-project.v1",
  "name": "projekt-systemow-klienta",
  "system_model_id": "...",
  "product_reference_source": {
    "file_name": "products.json",
    "hash": "..."
  },
  "system_mapping_profile": {},
  "row_rules": {},
  "product_matching_rules": {},
  "dictionary_value_maps": {},
  "embedded_files": {
    "system_model_files": [],
    "source_systems_file": null,
    "product_reference_file": null
  }
}
```

Projekt powinien pozwalac wrocic do pracy bez ponownego podpinania plikow. Jesli
plik produktow referencyjnych zostal zmieniony, UI musi pokazac komunikat, bo
moze to zmienic rozpoznanie produktow w systemach.

## MVP nowego projektu

Pierwsza wersja powinna miec tylko:

```text
1. Wczytaj model PIM systemow.
2. Wczytaj referencyjny products.json.
3. Wczytaj plik systemow klienta.
4. Zmapuj system, wariant, warstwe i produkt.
5. Pokaz podglad systemu jako drzewo.
6. Pokaz raport nierozpoznanych produktow.
7. Zapisz building_elements.json.
8. Zapisz/otworz projekt mapowania.
```

Drugi etap:

```text
9. Obsluga produktow wskazanych przez grupe produktow.
10. Ustawianie produktu domyslnego.
11. Mapowanie wartosci slownikowych.
12. Dopasowanie wspomagane sugestiami.
13. Uzupelnianie danych systemow z pliku dodatkowego.
```

## Co mozna przeniesc z obecnego repo

Do wykorzystania jako punkt startowy:

```text
data_master_app/converter.py
  - czytanie xlsx/json/csv/tsv
  - SourceTable
  - flattenowanie JSON
  - raporty eksportu

data_master_app/mapping.py
  - FieldDefinition
  - suggest_mapping
  - apply_cleanup
  - mapowanie slownikow
  - reguly wierszy jako inspiracja

tests/test_converter.py
  - stare testy mapowania systemow
  - testy oddzielnego eksportu produktow i systemow
```

Nie przenosic 1:1:

```text
data_master_app/web_ui.py
```

UI trzeba zbudowac od nowa. Obecny plik UI ma za duzo historii prototypu.

## Testy wymagane od poczatku

Nowe repo powinno zaczac od testow:

```text
test_system_model_loader.py
  - wykrywa model systemu
  - wykrywa tabele wariantow/warstw/produktow
  - czyta typy pol i opcje slownikowe

test_product_reference_index.py
  - indeksuje products.json po PIM ID, SAP ID, nazwie
  - wykrywa duplikaty

test_system_mapping_rules.py
  - sklada system z plaskiego pliku
  - sklada system z ID/Parent ID
  - wykrywa orphan rows

test_system_product_matching.py
  - dopasowanie po kodzie
  - dopasowanie po nazwie
  - dopasowanie po grupie
  - blokada przy wielu wynikach

test_system_export.py
  - eksport uzywa dynamicznych ID z modelu PIM
  - eksport nie uzywa stalych ID z prototypu
  - eksport zachowuje parenty tabel zagniezdzonych
```

Szczegolnie wazny test:

```text
Jesli model PIM ma inne ID niz prototyp, eksport nadal musi byc poprawny.
```

## Otwarte pytania przed implementacja

Przed startem nowego repo trzeba ustalic:

1. Jakie sa rzeczywiste nazwy plikow eksportu modelu systemow z PIM.
2. Czy system w PIM jest `BuildingElement`, `System`, czy innym modelem.
3. Czy warianty, warstwy i produkty sa tabelami zagniezdzonymi w jednym modelu.
4. Jak PIM przechowuje referencje do produktu: ID produktu, ID atrybutu, inna
   tabela relacyjna.
5. Czy dopuszczamy produkt wskazany przez grupe produktow, czy trzeba rozwijac
   grupe do listy produktow przed eksportem.
6. Jak zapisywac ilosci/zuzycie i jednostki.
7. Czy systemy maja wersje jezykowe.

## Rekomendacja

Uruchomic osobne repo, np.:

```text
builddata-ai-systems
```

albo:

```text
builddata-systems-mapper
```

Nie doklejac systemow do obecnego modulu produktowego `BuildData AI`. Obecne repo powinno
zostac zrodlem lekcji, testow i logiki parsowania, a nowe narzedzie powinno
startowac od czystego UI oraz dynamicznego modelu PIM.
