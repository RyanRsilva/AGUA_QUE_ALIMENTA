# sensores/monitoramento_ph.py

import sqlite3
import pandas as pd
import time
import os
from whatsapp.alerta_whatsapp import enviar_alerta_whatsapp

# --- CONFIGURAÇÕES GLOBAIS ---
FAIXA_MIN_PH = 6.5
FAIXA_MAX_PH = 8.0
INTERVALO_VERIFICACAO = 10  # A cada 10 segundos
INTERVALO_ALERTA = 20       # A cada 20 segundos para teste


def iniciar_monitoramento_alerta():
    """
    (VERSÃO DE DIAGNÓSTICO) Verifica o pH e imprime cada passo que executa.
    """
    ultimo_alerta_enviado = 0
    print("[MONITOR] Serviço de monitoramento e alertas iniciado.")

    while True:
        try:
            # --- DEBUG PRINT 1 ---
            print("\n[MONITOR] Inciando novo ciclo de verificação...")

            caminho_script = os.path.dirname(__file__)
            caminho_db = os.path.abspath(os.path.join(
                caminho_script, '..', 'banco', 'dados_ph.db'))

            if not os.path.exists(caminho_db):
                print("[MONITOR] Banco de dados ainda não encontrado. Aguardando...")
                time.sleep(5)
                continue

            conn = sqlite3.connect(caminho_db)
            df = pd.read_sql_query(
                "SELECT valor FROM leituras WHERE sensor = 'ph' ORDER BY data_hora DESC LIMIT 1", conn)
            conn.close()

            if not df.empty:
                ultimo_ph = df['valor'].iloc[0]
                # --- DEBUG PRINT 2 ---
                print(f"[MONITOR] Último pH lido do banco: {ultimo_ph}")

                if ultimo_ph < FAIXA_MIN_PH or ultimo_ph > FAIXA_MAX_PH:
                    # --- DEBUG PRINT 3 ---
                    print(
                        f">>> [MONITOR] VALOR FORA DA FAIXA DETECTADO: {ultimo_ph}")
                    tempo_atual = time.time()

                    if (tempo_atual - ultimo_alerta_enviado) > INTERVALO_ALERTA:
                        # --- DEBUG PRINT 4 ---
                        print(
                            ">>> [MONITOR] Cooldown permite o envio. CHAMANDO A FUNÇÃO DE ALERTA!")
                        enviar_alerta_whatsapp(ultimo_ph)
                        ultimo_alerta_enviado = tempo_atual
                    else:
                        # --- DEBUG PRINT 5 ---
                        print(
                            ">>> [MONITOR] Alerta detectado, mas estou em cooldown. Aguardando...")

            else:
                print("[MONITOR] Tabela 'leituras' está vazia. Aguardando dados...")

        except Exception as e:
            print(f"!!! [MONITOR] OCORREU UM ERRO NO LOOP: {e} !!!")

        time.sleep(INTERVALO_VERIFICACAO)
