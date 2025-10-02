# main/dashboard.py (Versão API-Driven)

from src.config.config import API_BASE_URL
import streamlit as st
import pandas as pd
import time
import requests

# --- CONFIGURAÇÕES ---
st.set_page_config(
    page_title="Monitoramento da Qualidade da Água", layout="centered")
st.title("Monitoramento da Qualidade da Água")
st.markdown("Dados em tempo real via API do sensor de pH")

# O endereço de informações"


def carregar_dados_via_api():
    """
    Esta função não toca mais no banco de dados. Ela faz uma requisição GET
    para o nosso endpoint de histórico no servidor FastAPI.
    """
    try:
        # Fazemos a chamada para o nosso endpoint, pedindo as últimas 50 leituras.
        response = requests.get(f"{API_BASE_URL}/dados/historico/50")

        # Esta linha verifica se o servidor respondeu com um erro (ex: 404, 500).
        # Se houve um erro, o programa para aqui e mostra o erro.
        response.raise_for_status()

        # Se a resposta foi um sucesso, pegamos o corpo da resposta em formato JSON.
        dados_json = response.json()

        # Convertemos o JSON (que é uma lista de dicionários) em um DataFrame do Pandas.
        df = pd.DataFrame(dados_json)
        return df

    except requests.exceptions.RequestException as e:
        # Se o servidor estiver offline ou houver um erro de rede, mostramos um aviso.
        st.error(f"Erro de conexão com a API: {e}")
        # Retorna um DataFrame vazio para não quebrar o resto do app.
        return pd.DataFrame()


placeholder = st.empty()

while True:
    df = carregar_dados_via_api()

    if not df.empty:
        with placeholder.container():
            st.subheader("Últimas Leituras (via API)")

            # Prepara a exibição dos dados
            df_display = df.copy()
            df_display['data_hora'] = pd.to_datetime(
                df_display['data_hora']).dt.strftime('%Y-%m-%d %H:%M:%S')
            st.dataframe(df_display.set_index('data_hora'))

            st.subheader("Gráfico do pH em Tempo Real")
            df_grafico = df.copy()
            df_grafico['data_hora'] = pd.to_datetime(df_grafico['data_hora'])
            df_grafico = df_grafico.set_index('data_hora')[['valor']]
            st.line_chart(df_grafico)
    else:
        with placeholder.container():
            st.warning("Aguardando dados da API do servidor...")

    time.sleep(5)  # Atualiza a cada 5 segundos
