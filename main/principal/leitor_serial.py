import serial
import pandas as pd
import os
from datetime import datetime
from time import sleep
import random
from sqlalchemy import create_engine

# ====== CONFIG ======
porta_serial = 'COM3'  # muda aqui quando estivermos com o ESP32
baud_rate = 115200
excel_file = 'dados_ph_excel.xlsx'
bd_file = "sqlite:///dados_ph_SQL.db"

#  CRIA EXCEL SE NÃO EXISTIR  ( eu acho kkk)
if not os.path.exists(excel_file):
    df_inicial = pd.DataFrame(columns=["timestamp", "ph"])
    df_inicial.to_excel(excel_file, index=False)

#  TENTA CONECTAR AO BANCO 
engine = create_engine(bd_file)

# CONECTA À SERIAL (OU TENTA SIMULA ESSA BAGAÇA) 
try:

    ser = serial.Serial(porta_serial, baud_rate)
    print("Conectado à serial.")

except serial.SerialException:
    print(f"Erro: Porta {porta_serial} não encontrada. Modo SIMULAÇÃO ativado.")
    ser = None

print("Iniciando leitura de pH... Pressione CTRL+C para parar.\n")

# ====== LOOP PRINCIPAL ======
try:
    while True:
        if ser:
            linha = ser.readline().decode().strip()
        else:
            ph_simulado = round(random.uniform(5.5, 8.4), 2)
            linha = f"pH: {ph_simulado}"
            sleep(3)

        if linha.startswith("pH:"):
            try:
                ph_valor = float(linha.split(":")[1].strip())
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Cria o dataframe da leitura
                novo_dado = pd.DataFrame([[timestamp, ph_valor]], columns=["timestamp", "ph"])

                # Salva no Excel
                with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                    novo_dado.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)

                # Salva no banco SQLite
                novo_dado.to_sql("leituras_ph", con=engine, if_exists='append', index=False)

                print(f"[{timestamp}] pH: {ph_valor}")
            except Exception as e:
                print(f"Erro ao processar linha: {linha} | Erro: {e}")

except KeyboardInterrupt:
    print("\nLeitura finalizada pelo usuário.")
finally:
    if ser:
        ser.close()
