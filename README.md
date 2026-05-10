# sklep-python

Baza klientów sklepu z operacjami CRUD na PostgreSQL, analizą danych w Pandas oraz testami w pytest. Pokazuje pracę z dwoma stylami dostępu do bazy: niskopoziomowym `psycopg2` oraz `SQLAlchemy` (Core), a także CLI do filtrowania i eksportu danych.

## Stack technologiczny

- **Python 3** + virtualenv (`.venv/`)
- **PostgreSQL** (lokalnie na porcie `5433`, bazy: `sklep` i `sklep_test`)
- **psycopg2-binary** — bezpośrednie zapytania SQL
- **SQLAlchemy 2.0** — engine + `text()` z parametryzacją
- **pandas** — analiza, agregacje, eksport CSV, zapis ramek do bazy (`to_sql`)
- **pytest** — testy jednostkowe i integracyjne z fixturami i parametryzacją

## Struktura projektu

```
sklep-python/
├── cli.py                  # CLI: filtrowanie klientów + eksport CSV (argparse)
├── pandas_demo.py          # Demo Pandas: groupby, filtry, agregacje, to_sql
├── krakow.csv              # Przykładowy eksport
├── requirements.txt
├── src/
│   ├── db.py               # Połączenia psycopg2 (sklep, sklep_test)
│   ├── sqlalchemy_engine.py# Engine SQLAlchemy (sklep, sklep_test) + demo zamówienia
│   ├── models.py           # Klasa domenowa Customer
│   └── validators.py       # is_valid_email, validate_amount, validate_phone_number
├── scripts/                # Skrypty operacyjne (psycopg2)
│   ├── show_clients.py
│   ├── insert_fast.py      # bulk insert przez execute_values
│   ├── insert_slow.py      # insert w pętli (porównanie wydajności)
│   ├── delete_client.py    # DELETE + obsługa ForeignKeyViolation
│   ├── update_client_city.py
│   └── place_order.py      # transakcja: zamówienie + pozycje + update stanu
└── tests/
    ├── conftest.py         # fixtures: sample_customer, db_connection, db_engine
    ├── test_db.py          # CRUD na bazie testowej (psycopg2 + SQLAlchemy)
    ├── test_customer.py
    ├── test_validators.py  # email
    ├── test_amount.py
    └── test_phone.py
```

## Schemat bazy

Projekt pracuje na tabelach: `klienci`, `zamowienia`, `pozycje_zamowienia`, `produkty`, `kategorie` (relacje FK między `zamowienia → klienci`, `pozycje_zamowienia → zamowienia/produkty`).

## Konfiguracja

1. Utwórz i aktywuj wirtualne środowisko:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```
3. Upewnij się, że masz uruchomione PostgreSQL na porcie `5433` z bazami `sklep` oraz `sklep_test`. Konfiguracja połączenia (host, port, user) znajduje się w `src/db.py` i `src/sqlalchemy_engine.py`.

## Usage

```bash
python cli.py --city Krakow --min-id 1
python cli.py --city Krakow --min-id 1 --columns imie email --limit 5
python cli.py --city Krakow --min-id 1 --export krakow.csv
python pandas_demo.py
```

## Uruchamianie

### CLI — filtrowanie klientów

```bash
python cli.py --city Krakow --min-id 1
python cli.py --city Krakow --min-id 1 --columns imie email --limit 5
python cli.py --city Krakow --min-id 1 --export krakow.csv
```

Argumenty:
- `--city` (wymagany) — miasto klienta
- `--min-id` (wymagany) — minimalne id
- `--columns` — lista kolumn do wyświetlenia
- `--limit` — maksymalna liczba wierszy
- `--export` — ścieżka pliku CSV do zapisu

### Demo Pandas

```bash
python pandas_demo.py
```

Pokazuje filtrowanie, `groupby`, agregacje (`min`/`max`/`mean`/`count`) oraz zapis wyników z powrotem do bazy (`klienci_per_miasto`, `klienci_id_stats`, `raport_marketingu`, `klienci_top_miasta`).

### Skrypty operacyjne

```bash
python -m scripts.show_clients
python -m scripts.insert_fast        # bulk insert 5000 klientów (execute_values)
python -m scripts.insert_slow        # ten sam wynik w pętli (benchmark)
python -m scripts.update_client_city # interaktywne (input)
python -m scripts.delete_client      # interaktywne (input)
python -m scripts.place_order        # transakcja zamówienia + update stanu
```

### Testy

```bash
pytest
```

Fixture `db_connection` / `db_engine` z `tests/conftest.py` czyści tabele w bazie `sklep_test` przed każdym testem (kolejność usuwania uwzględnia FK).

## Co projekt pokazuje

- Dwa style dostępu do PostgreSQL (psycopg2 vs SQLAlchemy Core) i parametryzowane zapytania chroniące przed SQL injection
- Obsługa transakcji: `commit` / `rollback`, łapanie `psycopg2.errors.ForeignKeyViolation`
- Bulk insert z `psycopg2.extras.execute_values` (porównanie z naiwną pętlą)
- Integracja Pandas ↔ baza: `read_sql` / `to_sql` (`if_exists="replace"`/`"append"`)
- CLI z `argparse` (wymagane/opcjonalne argumenty, `nargs="+"`, eksport)
- Walidacja danych wejściowych (e-mail, kwota, numer telefonu) z rozróżnieniem `ValueError` / `TypeError`
- Testy: fixtures, parametryzacja (`@pytest.mark.parametrize`), izolacja stanu między testami, pełen scenariusz CRUD
