from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime
from config.config import BD_URI


def create_tables():
    engine = create_engine(BD_URI)
    metadata = MetaData()

    # Definir a tabela leituras
    leituras = Table('leituras', metadata,
                     Column('id', Integer, primary_key=True,
                            autoincrement=True),
                     Column('data_hora', DateTime, nullable=False),
                     Column('device_id', String(50)),
                     Column('sensor', String(50), nullable=False),
                     Column('valor', Float, nullable=False)
                     )

    # Criar as tabelas
    metadata.create_all(engine)
    print("✅ Tabelas criadas com sucesso no PostgreSQL!")


if __name__ == "__main__":
    create_tables()
