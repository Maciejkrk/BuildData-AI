# BuildData AI Products Model

## Cel

Model produktu BuildData AI Products jest formatem kanonicznym pomiedzy danymi klienta
a eksportem do PIM JSON.

Nie kopiujemy calego swiata klienta. Przechowujemy tylko dane potrzebne do:

- mapowania produktow,
- uzupelniania brakow,
- kontroli jakosci danych,
- eksportu do struktury PIM uzywanej przez agenta,
- przyszlych eksportow do innych formatow.

## Glowna Zasada

Kazde wazne pole ma nie tylko wartosc, ale tez informacje skad pochodzi i czy
wymaga sprawdzenia.

```json
{
  "value": 0.035,
  "unit": "W/mK",
  "source": "normative_model",
  "confidence": "inferred",
  "requires_review": true,
  "reason": "Uzupelniono typowa wartoscia dla welny mineralnej.",
  "rule_id": "mineral_wool_default_lambda"
}
```

## FieldValue

Wspolna struktura dla pol modelu:

```text
value             - wartosc pola
unit              - jednostka, jesli dotyczy
source            - client | pim_reference | normative_model | manual | import_rule
confidence        - confirmed | inferred | estimated | missing
requires_review   - czy czlowiek powinien zatwierdzic wartosc
reason            - dlaczego wartosc jest taka albo dlaczego jej brakuje
rule_id           - identyfikator reguly uzupelniajacej
updated_at        - data zmiany / uzupelnienia
```

## Measurement

Dla wartosci liczbowych jednostka jest zapisywana osobno od wartosci. To jest
wazne, bo rozne systemy podaja jednostki w roznych formatach, np. `W/mK`,
`W/(m*K)`, `kg/m3`, `kg/m³`, `J/kgK`.

```text
Measurement
  value: FieldValue
  unit: FieldValue
```

Przyklad:

```json
{
  "value": {
    "value": 0.035,
    "source": "client",
    "confidence": "confirmed"
  },
  "unit": {
    "value": "W/mK",
    "source": "client",
    "confidence": "confirmed"
  }
}
```

## Product v1

```text
Product
  model_version
  source_record_id
  pim_product_id
  code
  name
  category[]
  unit
  manufacturer
  product_url
  short_name
  full_name
  technical_name
  description
  properties
  application
  surface_preparation
  usage_method
  comments
  warnings
  norms
  storage
  packages[]
  technical_properties[]
  documents[]
  type_series[]
  raw_links[]
```

## Type Series

Typoszereg jest tabela wariantow produktu. Uzytkownik importu powinien moc
przypisac kolumny klienta do tej tabeli, a nie tylko do prostych pol produktu.

Standardowe pola wiersza typoszeregu:

```text
TypeSeriesRow
  variant_code
  variant_name
  thickness
  lambda_value
  density
  vapor_permeability_mu
  specific_heat
```

Standard minimalny powinien obejmowac:

```text
thickness              - grubosc, np. m albo mm
lambda_value           - przewodnosc cieplna, np. W/mK
density                - gestosc, np. kg/m3
vapor_permeability_mu  - wspolczynnik oporu dyfuzyjnego mu
specific_heat          - cieplo wlasciwe, np. J/kgK
```

Nie ograniczamy modelu tylko do tych pol, ale dodatkowe parametry wariantu musza
byc najpierw dodane do modelu PIM. Program mapuje tylko pola istniejace w
zaakceptowanym modelu.

## Przyklad Produktu

```json
{
  "model_version": "product.v1",
  "pim_product_id": {
    "value": 6076,
    "source": "pim_reference",
    "confidence": "confirmed"
  },
  "code": {
    "value": "1ED2A1926E5D6F8289CC35116F5BBDA6",
    "source": "pim_reference",
    "confidence": "confirmed"
  },
  "name": {
    "value": "FAST AQUA",
    "source": "client",
    "confidence": "confirmed"
  },
  "product_url": {
    "value": "https://example.com/fast-aqua",
    "source": "client",
    "confidence": "confirmed"
  },
  "type_series": [
    {
      "thickness": {
        "value": {
          "value": 0.05,
          "source": "client",
          "confidence": "confirmed"
        },
        "unit": {
          "value": "m",
          "source": "client",
          "confidence": "confirmed"
        }
      },
      "lambda_value": {
        "value": {
          "value": 0.035,
          "source": "normative_model",
          "confidence": "inferred",
          "requires_review": true,
          "rule_id": "mineral_wool_default_lambda",
          "reason": "Brak lambda w danych klienta."
        },
        "unit": {
          "value": "W/mK",
          "source": "normative_model",
          "confidence": "inferred",
          "requires_review": true
        }
      },
      "specific_heat": {
        "value": {
          "value": 1030,
          "source": "normative_model",
          "confidence": "inferred",
          "requires_review": true,
          "rule_id": "mineral_wool_default_specific_heat",
          "reason": "Brak ciepla wlasciwego w danych klienta."
        },
        "unit": {
          "value": "J/kgK",
          "source": "normative_model",
          "confidence": "inferred",
          "requires_review": true
        }
      }
    }
  ]
}
```

## Jak Oznaczamy Dane

### Dane od klienta

```json
{
  "value": "FAST AQUA",
  "source": "client",
  "confidence": "confirmed",
  "requires_review": false
}
```

### Dane z PIM referencyjnego

```json
{
  "value": 6076,
  "source": "pim_reference",
  "confidence": "confirmed",
  "requires_review": false
}
```

### Dane uzupelnione normowo

```json
{
  "value": 0.035,
  "unit": "W/mK",
  "source": "normative_model",
  "confidence": "inferred",
  "requires_review": true,
  "rule_id": "mineral_wool_default_lambda",
  "reason": "Uzupelniono z modelu normowego, bo klient nie podal wartosci."
}
```

### Brak danych

```json
{
  "value": null,
  "source": "client",
  "confidence": "missing",
  "requires_review": true,
  "reason": "Brak pola w danych klienta."
}
```

## Mapowanie

Mapowanie klienta powinno prowadzic do tego modelu:

```text
kolumna klienta -> Product.field -> FieldValue
kolumna klienta -> Product.type_series[].field -> Measurement
kolumna klienta -> Product.type_series[].field -> Measurement
```

Dopiero z modelu `Product` budujemy eksporty:

```text
Product -> products.json PIM
Product -> raport brakow
Product -> przyszle eksporty BIM/ERP/ofertowe
```
