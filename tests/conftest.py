import pytest
from src.models import Customer
from src.db import connect_test
from src.sqlalchemy_engine import test_engine
from sqlalchemy import text


@pytest.fixture
def sample_customer():
    """Returns a fresh Customer instance for each test."""
    return Customer("Anna", "anna@test.com", "Warszawa")


@pytest.fixture
def db_connection():
    """
    Provides a clean test database connection.
    Cleans all data BEFORE each test.
    Closes connection AFTER each test.
    """
    # SETUP: open connection and clean data
    conn = connect_test()
    cur = conn.cursor()

    # Clean tables in correct order (children before parents - FK constraints!)
    cur.execute("DELETE FROM pozycje_zamowienia;")
    cur.execute("DELETE FROM zamowienia;")
    cur.execute("DELETE FROM klienci;")
    cur.execute("DELETE FROM produkty;")
    cur.execute("DELETE FROM kategorie;")
    conn.commit()
    cur.close()

    # GIVE connection to the test
    yield conn

    # TEARDOWN: close connection
    conn.close()


@pytest.fixture
def db_engine():
    """Provides SQLAlchemy engine for sklep_test, with cleanup BEFORE each test."""
    with test_engine.connect() as conn:
        conn.execute(text("DELETE FROM pozycje_zamowienia;"))
        conn.execute(text("DELETE FROM zamowienia;"))
        conn.execute(text("DELETE FROM klienci;"))
        conn.execute(text("DELETE FROM produkty;"))
        conn.execute(text("DELETE FROM kategorie;"))
        conn.commit()

    yield test_engine











