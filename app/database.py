# app/database.py
from sqlmodel import create_engine, SQLModel
import os
from dotenv import load_dotenv
from sqlmodel import Session
from .models import ProcessEvent

load_dotenv() # Carrega as variáveis do arquivo .env

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    """Cria o banco de dados e as tabelas definidas em models.py, se não existirem."""
    SQLModel.metadata.create_all(engine)
    print("Banco de dados e tabelas criadas com sucesso!")

# Para gerenciar sessões de banco de dados
def get_session():
    """Gera uma nova sessão de banco de dados para a rota."""
    with Session(engine) as session:
        yield session