# app/models.py
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine
from datetime import datetime

# 1. Definição do Schema da Tabela (como ela é no banco)
class ProcessEvent(SQLModel, table=True):
    # O nome da tabela no PostgreSQL será 'processevent'
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Dados que você quer receber
    case_id: str = Field(index=True)        # O ID da instância do processo (seu alvo principal)
    activity_name: str                      # O nome da atividade/etapa (ex: 'MonitorProcess')
    timestamp: datetime = Field(default_factory=datetime.utcnow) # Quando o evento foi registrado
    payload_data: Optional[str] = None      # Dados variáveis (pode ser JSON ou uma string longa)

# 2. Definição do Schema de Entrada (o objeto que a API POST espera)
# Geralmente é um subconjunto do modelo principal
class ProcessEventCreate(SQLModel):
    case_id: str
    activity_name: str
    payload_data: Optional[str] = None