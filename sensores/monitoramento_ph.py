# sensores/monitoramento_ph.py

import sqlite3
import pandas as pd
import time
import os
from whatsapp.alerta_whatsapp import enviar_alerta_whatsapp

# --- CONFIGURAÇÕES GLOBAIS ---
# Todas as configurações agora estão aqui fora, no lugar correto.
FAIXA_MIN_PH = 6.5
FAIXA_MAX_PH = 8.0
INTERVALO_VERIFICACAO = 10  # segundos
INTERVALO_ALERTA = 300      # segundos (5 minutos)

def iniciar_monitoramento_alerta():
    """
    Verifica continuamente o último valor de pH no banco de dados e envia um alerta se estiver fora da faixa.
    """
    ultimo_alerta_enviado = 0
    print("[MONITOR] Serviço de monitoramento e alertas iniciado.")

    while True:
        try:
            caminho_script = os.path.dirname(__file__)
            caminho_db = os.path.abspath(os.path.join(caminho_script, '..', 'banco', 'dados_ph_SQL.db'))
            
            if not os.path.exists(caminho_db):
                time.sleep(5)
                continue

            conn = sqlite3.connect(caminho_db)
            df = pd.read_sql_query("SELECT valor FROM leituras WHERE sensor = 'ph' ORDER BY data_hora DESC LIMIT 1", conn)
            conn.close()

            if not df.empty:
                ultimo_ph = df['valor'].iloc[0]
                
                if ultimo_ph < FAIXA_MIN_PH or ultimo_ph > FAIXA_MAX_PH:
                    tempo_atual = time.time()
                    if (tempo_atual - ultimo_alerta_enviado) > INTERVALO_ALERTA:
                        enviar_alerta_whatsapp(ultimo_ph)
                        ultimo_alerta_enviado = tempo_atual
        except Exception as e:
            print(f"[MONITOR] Erro ao verificar o pH: {e}")

        # A função agora usa a variável INTERVALO_VERIFICACAO que está fora dela
        time.sleep(INTERVALO_VERIFICACAO) 