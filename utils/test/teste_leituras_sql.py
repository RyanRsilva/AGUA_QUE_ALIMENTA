import sqlite3

# Conectar ao banco (vai criar se não existir)
conn = sqlite3.connect("banco/dados_ph_SQL.db")
cursor = conn.cursor()

# Criar a tabela (se não existir)
cursor.execute('''
CREATE TABLE IF NOT EXISTS leituras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor TEXT,
    valor REAL,
    data_hora TEXT
)
''')

# Inserir um exemplo de leitura
cursor.execute('''
INSERT INTO leituras (sensor, valor, data_hora)
VALUES ('ph', 7.2, datetime('now'))
''')

# Salvar e consultar os dados
conn.commit()
cursor.execute("SELECT * FROM leituras_ph")
dados = cursor.fetchall()

# Mostrar os dados
for linha in dados:
    print(linha)

# Fechar conexão
conn.close()
