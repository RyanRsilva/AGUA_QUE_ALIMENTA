import pandas as pd
import time
import logging
from sqlalchemy import create_engine
from whatsapp.alerta_whatsapp import enviar_alerta_whatsapp
from whatsapp.alerta_email import enviar_alerta_email
from config.config import BD_URI, SENSORS, INTERVALO_VERIFICACAO, INTERVALO_ALERTA, CLIENTS

logger = logging.getLogger(__name__)

# Conectar ao banco de dados
engine = create_engine(BD_URI)


def iniciar_monitoramento_alerta():
    """
    Verifica os sensores e envia alertas se fora da faixa.
    Tenta WhatsApp primeiro, depois email como fallback.
    """
    ultimo_alerta_enviado = 0
    logger.info("Serviço de monitoramento e alertas iniciado.")

    while True:
        try:
            logger.debug("Iniciando novo ciclo de verificação...")

            # Verificar todos os sensores configurados
            for sensor, limits in SENSORS.items():
                df = pd.read_sql_query(
                    f"SELECT valor FROM leituras WHERE sensor = '{sensor}' ORDER BY data_hora DESC LIMIT 1",
                    con=engine
                )

                if not df.empty:
                    ultimo_valor = df['valor'].iloc[0]
                    logger.debug(
                        f"Último {sensor} lido do banco: {ultimo_valor}")

                    if ultimo_valor < limits['min'] or ultimo_valor > limits['max']:
                        logger.warning(
                            f"Valor fora da faixa detectado: {sensor} = {ultimo_valor}")
                        tempo_atual = time.time()

                        if (tempo_atual - ultimo_alerta_enviado) > INTERVALO_ALERTA:
                            logger.info(
                                "Cooldown permite o envio. Enviando alerta...")

                            # Tentar WhatsApp primeiro
                            numero_admin = CLIENTS.get(
                                'admin', '5511999999999')  # Fallback
                            mensagem = f"ALERTA: {sensor.upper()} fora da faixa! Valor: {ultimo_valor} (faixa: {limits['min']}-{limits['max']})"
                            if not enviar_alerta_whatsapp(numero_admin, mensagem):
                                logger.warning(
                                    "WhatsApp falhou, tentando email...")
                                subject = f"Alerta Sistema Água que Alimenta - {sensor.upper()}"
                                enviar_alerta_email(subject, mensagem)

                            ultimo_alerta_enviado = tempo_atual
                        else:
                            logger.debug("Alerta detectado, mas em cooldown.")
                else:
                    logger.debug(
                        f"Tabela 'leituras' vazia para sensor {sensor}.")

        except Exception as e:
            logger.error(f"Erro no loop de monitoramento: {e}")

        time.sleep(INTERVALO_VERIFICACAO)
