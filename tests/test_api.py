import requests
import time

# Teste POST /data
print("Testando POST /data...")
response = requests.post("http://127.0.0.1:8000/data",
                         json={"device_id": "test_device", "sensor": "ph", "value": 7.0})
print(f"Status: {response.status_code}, Response: {response.json()}")

# Teste GET /dados/ultimo
print("\nTestando GET /dados/ultimo...")
response = requests.get("http://127.0.0.1:8000/dados/ultimo")
print(f"Status: {response.status_code}, Response: {response.json()}")

# Teste GET /dados/historico/5
print("\nTestando GET /dados/historico/5...")
response = requests.get("http://127.0.0.1:8000/dados/historico/5")
print(f"Status: {response.status_code}, Response: {response.json()}")

# Teste GET /dados/resumo
print("\nTestando GET /dados/resumo...")
response = requests.get("http://127.0.0.1:8000/dados/resumo")
print(f"Status: {response.status_code}, Response: {response.json()}")

print("\nTestes da API concluídos.")
