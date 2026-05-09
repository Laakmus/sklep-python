from src.db import connect
from psycopg2.extras import RealDictCursor

conn = connect()
try:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM klienci ORDER BY id ASC;")
        results = cur.fetchall()

        for klient in results:
            print(f"ID: {klient['id']} | {klient['imie']} | {klient['email']} | {klient['miasto']}")
finally:
    conn.close()
