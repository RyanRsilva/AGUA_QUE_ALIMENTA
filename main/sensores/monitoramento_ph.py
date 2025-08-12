# sensores/monitoramento_ph.py

import sqlite3
import pandas as pd
import time
import os
# from whatsapp.alerta_whatsapp import enviar_alerta_whatsapp

# --- CONFIGURAÇÕES ---
FAIXA_MIN_PH = 6.5
FAIXA_MAX_PH = 8.0
INTERVALO_VERIFICACAO = 10  # segundos - verifica o banco de dados a cada 10s
# segundos - só envia um novo alerta a cada 5 minutos para não haver spam
INTERVALO_ALERTA = 300


def iniciar_monitoramento_alerta():
    """
    Verifica continuamente o último valor de pH no banco de dados e envia um alerta se estiver fora da faixa.
    """
    ultimo_alerta_enviado = 0
    print("[MONITOR] Serviço de monitoramento e alertas iniciado.")

    while True:
        try:
            # Constrói o caminho absoluto para o banco de dados (mesma lógica do dashboard)
            caminho_script = os.path.dirname(__file__)
            caminho_db = os.path.abspath(os.path.join(
                caminho_script, '..', 'banco', 'dados_ph_SQL.db'))

            conn = sqlite3.connect(caminho_db)
            # Pega apenas a última leitura do banco de dados
            df = pd.read_sql_query(
                "SELECT valor FROM leituras WHERE sensor = 'ph' ORDER BY data_hora DESC LIMIT 1", conn)
            conn.close()

            if not df.empty:
                ultimo_ph = df['valor'].iloc[0]

                # Verifica se o pH está fora da faixa ideal
                if ultimo_ph < FAIXA_MIN_PH or ultimo_ph > FAIXA_MAX_PH:
                    tempo_atual = time.time()
                    # Verifica se já passou tempo suficiente desde o último alerta (evita spam)
                    if (tempo_atual - ultimo_alerta_enviado) > INTERVALO_ALERTA:
                        #                        enviar_alerta_whatsapp(ultimo_ph)
                        # Adicionei este print para teste
                        print(
                            f"### ALERTA DE PH DETECTADO (TESTE): {ultimo_ph} ###")
                        ultimo_alerta_enviado = tempo_atual  # Atualiza o tempo do último alerta

        except Exception as e:
            print(f"[MONITOR] Erro ao verificar o pH: {e}")

        # Aguarda antes da próxima verificação
        time.sleep(INTERVALO_VERIFICACAO)
