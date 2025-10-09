import requests
import time

# Simular envio de dados do ESP32
url = "http://localhost:8000/data"

data = {
    "device_id": "esp32_ph_01",
    "sensor": "ph",
    "value": 7.2
}

response = requests.post(url, json=data)
print(f"Status: {response.status_code}, Response: {response.json()}")
