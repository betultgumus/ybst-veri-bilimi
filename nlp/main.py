import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

df = pd.read_csv("data/raw/beko_urun_ozellikleri.csv")
print(df.info())
