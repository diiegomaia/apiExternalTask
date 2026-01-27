# run.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ← ADICIONAR
from app.database import create_db_and_tables
from app.routes import router
from app.security import api_key_middleware

# 1. Cria as tabelas antes de iniciar a aplicação
create_db_and_tables()

app = FastAPI(title="Process Mining Event API")

# 2. CORS PRIMEIRO (antes de tudo) ← ADICIONAR ISSO
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos os domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. API Key middleware DEPOIS do CORS
app.middleware("http")(api_key_middleware)

# 4. Inclui o roteador (onde estão os endpoints)
app.include_router(router)

# Ponto de execução com uvicorn (executar no terminal)
if __name__ == "__main__":
    import uvicorn
    print("\nPara iniciar, execute no terminal:")
    print("uvicorn run:app --reload")

# --- COMO EXECUTAR ---
# Certifique-se de que seu PostgreSQL está rodando
# 1. Verifique se o .env está configurado
# 2. Execute na raiz do projeto:
# uvicorn run:app --reload