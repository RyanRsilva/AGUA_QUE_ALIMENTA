import threading
import time
import logging
from sensores.leitor_serial import iniciar_leitura_serial
from alertas.alert_service import iniciar_monitoramento_alerta

# Configurar logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    logger.info("Iniciando sistema de monitoramento de qualidade da água")

    t1 = threading.Thread(target=iniciar_leitura_serial, daemon=True)
    t2 = threading.Thread(target=iniciar_monitoramento_alerta, daemon=True)

    logger.info("Sistema iniciado. Pressione CTRL+C para sair.")

    t1.start()
    time.sleep(2)  # Pausa para garantir que a thread serial comece primeiro
    t2.start()

    try:
        while t1.is_alive() and t2.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Sistema encerrado pelo usuário.")
    finally:
        logger.info("Finalizando...")


if __name__ == "__main__":
    main()
