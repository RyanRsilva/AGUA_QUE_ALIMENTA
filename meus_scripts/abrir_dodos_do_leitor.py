
# MOSTRA OS DADOS QUE FORAM PROJETADOS DENTRO DO LEITOR

import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///ph_database.db')
df = pd.read_sql("SELECT * FROM leituras_ph", engine)
print(df)
