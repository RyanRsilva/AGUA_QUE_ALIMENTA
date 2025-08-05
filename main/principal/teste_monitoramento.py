import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from openpyxl import load_workbook
import os

excel_file = 'dados_ph_excel.xlsx'
db_file = "dados_ph_SQL.db"
sheet_name = 'leituras_ph'

# Cria arquivo Excel se não existir
if not os.path.exists(excel_file):
    df = pd.DataFrame(columns=['pH', 'Temperatura', 'Turbidez'])
    df.to_excel(excel_file, index=False, sheet_name=sheet_name)

# Cria banco de dados se não existir

conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS dados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ph REAL,
        temperatura REAL,
        turbidez REAL
    )
''')
conn.commit()

print("Pressione Ctrl+C para sair.\n")

try:
    while True:
        # Entrada de dados
        ph = float(input("Digite o valor de pH: "))
        temp = float(input("Digite a temperatura: "))
        turb = float(input("Digite a turbidez: "))

        # Novo dado
        novo_dado = pd.DataFrame([{
            'pH': ph,
            'Temperatura': temp,
            'Turbidez': turb
        }])

        # Adiciona ao Excel
        book = load_workbook(excel_file)
        writer = pd.ExcelWriter(excel_file, engine='openpyxl')
        writer.book = book
        writer.sheets = {ws.title: ws for ws in book.worksheets}
        reader = pd.read_excel(excel_file, sheet_name=sheet_name)
        final_df = pd.concat([reader, novo_dado], ignore_index=True)
        final_df.to_excel(writer, sheet_name=sheet_name, index=False)
        writer.close()

        # Adiciona ao banco
        cursor.execute("INSERT INTO dados (ph, temperatura, turbidez) VALUES (?, ?, ?)",
                    (ph, temp, turb))
        conn.commit()

        # Gera gráfico atualizado
        df = pd.read_sql_query("SELECT * FROM dados", conn)
        plt.figure(figsize=(10, 5))
        plt.plot(df['id'], df['ph'], label='pH')
        plt.plot(df['id'], df['temperatura'], label='Temperatura')
        plt.plot(df['id'], df['turbidez'], label='Turbidez')
        plt.xlabel('Leitura')
        plt.ylabel('Valor')
        plt.title('Monitoramento de Qualidade da Água')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

except KeyboardInterrupt:
    print("\nEncerrado pelo usuário.")

finally:
    conn.close()
