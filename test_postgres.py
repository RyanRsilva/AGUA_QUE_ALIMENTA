import psycopg2
from config.config import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD


def test_postgres_connection():
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname='postgres',
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            client_encoding='latin1'
        )
        cur = conn.cursor()
        cur.execute("SELECT version()")
        version = cur.fetchone()
        print("✅ Conexão com PostgreSQL bem-sucedida!")
        print(f"Versão do PostgreSQL: {version[0]}")
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Erro ao conectar com PostgreSQL: {e}")
        return False


if __name__ == "__main__":
    test_postgres_connection()
