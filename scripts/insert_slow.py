from src.db import connect
import time


clients = [(f"Test_{i}",f"bench_{i}@test.com", f"City_{i}") for i in range(5000)]

conn = connect()

try:
    with conn.cursor() as cur:
        start = time.time()
        for client in clients:
            cur.execute("INSERT INTO klienci (imie, email, miasto) VALUES (%s, %s, %s);", (client[0], client[1], client[2]))
        conn.commit()
        end = time.time()
        print(f"Inserted 5000 clients in {round(end - start, 2)} seconds")
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    conn.close()





