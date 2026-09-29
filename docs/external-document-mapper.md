# Mapper dokumentow zewnetrznych

W glownym mapperze produktow, w sekcji Zrodla i powiazania, rozwin podmodel dokumentow i wybierz zrodlo Mapper dokumentow zewnetrznych.

Wybierz katalog. Aplikacja skanuje metadane nazw i sciezek, bez przesylania zawartosci dokumentow. Wskaz kolumne klucza w danych produktu i odpowiadajacy jej poziom katalogu.

Kazde pole podmodelu ma niezalezny wybor: Katalog 1, Katalog 2 itd., nazwa pliku, nazwa bez rozszerzenia, rozszerzenie lub sciezka. Opcja Nie mapuj pomija pole. Pola wynikaja z definicji wczytanego modelu. Nazwy slownikowe musza odpowiadac wartosciom slownika modelu.

Przyklad wzgledem wybranego folderu: `P1/Karty/pl/instrukcja.pdf`:

- Katalog 1 = P1, lacznik produktu.
- Katalog 2 = Karty, mozliwe zrodlo typu dokumentu.
- Katalog 3 = pl, mozliwe zrodlo jezyka.
- Nazwa bez rozszerzenia = instrukcja.
- Sciezka pliku = P1/Karty/pl/instrukcja.pdf.

Lista metadanych i mapowanie sa zapisane w `product_mapping_profile._nested_relations` standardowego projektu. Podglad podmodelu korzysta z tej samej relacji co eksport. Wiele plikow tworzy wiele rekordow w jednym `products.json`.

Atrybut Files otrzymuje wpis w `filesAttributes` powiazany przez parentHash z wierszem metadanych. Lokalna referencja jest zapisana w dodatkowym polu `sourcePath`, a `fileUrl` pozostaje null do przeslania. Trzeba zmapowac co najmniej jedna ceche metadanych dokumentu razem z plikiem. Nie jest to gotowy URL PIM. Starszy importer nie rozpoznaje jeszcze automatycznie sourcePath; adaptacja wysylki tego wariantu JSON pozostaje osobnym etapem. Nie nalezy importowac takich lokalnych referencji starszym importerem jako gotowych plikow serwerowych.

Obecnie integracja dotyczy podmodelow produktowych jednego poziomu. Samodzielny ekran skanowania katalogow pozostaje dostepny, ale nie jest wymagany do tego przeplywu. Ponowny skan aktualizuje liste plikow. Zapis projektu nie nadaje przegladarce stalego dostepu do katalogu.
