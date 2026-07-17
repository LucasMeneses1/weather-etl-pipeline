from sqlalchemy import create_engine
from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)

# Monta a string de conexão
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Cria a engine de conexão
engine = create_engine(DATABASE_URL)

def get_engine():
    """
    Retorna a engine de conexão com o banco.
    """
    return engine