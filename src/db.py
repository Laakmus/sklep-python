import psycopg2

DB_HOST = "localhost"
DB_PORT = 5433
DB_NAME = "sklep"
DB_USER = "jaroslawurbanowicz"
DB_PASSWORD = ""

TEST_DB_NAME = "sklep_test"

def connect():
    """Connect to the 'sklep' and return a connection object."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def connect_test():
    """Connect to the test 'sklep_test' database."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=TEST_DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )