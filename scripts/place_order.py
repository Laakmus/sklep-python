from src.db import connect
from psycopg2.extras import RealDictCursor

conn = connect()

client_id = 1
items = [(2,1), (3,2),] # 1 produkt_id, 2 ilosc

try:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("INSERT INTO zamowienia (klient_id, status) VALUES (%s, 'nowe') RETURNING id;", (client_id,))
        order_id = cur.fetchone()['id']

        for produkt_id, ilosc in items:
            cur.execute("SELECT cena FROM produkty WHERE id = %s;", (produkt_id,))
            cena = cur.fetchone()['cena']
            cur.execute("INSERT INTO pozycje_zamowienia (zamowienie_id, produkt_id, ilosc, cena_jednostkowa) VALUES (%s, %s, %s, %s);",
                        (order_id, produkt_id, ilosc, cena))
            cur.execute("UPDATE produkty SET stan_magazynowy = stan_magazynowy - %s WHERE id = %s;", (ilosc, produkt_id))
        conn.commit()

        print(f"Order #{order_id} placed successfully")


except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    conn.close()