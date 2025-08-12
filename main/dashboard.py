import streamlit as st 
import sqlite3
import pandas as pd
import time 
import os 
# ===== config basicas =====

st.set_page_config(page_title="Monitoramento da Qualidade da Água", layout="centered")
st.title("Monitoramento da Qualidade da Água")
st.markdown("Dados em tempo real do sensor de pH (e outros futuramente)")

# ===== funçao para ler dados do banco =====
def Carregar_Dados ():
    # Constrói o caminho absoluto para o banco de dados
    # Isso garante que o Streamlit sempre o encontrará, não importa de onde você rode o comando
    caminho_script = os.path.dirname(__file__) # Pega o diretório do script atual (ex: .../main)
    caminho_db = os.path.abspath(os.path.join(caminho_script, '..', 'banco', 'dados_ph.db'))

    conn = sqlite3.connect(caminho_db)
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
