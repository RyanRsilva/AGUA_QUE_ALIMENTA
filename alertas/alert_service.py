import time
import pandas as pd
from sqlalchemy import create_engine
import logging
from config import BD_URI, CLIENTS, FAIXA_MIN_PH, FAIXA_MAX_PH, INTERVALO_VERIFICACAO, INTERVALO_ALERTA
from whatsapp.alerta_whatsapp import enviar_alerta_whatsapp

logger = logging.getLogger(__name__)
engine = create_engine(BD_URI)


def check_alerts():
    """
    Verifica alertas para todos os dispositivos e envia notificações se necessário.
    """
    logger.info("Verificando alertas...")
    ultimo_alerta_enviado = {}  # Para controlar cooldown por dispositivo

    try:
        # Pega a última leitura de CADA dispositivo
        query = """
        SELECT * FROM (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY device_id ORDER BY data_hora DESC) as rn
            FROM leituras
        ) WHERE rn = 1
        """
        df = pd.read_sql(query, con=engine)

        if df.empty:
            logger.info("Nenhuma leitura encontrada.")
            return

        for _, row in df.iterrows():
            device_id = row['device_id']
            ph_valor = row['valor']
            timestamp = row['data_hora']

            if ph_valor < FAIXA_MIN_PH or ph_valor > FAIXA_MAX_PH:
                logger.warning(
                    f"ALERTA! Dispositivo '{device_id}' com pH fora da faixa: {ph_valor}")

                tempo_atual = time.time()
                if device_id not in ultimo_alerta_enviado or (tempo_atual - ultimo_alerta_enviado[device_id]) > INTERVALO_ALERTA:
                    if device_id in CLIENTS:
                        numero_cliente = CLIENTS[device_id]
                        mensagem = f"Alerta no dispositivo '{device_id}': pH atual é {ph_valor:.2f}, fora da faixa ideal ({FAIXA_MIN_PH}-{FAIXA_MAX_PH}). Timestamp: {timestamp}"
                        if enviar_alerta_whatsapp(numero_cliente, mensagem):
                            ultimo_alerta_enviado[device_id] = tempo_atual
                            logger.info(
                                f"Notificação enviada para {numero_cliente}")
                        else:
                            logger.error(
                                f"Falha ao enviar notificação para {numero_cliente}")
                    else:
                        logger.warning(
                            f"Dispositivo '{device_id}' não encontrado no mapa de clientes.")
                else:
                    logger.debug(
                        f"Alerta em cooldown para dispositivo '{device_id}'")

    except Exception as e:
        logger.error(f"Erro ao verificar alertas: {e}")


def iniciar_monitoramento_alerta():
    """
    Inicia o monitoramento contínuo de alertas.
    """
    logger.info("Serviço de monitoramento e alertas iniciado.")
    while True:
        check_alerts()
        time.sleep(INTERVALO_VERIFICACAO)


if __name__ == "__main__":
    iniciar_monitoramento_alerta()
