from src.db import connect

conn = connect()

client_id = int(input("ID: "))
new_city = input("New city: ")

if not new_city.strip():
    print("Error: city cannot be empty")
    exit(1)

try:
    with conn.cursor() as cur:
        cur.execute("UPDATE klienci SET miasto = %s WHERE id = %s;", (new_city, client_id))
        if cur.rowcount == 0:
            print(f"Customer with id={client_id} not found")
        elif cur.rowcount == 1:
            print(f"Updated city to {new_city} for client with id={client_id}")
        else:
            print(f"WARNING: actualized {cur.rowcount} rows!")
        conn.commit()
finally:
    conn.close()