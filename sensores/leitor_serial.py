import serial
import pandas as pd
import os
from datetime import datetime
from time import sleep
import random
from sqlalchemy import create_engine

# ==============================================================================
# --- CONFIGURAÇÕES ---
# ==============================================================================
# Garanta que a porta e a velocidade são as mesmas configuradas no seu ESP32
porta_serial = 'COM3'  
baud_rate = 115200  # Velocidade de comunicação

# Caminhos para os arquivos de log e banco de dados
log_dir = 'banco'
csv_file = os.path.join(log_dir, 'historico_ph.csv')
db_path = os.path.join(log_dir, "dados_ph.db")
bd_uri = f'sqlite:///{db_path}'

# Garante que o diretório 'banco' exista
os.makedirs(log_dir, exist_ok=True)

# Conecta ao banco de dados usando SQLAlchemy
try:
    engine = create_engine(bd_uri)
    print("Conexão com o banco de dados SQLite estabelecida.")
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
    exit() # Se não conseguir conectar ao BD, o programa não deve continuar

# ==============================================================================
# --- FUNÇÃO PRINCIPAL ---
# ==============================================================================
def iniciar_leitura_serial():
    """
    Lê o valor de pH da porta serial (ou simula), e salva no arquivo CSV e no banco de dados SQLite.
    """

    # Tenta conectar à porta serial
    try:
        ser = serial.Serial(porta_serial, baud_rate, timeout=2) # Adicionado timeout de 2s
        print(f"Sucesso! Conectado à porta serial {porta_serial}.")
    except serial.SerialException:
        print(f"AVISO: Porta serial {porta_serial} não encontrada. Ativando MODO DE SIMULAÇÃO.")
        ser = None

    print("Iniciando leitura de pH... Pressione CTRL+C para parar.\n")

    # --- Loop Principal de Leitura ---
    try:
        while True:
            linha = None
            if ser and ser.is_open:
                # Lê uma linha da porta serial
                linha_bytes = ser.readline()
                if linha_bytes:
                    linha = linha_bytes.decode('utf-8').strip()
            else:
                # MODO SIMULAÇÃO
                ph_simulado = round(random.uniform(6.5, 7.8), 2)
                # Formato da linha deve ser IDÊNTICO ao que o ESP32 envia
                linha = f"ph_value:{ph_simulado}" 
                print("(Simulação)")
                sleep(2)

            # Processa a linha apenas se ela for válida
            if linha and linha.startswith("ph_value:"):
                try:
                    # 1. Extrai o valor de pH da linha
                    ph_valor = float(linha.split(":")[1].strip())
                    timestamp = datetime.now()
                    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

                    print(f"[{timestamp_str}] Leitura recebida -> pH: {ph_valor}")

                    # 2. Cria um DataFrame para a nova leitura
                    novo_dado_df = pd.DataFrame([[timestamp, ph_valor]], columns=["timestamp", "ph"])

                    # 3. Salva no arquivo CSV (Método robusto e eficiente)
                    # O cabeçalho é escrito automaticamente apenas se o arquivo não existir
                    try:
                        novo_dado_df.to_csv(csv_file, mode='a', index=False, header=not os.path.exists(csv_file))
                    except Exception as e:
                        print(f"### ERRO ao salvar no CSV: {e} ###")

                    # 4. Salva no banco de dados SQLite (Seu método já estava ótimo!)
                    # O formato da tabela ('leituras') é excelente para expansão futura
                    try:
                        novo_dado_sql = pd.DataFrame([[timestamp, 'ph', ph_valor]], columns=["data_hora", "sensor", "valor"])
                        novo_dado_sql.to_sql("leituras", con=engine, if_exists='append', index=False)
                    except Exception as e:
                        print(f"### ERRO ao salvar no Banco de Dados: {e} ###")

                except (ValueError, IndexError) as e:
                    print(f"--> Erro ao processar a linha: '{linha}'. Verifique o formato. | Erro: {e}")

    except KeyboardInterrupt:
        print("\nLeitura finalizada pelo usuário.")
    finally:
        if ser and ser.is_open:
            ser.close()
            print("Porta serial fechada.")

# ==============================================================================
# --- PONTO DE ENTRADA DO SCRIPT ---
# ==============================================================================
if __name__ == '__main__':
    iniciar_leitura_serial()