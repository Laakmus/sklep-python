import psycopg2
import pytest
from psycopg2.extras import RealDictCursor
from sqlalchemy import text


def test_database_starts_empty(db_connection):
    """Each test starts with empty database thanks to fixture cleanup."""
    cur = db_connection.cursor()
    cur.execute("SELECT COUNT(*) FROM klienci;")
    count = cur.fetchone()[0]
    cur.close()

    assert count == 0


def test_can_insert_customer(db_connection):
    """Insert a customer and verify it's in the database."""
    cur = db_connection.cursor()
    cur.execute("INSERT INTO klienci (imie, email, miasto) VALUES (%s, %s, %s);", ("Anna", "anna@test.com", "Warszawa"))
    db_connection.commit()

    cur.execute("SELECT COUNT(*) FROM klienci;")
    count = cur.fetchone()[0]
    cur.close()
    assert count == 1


def test_database_isolation(db_connection):
    """
    This test should also start with empty database,
    even though previous test inserted a customer
    """
    cur = db_connection.cursor()
    cur.execute("SELECT COUNT(*) FROM klienci;")
    count = cur.fetchone()[0]
    cur.close()
    assert count == 0

def test_insert_and_select_klient(db_connection):
    # 1. ARRANGE — prepare cursor
    cur = db_connection.cursor()
    # 2. ACT - insert client
    cur.execute("INSERT INTO klienci (imie, email, miasto) VALUES (%s, %s, %s);",
                ("Anna", "anna@test.com", "Warszawa"))
    db_connection.commit()
    # 3. ASSERT - get and check
    cur.execute("SELECT imie, email, miasto FROM klienci;")
    wynik = cur.fetchall()
    assert len(wynik) == 1
    assert wynik[0][0] == "Anna"
    assert wynik[0][1] == "anna@test.com"
    assert wynik[0][2] == "Warszawa"
    cur.close()

def test_insert_and_select_klient_sqlalchemy(db_engine):
    # 1. ARRAGNE - open connection from engine
    with db_engine.connect() as conn:
        # 2. ACT - insert client using prametrized query
        conn.execute(text("INSERT INTO klienci (imie, email, miasto) VALUES (:imie, :email, :miasto);"),
                     {"imie": "Anna", "email": "anna@test.com", "miasto": "Warszawa"})
        conn.commit()
        result = conn.execute(text("SELECT imie, email, miasto FROM klienci;")).fetchall()
        # 3. ASSERT - fetch and check 4 things
        assert len(result) == 1
        assert result[0][0] == "Anna"
        assert result[0][1] == "anna@test.com"
        assert result[0][2] == "Warszawa"



def test_update_klient_email(db_connection):
    """Checking if email is updated correctly."""
    cur = db_connection.cursor()

    cur.execute("INSERT INTO klienci (imie, email, miasto) VALUES (%s, %s, %s);",
                ("Anna", "old@test.com", "Warszawa"))
    cur.execute("UPDATE klienci SET email = %s WHERE imie = %s;", ("new@test.com", "Anna"))
    db_connection.commit()

    cur.execute("SELECT imie, email, miasto FROM klienci;")
    result = cur.fetchall()
    assert result[0][1] == "new@test.com"
    cur.close()

def test_delete_klient(db_connection):
    """Checking if we can delete a klient correctly."""
    cur = db_connection.cursor(cursor_factory=RealDictCursor)
    cur.execute("INSERT INTO klienci (imie, email, miasto) VALUES (%s, %s, %s), (%s, %s, %s);",
                ("Anna", "anna@test.com", "Warszawa", "Tom", "tom@test.com", "Krakow"))
    cur.execute("DELETE FROM klienci WHERE imie = %s;", ("Anna",))
    db_connection.commit()

    cur.execute("SELECT imie FROM klienci;")
    result = cur.fetchall()
    assert len(result) == 1
    assert result[0]["imie"] == "Tom"
    cur.close()

@pytest.mark.parametrize("imie, email, miasto",[
    ("Anna", "anna@test.com", "Warszawa"),
    ("Tom", "tom@test.com", "Krakow"),
    ("Maria", "maria@test.com", "Poznan"),
])
def test_insert_multiple_klients(imie, email, miasto, db_connection):
    cur = db_connection.cursor(cursor_factory=RealDictCursor)
    cur.execute("INSERT INTO klienci (imie, email, miasto) VALUES (%s, %s, %s);", (imie, email, miasto))
    db_connection.commit()
    cur.execute("SELECT imie FROM klienci WHERE imie = %s;", (imie,))
    result = cur.fetchone()
    assert result["imie"] == imie
    cur.close()

@pytest.mark.parametrize("imie, email, miasto", [
    ("Krzysztof", "krzysiek@test.com", "Wrocław"),
])
def test_full_crud_scenario(imie, email, miasto, db_connection):
    cur = db_connection.cursor(cursor_factory=RealDictCursor)
    cur.execute("INSERT INTO klienci (imie, email, miasto) VALUES (%s, %s, %s);", (imie, email, miasto))
    db_connection.commit()
    cur.execute("SELECT email FROM klienci WHERE imie = %s;", (imie,))
    result = cur.fetchone()
    assert result["email"] == email
    cur.execute("UPDATE klienci SET miasto = %s WHERE imie = %s;", ("Łódź", imie))
    db_connection.commit()
    cur.execute("SELECT miasto FROM klienci WHERE imie = %s;", (imie,))
    result = cur.fetchone()
    assert result["miasto"] == "Łódź"
    cur.execute("DELETE FROM klienci WHERE imie = %s;", (imie,))
    db_connection.commit()
    cur.execute("SELECT imie FROM klienci WHERE imie = %s;", (imie,))
    result = cur.fetchone()
    assert result is None
    cur.close()








