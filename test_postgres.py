import os
from sqlalchemy import create_engine, text
from config.config import BD_URI


def test_postgres_connection():
    try:
        engine = create_engine(BD_URI)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()
            print("✅ Conexão com PostgreSQL bem-sucedida!")
            print(f"Versão do PostgreSQL: {version[0]}")
        return True
    except Exception as e:
        print(f"❌ Erro ao conectar com PostgreSQL: {e}")
        return False


if __name__ == "__main__":
    test_postgres_connection()
