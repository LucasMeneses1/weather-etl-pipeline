from pathlib import Path
from dotenv import load_dotenv
import os

# Caminho para o arquivo .env
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

# Carrega as variáveis de ambiente
load_dotenv(ENV_FILE)

# Configurações do banco
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")