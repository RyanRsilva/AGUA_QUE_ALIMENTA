# whatsapp/alerta_whatsapp.py

import requests
import urllib.parse

import logging
from config.config import MINHA_APIKEY

logger = logging.getLogger(__name__)


def enviar_alerta_whatsapp(numero_destino, mensagem):
    """
    Envia uma MENSAGEM específica para um NÚMERO DE TELEFONE específico.
    """
    if not MINHA_APIKEY or MINHA_APIKEY == "SUA_CHAVE_APIKEY_AQUI":
        logger.error("APIKEY não configurada")
        return False

    if not numero_destino or not mensagem:
        logger.error("Número de destino ou mensagem não fornecidos")
        return False

    mensagem_formatada = urllib.parse.quote(mensagem)
    url = f"https://api.callmebot.com/whatsapp.php?phone={numero_destino}&text={mensagem_formatada}&apikey={MINHA_APIKEY}"

    logger.info(f"Enviando notificação para o número {numero_destino}")

    try:
        response = requests.get(url)
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
