import argparse
from sqlalchemy import text
from src.sqlalchemy_engine import engine
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Filter and display customers from database with optional CSV export",
                                     epilog="Example: python cli.py --city Wolkowysk --min-id 3 --columns imie email --limit 1 ")
    parser.add_argument("--city", type=str, required=True, help="City name")
    parser.add_argument("--min-id", type=int, required=True, help="Minimum id")
    parser.add_argument("--export", type=str, default=None, help="Export to csv")
    parser.add_argument("--limit", type=int, default=None, help="Limit the number of rows")
    parser.add_argument("--columns", type=str, nargs="+", default=None, help="Column names")
    args = parser.parse_args()



    with engine.connect() as conn:
        df = pd.read_sql(text("SELECT id, imie, miasto, email FROM klienci;"), conn)

    df_filtered = df[(df["miasto"] == args.city) & (df["id"] >= args.min_id)]
    if args.columns is not None:
        df_filtered = df_filtered[args.columns]
    if args.limit is not None:
        df_filtered = df_filtered.head(args.limit)
    if args.export is not None:
        df_filtered.to_csv(args.export, index=False)
        print(f"Saved to {args.export}")
    print(df_filtered)



if __name__ == "__main__":
    main()