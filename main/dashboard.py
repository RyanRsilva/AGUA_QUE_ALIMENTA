import streamlit as st 
import sqlite3
import pandas as pd
import time 

# ===== config basicas =====

st.set_page_config(page_title="Monitoramento da Qualidade da Água", layout="centered")
st.title("Monitoramento da Qualidade da Água")
st.markdown("Dados em tempo real do sensor de pH (e outros futuramente)")

# ===== funçao para ler dados do banco =====

def Carregar_Dados ():
    conn = sqlite3.connect("banco/dados_ph_SQL.db") # tenho que verificar se o caminho ta correto
    df = pd.read_sql_query("SELECT * FROM leituras ORDER BY data_hora DESC LIMIT 50", conn)
    conn.close()
    return df

# ===== loop de atualização =====


placeholder = st.empty()

while True:
    df = Carregar_Dados()

    with placeholder.container():
        st.subheader("Útimas leituras")
        st.dataframe(df)

        st.subheader("Gráfico do pH")
        df['data_hora'] = pd.to_datetime(df['data_hora'])
        df_grafico = df.set_index('data_hora')[['valor']]
        st.line_chart(df_grafico)



    time.sleep(5) # atualiza a cada 5 seg



# codigo para correr ele : streamlit run main/dashboard.py  
