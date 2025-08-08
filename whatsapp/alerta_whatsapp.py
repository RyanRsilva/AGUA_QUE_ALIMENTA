# Processo de envio de mensagens via WhatsApp

"""[SQLite DB] --->[Ler últimas leituras] --->[Valor fora da faixa?] --->[Pode enviar?]
                                            | não
                                            v sim
                                        [Enviar WhatsApp]
"""

"""
alerta_whatsapp.py
Script que monitora o banco SQLite e envia alertas via WhatsApp Cloud API
Modo de uso:
    - Configure .env com TOKEN, PHONE_ID, DEST_PHONE (opcional)
    - Rode: python alerta_whatsapp.py
"""

"""
alerta_whatsapp.py
Script que monitora o banco SQLite e envia alertas via WhatsApp Cloud API
Modo de uso:
    - Configure .env com TOKEN, PHONE_ID, DEST_PHONE (opcional)
    - Rode: python alerta_whatsapp.py
"""

import sqlite3
import time
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Carregar variáveis de ambiente de um .env (opcional, mas recomendado)
load_dotenv()

# ===== CONFIG =====
DB_PATH = os.path.join("banco", "dados_ph_SQL.db")   # caminho do DB (ajusta se precisar)
TABELA = "leituras"                                  # nome da tabela que contém leituras
COL_TIMESTAMP = "data_hora"                          # nome da coluna timestamp
COL_SENSOR = "sensor"                                # nome da coluna sensor
COL_VALOR = "valor"                                  # nome da coluna do valor (ph)

# Faixa aceitável do pH (ajusta conforme necessidade)
PH_MIN = 6.5
PH_MAX = 8.5

# WhatsApp Cloud API (pega do .env ou altera direto aqui)
WH_TOKEN = os.getenv("WH_TOKEN")         # Bearer token
WH_PHONE_ID = os.getenv("WH_PHONE_ID")   # Phone Number ID (da sua conta do Facebook Developer)
TO_NUMBER = os.getenv("TO_NUMBER")       # número destino no formato internacional sem '+', ex: 5511999999999

# Política anti-spam: tempo mínimo entre alertas para o mesmo número (em segundos)
COOLDOWN_SECONDS = int(os.getenv("COOLDOWN_SECONDS", "600"))  # 10 minutos por padrão

# Modo simulação (não envia mensagem, só imprime) -> True para testar sem token
SIMULATION = os.getenv("SIMULATION", "False").lower() in ("1", "true", "yes")

# Endpoint (versão pode mudar conforme doc, aqui usamos v17.0+ compatível)
WH_URL_TEMPLATE = "https://graph.facebook.com/v17.0/{phone_id}/messages"

# ===== Estado em memória: controla cooldown por telefone =====
last_alert_time = {}  # dict: numero -> datetime do último alerta

def iniciar_monitoramento_alerta():
    """função que monitora o banco e envia alertas via WhatsApp"""


# ===== Funções =====
def enviar_whatsapp_texto(to_number: str, texto: str) -> bool:
    """
    Envia mensagem via WhatsApp Cloud API (ou simula).
    Retorna True se enviado com sucesso (ou simulado).
    """
    if SIMULATION:
        print(f"[SIMULAÇÃO] Mensagem para {to_number}: {texto}")
        return True

    if not WH_TOKEN or not WH_PHONE_ID:
        print("Erro: WH_TOKEN ou WH_PHONE_ID não configurados. Use .env ou configure as variáveis.")
        return False

    url = WH_URL_TEMPLATE.format(phone_id=WH_PHONE_ID)
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": texto}
    }
    headers = {
        "Authorization": f"Bearer {WH_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        if r.status_code in (200, 201):
            print(f"[{datetime.now()}] Mensagem enviada para {to_number}")
            return True
        else:
            print(f"[ERRO] status={r.status_code} resp={r.text}")
            return False
    except Exception as e:
        print(f"[EXCEÇÃO] Erro ao enviar WhatsApp: {e}")
        return False

def pode_enviar_alerta(to_number: str) -> bool:
    """Verifica cooldown para evitar spam."""
    agora = datetime.now()
    ultimo = last_alert_time.get(to_number)
    if ultimo is None:
        return True
    return (agora - ultimo) >= timedelta(seconds=COOLDOWN_SECONDS)

def registrar_alerta(to_number: str):
    last_alert_time[to_number] = datetime.now()

def buscar_ultimas_leituras(limit=20):
    """Lê as últimas leituras do DB (mais recentes primeiro)."""
    if not os.path.exists(DB_PATH):
        print(f"Arquivo DB não encontrado em {DB_PATH}")
        return []

    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        query = f"SELECT * FROM {TABELA} ORDER BY {COL_TIMESTAMP} DESC LIMIT ?"
        cursor.execute(query, (limit,))
        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()
        # transforma em lista de dicts
        dados = [dict(zip(cols, row)) for row in rows]
        return dados
    except Exception as e:
        print("Erro ao ler DB:", e)
        return []
    finally:
        conn.close()

def checar_e_alertar():
    """Verifica as leituras e envia alertas quando necessário."""
    dados = buscar_ultimas_leituras(limit=10)
    if not dados:
        return

    # Como buscamos em ordem desc, o primeiro é o mais recente
    for linha in reversed(dados):  # percorre do mais antigo pro mais novo (opcional)
        try:
            sensor = linha.get(COL_SENSOR) or "ph"
            valor = float(linha.get(COL_VALOR))
            ts = linha.get(COL_TIMESTAMP)
        except Exception:
            continue

        # Só alerta para sensor pH (ajuste se houver multiplos sensores)
        if str(sensor).lower() not in ("ph", "pH", "Ph"):
            continue

        if valor < PH_MIN or valor > PH_MAX:
            # decidir numero alvo (TO_NUMBER) - pode ser dinâmico se tiver coluna no DB
            to = TO_NUMBER
            if not to:
                print("Nenhum número destino configurado (TO_NUMBER). Ignorando alerta.")
                return

            if pode_enviar_alerta(to):
                texto = (f"⚠️ Alerta de pH: valor fora da faixa em {ts}\n"
                        f"Sensor: {sensor}\nValor: {valor}\nFaixa aceitável: {PH_MIN} - {PH_MAX}")
                ok = enviar_whatsapp_texto(to, texto)
                if ok:
                    registrar_alerta(to)
            else:
                print(f"Cooldown ativo para {to}. Não enviando alerta para {valor} ({ts}).")

# ===== LOOP PRINCIPAL (polling simples) =====
if __name__ == "__main__":
    print("Iniciando monitor de alertas WhatsApp (CTRL+C para sair).")
    intervalo = float(os.getenv("CHECK_INTERVAL", "10"))  # checa a cada X segundos
    try:
        while True:
            checar_e_alertar()
            time.sleep(intervalo)
    except KeyboardInterrupt:
        print("Monitor finalizado pelo usuário.")


