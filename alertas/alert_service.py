# alert_service.py

import requests
import time
import pandas as pd
from sqlalchemy import create_engine
from whatsapp.alerta_whatsapp import enviar_alerta_whatsapp

# --- CONFIGURAÇÕES ---
DB_PATH = "banco/dados_ph.db"
BD_URI = f'sqlite:///{DB_PATH}'
engine = create_engine(BD_URI)

# Mapa de Dispositivos para Contatos (aqui simulamos o seu cadastro de clientes) ou tenta essa merda 
# no futuro isso vai virar um banco de dados de clientes
CLIENTS = {
    # colcoar os numeros de telefones aqui juntamente do nome do id do ESP
    "nascente_teste_01": "558194330307"

}

FAIXA_MIN_PH = 6.5
FAIXA_MAX_PH = 8.0
INTERVALO_VERIFICACAO = 15  # segundos


def check_alerts():
    print(f"[{time.strftime('%H:%M:%S')}] Vigilante: Verificando alertas...")
    try:
        # Pega a última leitura de CADA dispositivo. (de CADA DISPOSITIVO MEU AMIGO)
        query = """
        SELECT * FROM (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY device_id ORDER BY data_hora DESC) as rn
            FROM leituras
        ) WHERE rn = 1
        """
        df = pd.read_sql(query, con=engine)

        for _, row in df.iterrows():
            device_id = row['device_id']
            ph_valor = row['valor']

            if ph_valor < FAIXA_MIN_PH or ph_valor > FAIXA_MAX_PH:
                print(
                    f"ALERTA! Dispositivo '{device_id}' com pH fora da faixa: {ph_valor}")

                if device_id in CLIENTS:
                    numero_cliente = CLIENTS[device_id]
                    mensagem = f"Alerta no dispositivo '{device_id}': pH atual é {ph_valor}, fora da faixa ideal ({FAIXA_MIN_PH}-{FAIXA_MAX_PH})."
                    # vou precisar adaptar a função para receber número e mensagem
                    enviar_alerta_whatsapp(numero_cliente, mensagem)
                else:
                    print(
                        f"Aviso: Dispositivo '{device_id}' não encontrado no mapa de clientes.")

    except Exception as e:
        print(f"Vigilante: Erro ao verificar dados - {e}")


if __name__ == "__main__":
    while True:
        check_alerts()
        time.sleep(INTERVALO_VERIFICACAO)
