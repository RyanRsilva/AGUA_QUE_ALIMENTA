import os
from dotenv import load_dotenv

load_dotenv()

# Banco de Dados
DB_DIR = os.getenv("DB_DIR", "banco")
CSV_FILE = os.getenv("CSV_FILE", "banco/historico_ph.csv")
DB_PATH = os.getenv("DB_PATH", "banco/dados_ph.db")

# Banco de Dados - PostgreSQL
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "agua_que_alimenta")
POSTGRES_USER = os.getenv("POSTGRES_USER", "your_username")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "your_password")

BD_URI = os.getenv(
    "BD_URI", f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

# Porta Serial
PORTA_SERIAL = os.getenv("PORTA_SERIAL", "COM3")
BAUD_RATE = int(os.getenv("BAUD_RATE", 115200))

# Limites de pH
FAIXA_MIN_PH = float(os.getenv("FAIXA_MIN_PH", 6.5))
FAIXA_MAX_PH = float(os.getenv("FAIXA_MAX_PH", 8.0))

# Intervalos (segundos)
INTERVALO_VERIFICACAO = int(os.getenv("INTERVALO_VERIFICACAO", 300))
INTERVALO_ALERTA = int(os.getenv("INTERVALO_ALERTA", 600))

# API Key WhatsApp (CallMeBot - legado)
MINHA_APIKEY = os.getenv("MINHA_APIKEY", "SUA_CHAVE_APIKEY_AQUI")

# Evolution API
EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL", "http://localhost:8080")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "your-api-key")
EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE", "instance1")

# Clientes (dispositivos para números de telefone)
CLIENTS = {}
for key, value in os.environ.items():
    if key.startswith("CLIENT_"):
        device_id = key[7:].lower()
        CLIENTS[device_id] = value

# Credenciais API
API_USERNAME = os.getenv("API_USERNAME", "usuario_api")
API_PASSWORD = os.getenv("API_PASSWORD", "senha_api")

# API Base URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Configuração de Sensores
SENSORS = {
    "ph": {"min": FAIXA_MIN_PH, "max": FAIXA_MAX_PH},
    "temperature": {"min": 20.0, "max": 30.0},  # Exemplo
    "turbidity": {"min": 0.0, "max": 5.0},     # Exemplo
}
