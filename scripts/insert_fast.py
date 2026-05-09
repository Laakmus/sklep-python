from psycopg2.extras import execute_values
from src.db import connect
import time

clients = [(f"Test_{i}",f"bench_{i}@test.com", f"City_{i}") for i in range(5000)]

conn = connect()

try:
    with conn.cursor() as cur:
        start = time.time()
        execute_values(cur, "INSERT INTO klienci (imie, email, miasto) VALUES %s;", clients)
        conn.commit()
        end = time.time()
        print(f"Inserted 5000 clients in {round(end - start, 2)} seconds")
except Exception as e:
    print(e)
    conn.rollback()
finally:
    conn.close()