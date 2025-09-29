import pandas as pd
import plotly.express as px

# Lê os dados do Excel
df = pd.read_excel('dados_ph_excel.xlsx')

# Converte a coluna timestamp pra datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Cria a misera grafico interativo
fig = px.line(
    df,
    x="timestamp",
    y="ph",
    title="Variação do pH ao longo do tempo",
    markers=True,
    labels={"timestamp": "Data e Hora", "ph": "Valor de pH"},
    template="plotly_dark"
)

fig.update_layout(
    xaxis_title="Data e Hora",
    yaxis_title="Valor de pH",
    hovermode="x unified"
)

fig.show()
