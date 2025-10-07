# whatsapp/alerta_whatsapp.py

import requests
import logging
from config.config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE

logger = logging.getLogger(__name__)


def enviar_alerta_whatsapp(numero_destino, mensagem):
    """
    Envia uma mensagem via Evolution API.
    """
    if not EVOLUTION_API_URL or not EVOLUTION_API_KEY or not EVOLUTION_INSTANCE:
        logger.error("Configuração da Evolution API não encontrada")
        return False

    if not numero_destino or not mensagem:
        logger.error("Número de destino ou mensagem não fornecidos")
        return False

    url = f"{EVOLUTION_API_URL}/message/sendText/{EVOLUTION_INSTANCE}"
    headers = {
        "Content-Type": "application/json",
        "apikey": EVOLUTION_API_KEY
    }
    data = {
        "number": numero_destino,
        "text": mensagem
    }

    logger.info(f"Enviando notificação para o número {numero_destino}")

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            logger.info("Notificação enviada com sucesso")
            return True
        else:
            logger.error(
                f"Erro ao enviar. Código: {response.status_code}, Resposta: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Falha de conexão: {e}")
        return False


# --- Bloco de Teste ---
if __name__ == '__main__':
    print("--- Testando o módulo de alerta do WhatsApp ---")
    numero_teste = "55SEUNUMEROAQUI"
    mensagem_teste = "Olá! Este é um teste do sistema de alertas dinâmico. Kronnos."
    enviar_alerta_whatsapp(numero_teste, mensagem_teste)
