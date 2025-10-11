import subprocess
import sys


def run_process(command, name):
    print(f"Iniciando {name}...")
    process = subprocess.Popen(command, shell=True)
    return process


def main():
    # Comandos para rodar backend, dashboard e main.py
    backend_cmd = f'"{sys.executable}" -m uvicorn src.backend_server:app --reload'
    dashboard_cmd = f'"{sys.executable}" -m streamlit run src/main/dashboard.py'
    main_cmd = f'"{sys.executable}" -m src.main.main'

    # Inicia backend
    backend_proc = run_process(backend_cmd, "Backend FastAPI")

    # Inicia dashboard
    dashboard_proc = run_process(dashboard_cmd, "Dashboard Streamlit")

    # Inicia main.py (leitura e monitoramento)
    main_proc = run_process(main_cmd, "Main (Leitura e Monitoramento)")

    try:
        # Espera os processos terminarem (normalmente não terminam)
        backend_proc.wait()
        dashboard_proc.wait()
        main_proc.wait()
    except KeyboardInterrupt:
        print("Encerrando todos os processos...")
        backend_proc.terminate()
        dashboard_proc.terminate()
        main_proc.terminate()


if __name__ == "__main__":
    main()


# python banco_geral/run_all.py
