import serial
import requests
import logging
from time import sleep
import random
from datetime import datetime

# ==============================================================================
# --- CONFIGURAÇÕES ---
# ==============================================================================

from ..config.settings import PORTA_SERIAL, BAUD_RATE, API_BASE_URL

# Configuração de logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Endpoint da API para enviar os dados
API_ENDPOINT = f"{API_BASE_URL}/data"
DEVICE_ID = "esp32_leitor_serial"  # ID deste dispositivo/script

# ==============================================================================
# --- FUNÇÃO PRINCIPAL ---
# ==============================================================================


def iniciar_leitura_serial():
    """
    Lê o valor de pH da porta serial (ou simula) e envia para a API do backend_server.
    """

    # Tenta conectar à porta serial
    try:
        ser = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=2)
        logger.info(f"Sucesso! Conectado à porta serial {PORTA_SERIAL}.")
    except serial.SerialException:
        logger.warning(
            f"Porta serial {PORTA_SERIAL} não encontrada. Ativando MODO DE SIMULAÇÃO.")
        ser = None

    logger.info("Iniciando leitura de pH... Pressione CTRL+C para parar.")

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
                ph_simulado = round(random.uniform(3.5, 9.8), 2)
                linha = f"ph_value:{ph_simulado}"
                logger.info(f"(Simulação) Gerado valor de pH: {ph_simulado}")
                sleep(5)  # Em modo de simulação, espera 5 segundos

            # Processa a linha apenas se ela for válida
            if linha and linha.startswith("ph_value:"):
                try:
                    ph_valor = float(linha.split(":")[1].strip())
                    logger.info(f"Leitura recebida -> pH: {ph_valor}")

                    # Monta o payload para enviar à API
                    payload = {
                        "device_id": DEVICE_ID,
                        "sensor": "ph",
                        "value": ph_valor
                    }

                    # Envia os dados para a API
                    try:
                        response = requests.post(
                            API_ENDPOINT, json=payload, timeout=10)
                        response.raise_for_status()  # Lança exceção para status 4xx/5xx
                        logger.info(
                            f"Dados enviados para API com sucesso: {payload}")

                    except requests.exceptions.RequestException as e:
                        logger.error(f"Erro ao enviar dados para a API: {e}")

                except (ValueError, IndexError) as e:
                    logger.error(
                        f"Erro ao processar a linha: '{linha}'. Verifique o formato. | Erro: {e}")

            sleep(1)  # Pequena pausa no loop principal

    except KeyboardInterrupt:
        logger.info("Leitura finalizada pelo usuário.")
    finally:
        if ser and ser.is_open:
            ser.close()
            logger.info("Porta serial fechada.")


# ==============================================================================
# --- PONTO DE ENTRADA DO SCRIPT ---
# ==============================================================================
if __name__ == '__main__':
    iniciar_leitura_serial()
