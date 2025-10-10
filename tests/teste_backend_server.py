# main/backend_server.py (Versão com API Aprimorada)

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import pandas as pd
import os
from datetime import datetime
from sqlalchemy import create_engine
import logging
from config.settings import DB_DIR, CSV_FILE, DB_PATH, BD_URI, API_USERNAME, API_PASSWORD

# Configurar logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

os.makedirs(DB_DIR, exist_ok=True)
engine = create_engine(BD_URI)
app = FastAPI()
security = HTTPBasic()


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != API_USERNAME or credentials.password != API_PASSWORD:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return credentials.username


class SensorData(BaseModel):
    device_id: str
    sensor: str
    value: float


@app.post("/data")
def receive_data(data: SensorData):
    """
    Recebe dados do ESP32 (via POST) e os salva.
    """
    timestamp = datetime.now()
    logger.info(
        f"POST /data -> Recebido: Device: {data.device_id}, Sensor: {data.sensor}, Valor: {data.value}")

    try:
        novo_dado_df = pd.DataFrame(
            [[timestamp, data.device_id, data.value]], columns=["device_id", "timestamp", "ph"])
        novo_dado_df.to_csv(CSV_FILE, mode='a', index=False,
                            header=not os.path.exists(CSV_FILE))

        novo_dado_sql = pd.DataFrame([[timestamp, data.device_id, data.sensor, data.value]], columns=[
            "data_hora", "device_id", "sensor", "valor"])
        novo_dado_sql.to_sql("leituras", con=engine,
                             if_exists='append', index=False)
    except Exception as e:
        logger.error(f"Erro ao salvar dados: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erro ao salvar no banco de dados: {e}")

    return {"status": "sucesso", "dados_recebidos": data}

# --- Endpoint 1: Obter a última leitura ---


@app.get("/dados/ultimo", dependencies=[Depends(authenticate)])
def get_latest_reading():
    """
    Busca no banco de dados e retorna a leitura mais recente.
    """
    try:
        query = "SELECT * FROM leituras ORDER BY data_hora DESC LIMIT 1"
        df = pd.read_sql(query, con=engine)
        if df.empty:
            raise HTTPException(
                status_code=404, detail="Nenhum dado encontrado")
        # .to_dict('records') converte o DataFrame para uma lista de dicionários, formato ideal para JSON.
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao ler o banco de dados: {e}")

# --- Endpoint 2: Obter um histórico de leituras ---


@app.get("/dados/historico/{limit}", dependencies=[Depends(authenticate)])
def get_historical_readings(limit: int):
    """
    Retorna as últimas 'limit' leituras. O 'limit' é passado na própria URL.
    Ex: /dados/historico/10 -> retorna as últimas 10 leituras.
    """
    try:
        # Usei uma f-string para inserir o limite dinamicamente na consulta SQL.
        query = f"SELECT * FROM leituras ORDER BY data_hora DESC LIMIT {limit}"
        df = pd.read_sql(query, con=engine)
        if df.empty:
            raise HTTPException(
                status_code=404, detail="Nenhum dado encontrado")
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao ler o banco de dados: {e}")

# --- Endpoint 3: Obter um resumo estatístico ---


@app.get("/dados/resumo", dependencies=[Depends(authenticate)])
def get_summary():
    """
    Lê todos os dados de pH e retorna um resumo com média, mínimo, máximo e contagem.
    """
    try:
        query = "SELECT valor FROM leituras WHERE sensor = 'ph'"
        df = pd.read_sql(query, con=engine)
        if df.empty:
            raise HTTPException(
                status_code=404, detail="Nenhum dado encontrado")

        # usei a peste do Pandas para calcular as estatísticas.
        resumo = {
            "total_leituras": int(df['valor'].count()),
            "ph_medio": round(df['valor'].mean(), 2),
            "ph_minimo": float(df['valor'].min()),
            "ph_maximo": float(df['valor'].max())
        }
        return resumo
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar os dados: {e}")


# --- Ponto de Entrada para Rodar o Servidor---
if __name__ == "__main__":
    print("🚀 Iniciando servidor FastAPI com suporte a múltiplos dispositivos.")
    print("Pressione CTRL+C para parar.")
    uvicorn.run("backend_server:app", host="0.0.0.0", port=8000)
