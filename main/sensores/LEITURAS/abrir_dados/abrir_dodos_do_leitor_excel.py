
# MOSTRA OS DADOS QUE FORAM PROJETADOS DENTRO DO LEITOR

import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///dados_ph_SQL.db")
df = pd.read_sql("SELECT * FROM leituras", engine)
print(df)
