# main/main.py

import threading
import time


from sensores.leitor_serial import iniciar_leitura_serial
from sensores.monitoramento_ph import iniciar_monitoramento_alerta


def main():
    t1 = threading.Thread(target=iniciar_leitura_serial, daemon=True)
    t2 = threading.Thread(target=iniciar_monitoramento_alerta, daemon=True)

    print("🚀 Sistema iniciado. Pressione CTRL+C para sair.\n")

    t1.start()
    time.sleep(2)  # Pausa para garantir que a thread serial comece primeiro
    t2.start()

    try:
        while t1.is_alive() and t2.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Sistema encerrado pelo usuário.")
    finally:
        print("Finalizando...")


if __name__ == "__main__":
    main()


# ativar venv : .\.venv\Scripts\Activate.ps1

# ativar main : python -m main.main

# ativa o backand.py: python main/backend_server.py

# ativar dashboard: streamlit run main/dashboard.py

# ativar o zapzap : whatsapp/alerta_whatsapp.py 