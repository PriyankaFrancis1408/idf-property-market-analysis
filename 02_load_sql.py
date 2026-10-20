import pandas as pd
import sqlite3

df = pd.read_csv("dvf_clean_idf_2025.csv")

con = sqlite3.connect("dvf.db")
df.to_sql("sales", con, if_exists="replace", index=False)

print(pd.read_sql("SELECT COUNT(*) AS n_sales FROM sales", con))
con.close()