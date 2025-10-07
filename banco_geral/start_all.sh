#!/bin/sh

# Rodar backend FastAPI
uvicorn src.backend_server:app --host 0.0.0.0 --port 8000 &

# Rodar dashboard Streamlit
streamlit run src/main/dashboard.py &

# Rodar main.py para leitura e monitoramento
python src/main/main.py

# Espera para manter o container ativo
wait
