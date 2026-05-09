import pandas as pd
from sqlalchemy import text
from src.sqlalchemy_engine import engine

with engine.connect() as conn:
    df = pd.read_sql(text("SELECT id, imie, miasto FROM klienci;"), conn)
    df_krakow = pd.read_sql(text("SELECT id, imie, miasto FROM klienci WHERE miasto = :city;"), conn, params={"city": "Krakow"})
    df_a = pd.read_sql(text("SELECT id, imie, miasto FROM klienci WHERE imie LIKE :pattern;"), conn, params={"pattern": "A%"})

df_warszawa = df[df["miasto"] == 'Warszawa']
df_wa_high = df[(df["miasto"] == 'Warszawa') & (df["id"] > 2)]
df_3_cities = df[df["miasto"].isin(["Krakow", "Warszawa", "Gdansk"])]

print(df)
print()
print(df_krakow)
print()
print(df_a)
print()
print(df_warszawa)
print()
print(df_wa_high)
print()
print(df_3_cities)

counts_per_city = df.groupby("miasto").size()
multi_customer_cities = counts_per_city[counts_per_city > 1]
id_stats = df.groupby("miasto")["id"].agg(["min", "max", "count"])

print()
print(counts_per_city)
print()
print(multi_customer_cities)
print()
print(id_stats)

avg_series = df.groupby("miasto")["id"].mean()
print()
print(avg_series)
avg_df = df.groupby("miasto")["id"].agg(["mean"])
print()
print(avg_df)
print(type(avg_series))
print(type(avg_df))

high_avg_cities = avg_series[avg_series > 10]
print()
print(high_avg_cities)

id_summary = df.groupby("miasto")["id"].agg(["min", "max", "mean", "count"])
print()
print(id_summary)

summary = df.groupby("miasto").size().reset_index(name="liczba_klientow")
summary.to_sql("klienci_per_miasto", engine, if_exists="replace", index=False)

with engine.connect() as conn:
    result = pd.read_sql(text("SELECT * FROM klienci_per_miasto;"), conn)

print()
print(result)

df_summary = id_summary.reset_index()
df_summary.to_sql("klienci_id_stats", engine, if_exists="replace", index=False)
with engine.connect() as conn:
    result = pd.read_sql(text("SELECT * FROM klienci_id_stats;"), conn)
print()
print(result)


new_data = pd.DataFrame({
    "miasto":["Wroclaw", "Lodz"],
    "liczba_klientow": [5,3]
})

new_data.to_sql("klienci_per_miasto", engine, if_exists="append", index=False)

with engine.connect() as conn:
    result = pd.read_sql(text("SELECT * FROM klienci_per_miasto;"), conn)

print()
print(result)


with engine.connect() as conn:
    df_all = pd.read_sql(text("SELECT id, imie, miasto FROM klienci;"), conn)

    g_by_city = df_all.groupby("miasto").size()
    customer_high = (g_by_city[g_by_city >= 2]).reset_index(name="liczba_klientow")

    customer_high.to_sql("raport_marketingu", engine, if_exists="replace", index=False)

    result = pd.read_sql(text("SELECT * FROM raport_marketingu;"), conn)

print(result)

# === Drill day 2 - Drill 1 ===
with engine.connect() as conn:
    df = pd.read_sql(text("SELECT id, imie, miasto FROM klienci;"), conn)

stats = df.groupby("miasto")["id"].agg(["count", "min", "max"]).reset_index()
stats_sorted = stats.sort_values("count", ascending=False)
print(stats_sorted)

# === Drill day 2 - Drill 2 ===
df_top = df[df['miasto'].isin(["Krakow", "Warszawa"])]
df_top.to_sql("klienci_top_miasta", engine, if_exists="replace", index=False)

with engine.connect() as conn:
    verify = pd.read_sql(text("SELECT * FROM klienci_top_miasta;"), conn)

print(verify)












