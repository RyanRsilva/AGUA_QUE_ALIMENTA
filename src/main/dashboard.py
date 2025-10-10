# main/dashboard.py (Versão API-Driven)

from src.config.settings import API_BASE_URL, SENSORS,API_PASSWORD,API_USERNAME
import streamlit as st
import pandas as pd
import time
import requests
from datetime import datetime, timedelta

# --- CONFIGURAÇÕES ---
st.set_page_config(
    page_title="Monitoramento da Qualidade da Água", layout="wide")
st.title("Monitoramento da Qualidade da Água")
st.markdown("Dados em tempo real via API do sensor")

# Sidebar for filters
st.sidebar.header("Filtros")
start_date = st.sidebar.date_input(
    "Data inicial", datetime.now().date() - timedelta(days=7))
end_date = st.sidebar.date_input("Data final", datetime.now().date())
sensor_filter = st.sidebar.multiselect("Selecionar sensores", list(
    SENSORS.keys()), default=list(SENSORS.keys()))


def carregar_dados_via_api(limit=100):
    try:
        response = requests.get(f"{API_BASE_URL}/dados/historico/{limit}", auth=(API_USERNAME, API_PASSWORD))
        response.raise_for_status()
        dados_json = response.json()
        df = pd.DataFrame(dados_json)
        return df
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão com a API: {e}")
        return pd.DataFrame()


def carregar_resumo_via_api():
    try:
        response = requests.get(f"{API_BASE_URL}/dados/resumo", auth=(API_USERNAME, API_PASSWORD))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao carregar resumo: {e}")
        return {}


placeholder = st.empty()

while True:
    df = carregar_dados_via_api(200)  # Load more data

    if not df.empty:
        # Filter by date
        df['data_hora'] = pd.to_datetime(df['data_hora'])
        df_filtered = df[(df['data_hora'].dt.date >= start_date)
                         & (df['data_hora'].dt.date <= end_date)]
        df_filtered = df_filtered[df_filtered['sensor'].isin(sensor_filter)]

        with placeholder.container():
            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader("Últimas Leituras")

                df_display = df_filtered.tail(20).copy()
                df_display['data_hora'] = df_display['data_hora'].dt.strftime(
                    '%Y-%m-%d %H:%M:%S')
                st.dataframe(df_display.set_index('data_hora'))

            with col2:
                st.subheader("Resumo Estatístico")
                resumo = carregar_resumo_via_api()
                for sensor, stats in resumo.items():
                    if sensor in sensor_filter:
                        st.write(f"**{sensor.upper()}**")
                        st.write(f"Média: {stats['medio']}")
                        st.write(
                            f"Mín: {stats['minimo']}, Máx: {stats['maximo']}")
                        st.write(f"Total: {stats['total_leituras']}")
                        st.markdown("---")

            # Alerts
            st.subheader("Alertas")
            alerts = []
            for sensor, limits in SENSORS.items():
                if sensor in sensor_filter:
                    latest = df_filtered[df_filtered['sensor'] ==
                                         sensor]['valor'].iloc[-1] if not df_filtered[df_filtered['sensor'] == sensor].empty else None
                    if latest is not None:
                        if latest < limits['min'] or latest > limits['max']:
                            alerts.append(
                                f"⚠️ {sensor.upper()}: {latest} fora da faixa ({limits['min']}-{limits['max']})")
            if alerts:
                for alert in alerts:
                    st.warning(alert)
            else:
                st.success("Todos os sensores dentro da faixa normal.")

            # Charts
            st.subheader("Gráficos de Tendência")
            for sensor in sensor_filter:
                sensor_df = df_filtered[df_filtered['sensor'] == sensor].copy()
                if not sensor_df.empty:
                    sensor_df = sensor_df.set_index('data_hora')[['valor']]
                    st.line_chart(sensor_df, height=200)
                    st.caption(f"Tendência de {sensor.upper()}")
    else:
        with placeholder.container():
            st.warning("Aguardando dados da API do servidor...")

    time.sleep(10)  # Update every 10 seconds
