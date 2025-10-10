# -*- coding: utf-8 -*-
"""
Este é o script principal que gerencia o sistema de monitoramento de água.

O sistema é composto por vários componentes que podem ser executados de forma independente
ou orquestrados para uma simulação completa.

--------------------------------------------------------------------------------
COMO EXECUTAR O PROJETO COMPLETO (EM TERMINAIS SEPARADOS):
--------------------------------------------------------------------------------

1. INICIAR O SERVIDOR BACKEND (API):
    - O servidor FastAPI recebe os dados dos sensores e os armazena.
    - Comando:
        python -m uvicorn src.backend_server:app --reload
        tem que esta dentro do src:
            cd src /uvicorn backend_server:app --reload

2. INICIAR O DASHBOARD DE VISUALIZAÇÃO:
    - O Streamlit consome os dados da API e os exibe em tempo real.
    - Comando:
        python -m streamlit run src/main/dashboard.py

3. (OPCIONAL) INICIAR O SIMULADOR DE SENSOR ESP32:
    - Envia dados falsos para o backend, útil para testes sem hardware.
    - Comando:
        python simulate_esp32.py

4. EXECUTAR ESTE SCRIPT (main.py):
    - Este script inicia a leitura da porta serial (se houver um dispositivo real)
        e o sistema de monitoramento de alertas (que verifica os dados no banco).
    - Comando:
        python -m src.main.main

--------------------------------------------------------------------------------
"""
import threading
import time
import logging
from src.sensores.leitor_serial import iniciar_leitura_serial
from src.alertas.alert_service import iniciar_monitoramento_alerta

# Configurar logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """
    Função principal que inicia as threads para leitura serial e monitoramento de alertas.
    """

    # Thread para ler dados da porta serial (do hardware real)
    thread_leitura_serial = threading.Thread(target=iniciar_leitura_serial, daemon=True)

    # Thread para monitorar o banco de dados e enviar alertas
    thread_monitoramento_alertas = threading.Thread(target=iniciar_monitoramento_alerta, daemon=True)

    thread_leitura_serial.start()
    logger.info("Thread de leitura da porta serial iniciada.")

    time.sleep(2)  # Pequena pausa para garantir que a leitura serial comece primeiro

    thread_monitoramento_alertas.start()
    logger.info("Thread de monitoramento de alertas iniciada.")

    logger.info("Sistema em execução. Pressione CTRL+C para encerrar.")
    try:
        # Mantém o script principal vivo enquanto as threads estiverem ativas
        while thread_leitura_serial.is_alive() and thread_monitoramento_alertas.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Encerrando o sistema a pedido do usuário (CTRL+C).")
    finally:
        logger.info("Finalizando threads...")

if __name__ == "__main__":
    main()
