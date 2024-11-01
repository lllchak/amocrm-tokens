import psycopg2
from psycopg2 import sql
from app.core.config import settings


def get_db_connection():
    return psycopg2.connect(settings.database_url)


def create_tables_if_not_exist():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        create_amocrm_tokens_table = """
        CREATE TABLE IF NOT EXISTS amocrm_tokens (
            id SERIAL PRIMARY KEY,
            access_token TEXT NOT NULL,
            refresh_token TEXT NOT NULL,
            expires_in BIGINT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        cursor.execute(create_amocrm_tokens_table)
        conn.commit()

    except Exception as e:
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

def init_db():
    try:
        create_tables_if_not_exist()
    except Exception as e:
        pass
