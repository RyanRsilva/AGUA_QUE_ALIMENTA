import os
from dotenv import load_dotenv

load_dotenv()

# Banco de Dados - SQLite
DB_DIR = os.getenv("DB_DIR", "cloud/banco")
CSV_FILE = os.getenv("CSV_FILE", "cloud/banco/historico_ph.csv")
DB_PATH = os.getenv("DB_PATH", "cloud/banco/dados_ph.db")
BD_URI = f"sqlite:///{DB_PATH}"

# Porta Serial
PORTA_SERIAL = os.getenv("PORTA_SERIAL", "COM3")
BAUD_RATE = int(os.getenv("BAUD_RATE", 115200))

# Limites de pH
FAIXA_MIN_PH = float(os.getenv("FAIXA_MIN_PH", 6.5))
FAIXA_MAX_PH = float(os.getenv("FAIXA_MAX_PH", 8.0))

# Intervalos (segundos)
INTERVALO_VERIFICACAO = int(os.getenv("INTERVALO_VERIFICACAO", 300))
INTERVALO_ALERTA = int(os.getenv("INTERVALO_ALERTA", 600))

# API Key WhatsApp (CallMeBot)
MINHA_APIKEY = os.getenv("2180486")

# Clientes (dispositivos para números de telefone)
CLIENTS = {}
for key, value in os.environ.items():
    if key.startswith("CLIENT_"):
        device_id = key[7:].lower()
        CLIENTS[device_id] = value

# Credenciais API
API_USERNAME = os.getenv("API_USERNAME", "akashi")
API_PASSWORD = os.getenv("API_PASSWORD", "br8mRzx2535")

# API Base URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

# Configuração de Sensores
SENSORS = {
    "ph": {"min": FAIXA_MIN_PH, "max": FAIXA_MAX_PH},
    "temperature": {"min": 20.0, "max": 30.0},  # Exemplo
    "turbidity": {"min": 0.0, "max": 5.0},     # Exemplo
}
