import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Conecta ao banco SQLite
engine = create_engine("sqlite:///dados_ph_SQL.db")

# Lê os dados da tabela
df = pd.read_sql("SELECT * FROM leituras_ph", con=engine)

# Converte a coluna timestamp
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Cria o gráfico
fig = px.line(
    df,
    x="timestamp",
    y="ph",
    title="Leitura de pH (Banco de Dados)",
    markers=True,
    labels={"timestamp": "Data e Hora", "ph": "Valor de pH"},
    template="plotly"
)

fig.update_layout(
    xaxis_title="Data e Hora",
    yaxis_title="Valor de pH",
    hovermode="x unified"
)

fig.show()
