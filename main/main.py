import sys
import os
import threading
import time

# Adiciona a raiz do projeto ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sensores.leitor_serial import iniciar_leitura_serial
from whatsapp.alerta_whatsapp import iniciar_monitoramento_alerta

def main():
    # Thread 1 - Leitura e gravação de dados
    t1 = threading.Thread(target=iniciar_leitura_serial, daemon=True)

    # Thread 2 - Monitoramento de pH e alerta
    t2 = threading.Thread(target=iniciar_monitoramento_alerta, daemon=True)

    print("🚀 Sistema iniciado. Pressione CTRL+C para sair.\n")

    t1.start()
    t2.start()

    try:
        while True:
            time.sleep(1)  # Mantém o main rodando
    except KeyboardInterrupt:
        print("\n🛑 Sistema encerrado.")

if __name__ == "__main__":
    main()


#  =======  sistema  =======

# para rodar o sistema, execute: python -m main.main

# para rodar o dashboard, execute: streamlit run main/dashboard.py

# para rodar o alerta WhatsApp, execute: python whatsapp/alerta_whatsapp.py