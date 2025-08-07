import pandas as pd
import sqlite3

conn = sqlite3.connect("dados_ph_SQL.db")
df = pd.read_sql_query("SELECT * FROM leituras", conn)
conn.close()

print(df)
