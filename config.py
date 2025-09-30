import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Banco
DB_DIR = os.getenv('DB_DIR', 'banco')
CSV_FILE = os.getenv('CSV_FILE', os.path.join(DB_DIR, 'historico_ph.csv'))
DB_PATH = os.getenv('DB_PATH', os.path.join(DB_DIR, 'dados_ph.db'))
BD_URI = os.getenv('BD_URI', f'sqlite:///{DB_PATH}')

# Porta Serial
PORTA_SERIAL = os.getenv('PORTA_SERIAL', 'COM3')
BAUD_RATE = int(os.getenv('BAUD_RATE', 115200))

# Faixas de pH
FAIXA_MIN_PH = float(os.getenv('FAIXA_MIN_PH', 6.5))
FAIXA_MAX_PH = float(os.getenv('FAIXA_MAX_PH', 8.0))

# Intervalos
INTERVALO_VERIFICACAO = int(os.getenv('INTERVALO_VERIFICACAO', 300))
INTERVALO_ALERTA = int(os.getenv('INTERVALO_ALERTA', 600))

# API WhatsApp
MINHA_APIKEY = os.getenv('MINHA_APIKEY', 'SUA_CHAVE_APIKEY_AQUI')

# Clientes (pode ser expandido para um dict dinâmico)
CLIENTS = {}
for key, value in os.environ.items():
    if key.startswith('CLIENT_'):
        device_id = key.replace('CLIENT_', '').lower()
        CLIENTS[device_id] = value

# API
API_USERNAME = os.getenv('API_USERNAME', 'admin')
API_PASSWORD = os.getenv('API_PASSWORD', 'senha123')

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'app.log')
