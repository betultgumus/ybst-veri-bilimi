import sqlite3
import pandas as pd
from src.config import DB_PATH


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def write_df_to_table(df: pd.DataFrame, table_name: str, if_exists: str = "replace"):
    conn = get_connection()
    df.to_sql(table_name, conn, if_exists=if_exists, index=False)
    conn.close()


def read_table(table_name: str) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query(f'SELECT * FROM "{table_name}"', conn)
    conn.close()
    return df


def list_tables():
    conn = get_connection()
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    tables = pd.read_sql_query(query, conn)
    conn.close()
    return tables