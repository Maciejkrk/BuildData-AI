# Mapping and Typical Data Workflow

## Cel

Mapowanie nie moze byc tylko lista `kolumna -> pole`. Operator importu musi
zdecydowac, co zrobic z kazda kolumna i jak zbudowac wynikowy produkt w modelu
BuildData AI Products.

## Decyzje Dla Kolumny

Dla kazdej kolumny z pliku klienta operator powinien moc wybrac:

```text
ignore                      - pomin kolumne
model_field                 - zapisz do pola z modelu produktu PIM
type_series_field           - zapisz do pola typoszeregu z modelu produktu PIM
```

Operator nie tworzy cech wlasnych w projekcie mapowania. Jezeli cecha ma byc
importowana, musi najpierw istniec w zaakceptowanym modelu produktu PIM.

Jesli kolumna jest mapowana do cechy z modelu, UI musi pozwalac ustawic:

```text
docelowa cecha z modelu PIM
jednostka
kolumna z jednostka, jesli jednostka jest w osobnej kolumnie
transformacje wartosci
```

## Pola Wyboru

Pola wyboru w modelu PIM nie moga byc edytowane jako zwykly tekst.

Jesli cecha ma opcje slownikowe:

```text
single_choice  - UI pokazuje select z jedna wartoscia
multi_choice   - UI pokazuje select wielokrotny albo checkboxy
free_text      - UI pokazuje pole tekstowe
```

Ta zasada dotyczy zarowno mapowania automatycznego, jak i recznego
uzupelniania danych. Operator nie powinien moc wpisac dowolnego tekstu do pola
slownikowego, bo taki zapis nie bedzie zgodny z modelem PIM.

Dla danych z pliku klienta albo pliku uzupelnien wartosci spoza slownika musza
byc jawnie zmapowane:

```text
wartosc z pliku -> opcja PIM
```

Bez takiej mapy wartosc powinna pozostac niezaimportowana lub oznaczona jako
wymagajaca decyzji operatora.

## Transformacje Wartosc

Czyszczenie danych powinno byc jawne i zapisane w profilu mapowania.

Przyklady:

```text
trim
remove_text: "okolo"
remove_text: "lambda ="
replace_text: "," -> "."
parse_number
unit_conversion: mm -> m, factor 0.001
```

Przyklad reguly:

```json
{
  "source_column": "Grubosc",
  "target_kind": "type_series_field",
  "target_path": "type_series[].thickness.value",
  "unit": "mm",
  "transforms": [
    { "kind": "remove_text", "search": "mm" },
    { "kind": "decimal_comma_to_dot" },
    { "kind": "parse_number" }
  ]
}
```

## Typoszereg

Typoszereg powinien byc widoczny w podgladzie jako tabela.

Minimalne kolumny standardowe:

```text
variant_code
variant_name
thickness value/unit
lambda value/unit
density value/unit
vapor permeability mu value/unit
specific heat value/unit
additional properties
```

Operator musi moc przypisac kolumny klienta do standardowych pol albo dodac je
jako dodatkowe parametry typoszeregu.

## Podglad Produktu

Po analizie mapowania UI powinien pokazac podglad nowego produktu:

```text
Product
  nazwa
  kod
  kategoria
  opis
  pola z modelu PIM
  typoszereg jako tabela
  braki danych
  dane wymagajace zatwierdzenia
```

Podglad powinien pokazywac wynik po transformacjach, nie surowa wartosc z Excela.

## Dane Typowe

Dane typowe sa osobnym importem. Moga sluzyc do:

```text
fill_if_missing             - uzupelnij tylko braki
replace_existing            - zastap wartosc z danych klienta
add_type_series_property    - dodaj jako parametr typoszeregu z modelu PIM
```

Kazda wartosc dodana z danych typowych musi miec:

```text
source = normative_model
confidence = inferred albo estimated
requires_review = true
rule_id
reason
```

## Przyklad Uzupelnienia

```json
{
  "rule_id": "mineral_wool_specific_heat",
  "action": "fill_if_missing",
  "target_path": "type_series[].specific_heat.value",
  "typical_source_path": "materials.mineral_wool.specific_heat",
  "condition_path": "product.category[].value",
  "condition_value": "Welna mineralna",
  "requires_review": true,
  "reason": "Brak ciepla wlasciwego w danych klienta. Uzupelniono z danych typowych."
}
```
