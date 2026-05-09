from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://jaroslawurbanowicz@localhost:5433/sklep"
engine = create_engine(DATABASE_URL)

TEST_DATABASE_URL = "postgresql+psycopg2://jaroslawurbanowicz@localhost:5433/sklep_test"
test_engine = create_engine(TEST_DATABASE_URL)

if __name__ == "__main__":
    name = "Anna"
    email = "anna@example.com"
    with engine.connect() as conn:
        anna_id = conn.execute(text("SELECT id FROM klienci WHERE imie = :name AND email = :email"), {"name": name, "email": email}).fetchone()[0]

        order_id = conn.execute(text("INSERT INTO zamowienia (klient_id, status) VALUES (:id, 'nowe') RETURNING id"), {"id": anna_id}).scalar() #robi to samo co .fetchone()[0]
        position_order = conn.execute(text("INSERT INTO pozycje_zamowienia (zamowienie_id, produkt_id, ilosc, cena_jednostkowa) "
                                           "VALUES (:order_id, 4, 2, 10.50), (:order_id, 5, 1, 25.00)"), {"order_id": order_id})
        conn.commit()
        result = conn.execute(text("SELECT zamowienie_id, produkt_id, ilosc, cena_jednostkowa FROM pozycje_zamowienia"
                                   " WHERE zamowienie_id = :order_id;"), {"order_id": order_id}).fetchall()
        for row in result:
            print(row)



