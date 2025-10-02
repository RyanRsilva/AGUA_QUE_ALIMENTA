import os
from dotenv import load_dotenv

load_dotenv()

# Banco de Dados
DB_DIR = os.getenv("DB_DIR", "banco")
CSV_FILE = os.getenv("CSV_FILE", "banco/historico_ph.csv")
DB_PATH = os.getenv("DB_PATH", "banco/dados_ph.db")
BD_URI = os.getenv("BD_URI", f"sqlite:///{DB_PATH}")

# Porta Serial
PORTA_SERIAL = os.getenv("PORTA_SERIAL", "COM3")
BAUD_RATE = int(os.getenv("BAUD_RATE", 115200))

# Limites de pH
FAIXA_MIN_PH = float(os.getenv("FAIXA_MIN_PH", 6.5))
FAIXA_MAX_PH = float(os.getenv("FAIXA_MAX_PH", 8.0))

# Intervalos (segundos)
INTERVALO_VERIFICACAO = int(os.getenv("INTERVALO_VERIFICACAO", 300))
INTERVALO_ALERTA = int(os.getenv("INTERVALO_ALERTA", 600))

# API Key WhatsApp
MINHA_APIKEY = os.getenv("MINHA_APIKEY", "SUA_CHAVE_APIKEY_AQUI")

# Clientes (dispositivos para números de telefone)
CLIENTS = {}
for key, value in os.environ.items():
    if key.startswith("CLIENT_"):
        device_id = key[7:].lower()
        CLIENTS[device_id] = value

# Credenciais API
API_USERNAME = os.getenv("API_USERNAME", "usuario_api")
API_PASSWORD = os.getenv("API_PASSWORD", "senha_api")
