import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import pandas as pd
import os
from datetime import datetime
from sqlalchemy import create_engine
import logging
from .config.settings import DB_DIR, CSV_FILE, BD_URI, API_USERNAME, API_PASSWORD
import traceback



# Configurar logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

os.makedirs(DB_DIR, exist_ok=True)
engine = create_engine(BD_URI)

app = FastAPI()
security = HTTPBasic()

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore
app.add_middleware(SlowAPIMiddleware)


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != API_USERNAME or credentials.password != API_PASSWORD:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return credentials.username


class SensorData(BaseModel):
    device_id: str = Field(min_length=1, max_length=50)
    sensor: str = Field(min_length=1, max_length=50)
    value: float = Field(ge=0)


@limiter.limit("10/minute")
@app.post("/data")
def receive_data(data: SensorData, request: Request):
    """
    Recebe dados do ESP32 (via POST) e os salva.
    """
    timestamp = datetime.now()
    logger.info(
        f"POST /data -> Recebido: Device: {data.device_id}, Sensor: {data.sensor}, Valor: {data.value}")

    try:
        novo_dado_df = pd.DataFrame(
            [[timestamp, data.device_id, data.value]], columns=["timestamp", "device_id", "ph"])
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


@limiter.limit("30/minute")
@app.get("/dados/ultimo", dependencies=[Depends(authenticate)])
def get_latest_reading(request: Request):
    """
    Busca no banco de dados e retorna a leitura mais recente.
    """
    try:
        query = "SELECT * FROM leituras ORDER BY data_hora DESC LIMIT 1"
        df = pd.read_sql(query, con=engine)
        if df.empty:
            raise HTTPException(
                status_code=404, detail="Nenhum dado encontrado")
        return df.to_dict('records')
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao ler o banco de dados: {e}")

# --- Endpoint 2: Obter um histórico de leituras ---


@limiter.limit("30/minute")
@app.get("/dados/historico/{limit}", dependencies=[Depends(authenticate)])
def get_historical_readings(limit: int, request: Request):
    """
    Retorna as últimas 'limit' leituras. O 'limit' é passado na própria URL.
    Ex: /dados/historico/10 -> retorna as últimas 10 leituras.
    """
    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=400, detail="Limit deve ser entre 1 e 1000")
    try:
        query = f"SELECT * FROM leituras ORDER BY data_hora DESC LIMIT {limit}"
        df = pd.read_sql(query, con=engine)
        if df.empty:
            raise HTTPException(
                status_code=404, detail="Nenhum dado encontrado")
        return df.to_dict('records')
    except Exception as e:
        logger.error(f"Ocorreu um erro em /dados/historico: {e}")
        logger.error(traceback.format_exc()) # Esta linha vai nos mostrar o erro completo
        raise HTTPException(
            status_code=500, detail=f"Erro ao ler o banco de dados: {e}")

# --- Endpoint 3: Obter um resumo estatístico ---


@limiter.limit("30/minute")
@app.get("/dados/resumo", dependencies=[Depends(authenticate)])
def get_summary(request: Request):
    """
    Lê todos os dados e retorna um resumo por sensor com média, mínimo, máximo e contagem.
    """
    try:
        query = "SELECT sensor, valor FROM leituras"
        df = pd.read_sql(query, con=engine)
        if df.empty:
            raise HTTPException(
                status_code=404, detail="Nenhum dado encontrado")

        resumo = {}
        for sensor in df['sensor'].unique():
            sensor_df = df[df['sensor'] == sensor]
            resumo[sensor] = {
                "total_leituras": int(sensor_df['valor'].count()),
                "medio": round(sensor_df['valor'].mean(), 2),
                "minimo": float(sensor_df['valor'].min()),
                "maximo": float(sensor_df['valor'].max())
            }
        return resumo
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar os dados: {e}")


# --- Ponto de Entrada para Rodar o Servidor---
if __name__ == "__main__":
    print("🚀 Iniciando servidor FastAPI com suporte a múltiplos dispositivos.")
    print("Pressione CTRL+C para parar.")
    uvicorn.run("src.backend_server:app", host="0.0.0.0", port=8000)
