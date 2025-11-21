# run.py
from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routes import router

# 1. Cria as tabelas antes de iniciar a aplicação
create_db_and_tables()

app = FastAPI(title="Process Mining Event API")

# 2. Inclui o roteador (onde está seu endpoint POST)
app.include_router(router)

# Ponto de execução com uvicorn (executar no terminal)
if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    print("\nPara iniciar, execute no terminal:")
    print("uvicorn run:app --reload")

# --- COMO EXECUTAR ---
# Certifique-se de que seu PostgreSQL está rodando
# 1. Verifique se o .env está configurado
# 2. Execute na raiz do projeto:
# uvicorn run:app --reload