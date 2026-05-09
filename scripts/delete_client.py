import psycopg2
from src.db import connect

conn = connect()

client_id = int(input("Client ID: "))
if client_id < 0:
    print("Error: invalid client ID")
    exit(1)

try:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM klienci WHERE id = %s;", (client_id,))
        if cur.rowcount == 0:
            print(f"Customer with id={client_id} not deleted")
        elif cur.rowcount == 1:
            print(f"Customer {client_id} deleted successfully")
        else:
            print(f"WARNING: deleted {cur.rowcount} rows!")
        conn.commit()
except psycopg2.errors.ForeignKeyViolation as e:
    print(f"Cannot delete: customer {client_id} has orders")
    conn.rollback()
except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
finally:
    conn.close()
