import sqlite3

conn = sqlite3.connect("dados_ph_SQL.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()

print("Tabelas no banco:", tabelas)


#        VERIFICAR OS ITENS QUE TEM NAS COLUNAS

conn = sqlite3.connect("dados_ph_SQL.db")
cursor = conn.cursor()

# Mostra as colunas
cursor.execute("PRAGMA table_info(leituras_ph);")
colunas = cursor.fetchall()
print("Colunas:", colunas)

conn.close()
