# whatsapp/alerta_whatsapp.py

import requests
import logging
from urllib.parse import quote
from ..config.settings import MINHA_APIKEY

logger = logging.getLogger(__name__)


def enviar_alerta_whatsapp(numero_destino, mensagem):
    """
    Envia uma mensagem de alerta via CallMeBot API.
    """
    if not MINHA_APIKEY:
        logger.error(
            "API Key do CallMeBot não configurada. Verifique o arquivo .env.")
        return False

    if not numero_destino or not mensagem:
        logger.error("Número de destino ou mensagem não fornecidos.")
        return False

    try:
        url = f"https://api.callmebot.com/whatsapp.php?phone={numero_destino}&text={quote(mensagem)}&apikey={MINHA_APIKEY}"
        logger.info(
            f"Enviando alerta para o número {numero_destino} via CallMeBot...")

        response = requests.get(url)

        if response.status_code == 200:
            logger.info("Alerta enviado com sucesso pelo CallMeBot.")
            return True
        else:
            logger.error(
                f"Erro ao enviar alerta pelo CallMeBot. Código: {response.status_code}, Resposta: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        logger.error(
            f"Falha na conexão ao tentar enviar alerta pelo CallMeBot: {e}")
        return False
