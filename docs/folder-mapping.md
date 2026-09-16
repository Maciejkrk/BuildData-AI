# Mapowanie plikow

Osobna kategoria menu: Mapowanie plikow (`/transfer/folders`).

1. Wybierz wyeksportowane dane i definicje modeli JSON.
2. Wybierz produkty lub elementy budowlane i katalog dokumentow.
3. Wskaz pole identyfikatora (np. `product.Name`, `product.Id`, `version.Code`), wersje danych i poziom katalogu obiektu.
4. Wskaz domyslny atrybut Files albo dodaj reguly podkatalogow do atrybutow Files.
5. Sprawdz wynik i zapisz `powiazania-plikow.json`. Pliki binarne nie sa wtedy przesylane.
6. Przy pozniejszym eksporcie wczytaj plan, aktualne dane JSON i ponownie wybierz katalog. Sprawdz powiazania, potem przygotuj paczke.

Przyklad: `Dokumenty/Marka/PROD-A/Karty/PL/karta.pdf`. Po wybraniu `Dokumenty` poziom obiektu wynosi 2. Regula `Karty` obejmuje takze `Karty/PL`; bardziej szczegolowa regula ma pierwszenstwo. Dopasowanie identyfikatora ignoruje wielkosc liter i skrajne spacje, ale nie usuwa znakow ani zer wiodacych. Nie ma dopasowania przyblizonego.

Plan zapisuje sciezke wzgledna, nazwe pliku, typ/podkatalog, ID obiektu, atrybut, ustawienia i raport. Nie zawiera zawartosci dokumentow. Odczyt i kontrola zawartosci odbywaja sie przy tworzeniu ZIP. Paczke na serwer wysyla osobny importer; skanowanie nie laczy sie z PIM.

## Wiersz polecen

```powershell
python -m data_master_app.folder_links --data C:\Import\Dane --files C:\Import\Dokumenty --key product.Name --version 1 --attribute 17 --output C:\Import\plan.json
python -m data_master_app.transfer --data C:\Import\Dane --files C:\Import\Dokumenty --links C:\Import\plan.json --output C:\Import\paczka.zip
```

Opcje skanera: `--module buildingelements`, `--owner-depth 2`, `--rules reguly.json`.
Reguly JSON: `[{"folder":"Karty","attribute_id":17}]`.
CLI eksportu ponownie odczytuje pliki spod jawnie wskazanego `--files`, a nie ze sciezki podanej we wczytanym planie.

## Ograniczenia pierwszej wersji

- Typ podkatalogu kieruje do atrybutu Files. Nie tworzy jeszcze automatycznie wierszy zlozonego modelu Dokumenty ani wartosci slownikowych Typ/Język. Takie przypisania sa blokowane, gdy wymagaja kontekstu wiersza podmodelu.
- Pola lacznika to obecnie skalarne pola obiektu lub wersji, nie wartosci zagniezdzonych tablic atrybutow.
- Wszystkie nierozwiazane pliki blokuja paczke; plan z raportem mozna zapisac mimo bledow.
- Nowe pliki wymagaja ponownego skanowania. CLI eksportuje zatwierdzona liste z planu, nie dopisuje nowych plikow automatycznie.
- Przegladarka wymaga ponownego wyboru katalogu. Docker nie uzyskuje automatycznie dostepu do lokalnej sciezki Windows.
- Plan opisuje lokalizacje, nie zamraza zawartosci: przy eksporcie pobierana jest aktualna wersja pliku. Integralnosc sprawdzana jest od utworzenia ZIP.
