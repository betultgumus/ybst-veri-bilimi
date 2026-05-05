import pandas as pd

from src.config import (
    COMMENTS_CSV_PATH,
    PRODUCTS_CSV_PATH,
    RAW_COMPLAINTS_TABLE,
    RAW_PRODUCTS_TABLE
)
from src.database import write_df_to_table, list_tables


def read_csv_safely(path):
    encodings = ["utf-8-sig", "utf-8", "cp1254", "latin1"]

    last_error = None

    for enc in encodings:
        try:
            df = pd.read_csv(path, encoding=enc, sep=None, engine="python")
            df.columns = [str(col).strip() for col in df.columns]
            return df
        except Exception as e:
            last_error = e

    raise last_error


def load_raw_data():
    comments_df = read_csv_safely(COMMENTS_CSV_PATH)
    products_df = read_csv_safely(PRODUCTS_CSV_PATH)

    write_df_to_table(comments_df, RAW_COMPLAINTS_TABLE)
    write_df_to_table(products_df, RAW_PRODUCTS_TABLE)

    print("Ham CSV dosyaları SQLite'a aktarıldı.")
    print(f"Şikayet tablosu satır/sütun: {comments_df.shape}")
    print(f"Ürün tablosu satır/sütun: {products_df.shape}")

    print("\nSQLite tabloları:")
    print(list_tables())


if __name__ == "__main__":
    load_raw_data()