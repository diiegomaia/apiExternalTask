from fastapi import Request, HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

async def api_key_middleware(request: Request, call_next):
    # Libera docs e schema
    if request.url.path in ["/docs", "/openapi.json", "/redoc"]:
        return await call_next(request)
    
    # PERMITIR OPTIONS (preflight CORS) sem validar API key
    if request.method == "OPTIONS":
        return await call_next(request)

    # Validar API key para outros métodos (GET, POST, etc)
    api_key = request.headers.get("x-api-key")

    if api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing x-api-key"
        )

    return await call_next(request)