from src.config.settings import API_USERNAME, API_PASSWORD
from src.backend_server import app
import pytest
from httpx import AsyncClient, BasicAuth
import os

# Adiciona o diretório raiz ao path para encontrar o módulo `src`
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


BASE_URL = "http://test"
AUTH = BasicAuth(API_USERNAME, API_PASSWORD)


@pytest.mark.asyncio
async def test_receive_data():
    """Testa o endpoint de recebimento de dados."""
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        payload = {"device_id": "test_device", "sensor": "ph", "value": 7.5}
        response = await ac.post("/data", json=payload)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "sucesso"
    assert response_json["dados_recebidos"]["device_id"] == "test_device"


@pytest.mark.asyncio
async def test_get_latest_reading_unauthorized():
    """Testa o acesso não autorizado ao endpoint de última leitura."""
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get("/dados/ultimo")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_latest_reading_authorized():
    """Testa o acesso autorizado ao endpoint de última leitura."""
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        # Primeiro, insere um dado para garantir que o endpoint não retorne 404
        await ac.post("/data", json={"device_id": "test_device", "sensor": "ph", "value": 7.0})

        # Agora, testa o endpoint protegido
        response = await ac.get("/dados/ultimo", auth=AUTH)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_historical_readings():
    """Testa o endpoint de histórico."""
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get("/dados/historico/5", auth=AUTH)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) <= 5
