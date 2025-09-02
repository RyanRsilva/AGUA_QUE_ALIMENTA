# backend_server.py

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os
from datetime import datetime
from sqlalchemy import create_engine

# --- CONFIGURAÇÕES ---
DB_DIR = 'banco'
CSV_FILE = os.path.join(DB_DIR, 'historico_ph.csv')
DB_PATH = os.path.join(DB_DIR, "dados_ph.db")
BD_URI = f'sqlite:///{DB_PATH}'

os.makedirs(DB_DIR, exist_ok=True)
engine = create_engine(BD_URI)

# Cria a planta do nosso servidor.
app = FastAPI()

# Define o "contrato": todo dado recebido deve ter este formato.


class SensorData(BaseModel):
    sensor: str
    value: float

# Define o "portão de entrada" /data, que só aceita o método POST.


@app.post("/data")
def receive_data(data: SensorData):
    """
    o ESP32 envia dados para /data, esta função é executada.
    """
    timestamp = datetime.now()
    print(f"[{timestamp.strftime('%H:%M:%S')}] Dado recebido -> Sensor: {data.sensor}, Valor: {data.value}")

    # O processo de arquivamento (salvar em CSV e DB) é o mesmo de antes.
    try:
        novo_dado_df = pd.DataFrame(
            [[timestamp, data.value]], columns=["timestamp", "ph"])
        novo_dado_df.to_csv(CSV_FILE, mode='a', index=False,
                            header=not os.path.exists(CSV_FILE))

        novo_dado_sql = pd.DataFrame([[timestamp, data.sensor, data.value]], columns=[
                                    "data_hora", "sensor", "valor"])
        novo_dado_sql.to_sql("leituras", con=engine,
                            if_exists='append', index=False)
    except Exception as e:
        return {"status": "erro_ao_salvar", "detalhes": str(e)}

    return {"status": "sucesso", "dados_recebidos": data}


# Ponto de entrada para ligar o servidor.
if __name__ == "__main__":
    print("🚀 Iniciando servidor FastAPI. Ouvindo em http://0.0.0.0:8000")
    print("Pressione CTRL+C para parar.")
    # Uvicorn é o motor que executa a planta do FastAPI.
    uvicorn.run("backend_server:app", host="0.0.0.0",
                port=8000,)  # reload=True


