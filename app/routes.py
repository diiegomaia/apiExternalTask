from fastapi import APIRouter, Depends
from sqlmodel import Session
from .database import get_session
from .models import ProcessEvent, ProcessEventCreate

router = APIRouter()

# O endpoint POST deve agora receber a nova estrutura ProcessEventCreate
@router.post("/events/log", response_model=ProcessEvent, status_code=201)
def create_process_event(
    event: ProcessEventCreate,
    session: Session = Depends(get_session)
):
    """
    Recebe um objeto de evento (via POST) com metadados de workflow, 
    o salva no PostgreSQL e retorna o objeto salvo.
    """
    # 1. Converte o objeto de entrada (Pydantic) para o objeto do banco (SQLModel)
    # Isso funciona porque as chaves em ProcessEventCreate correspondem
    # às chaves em ProcessEvent (exceto id e timestamp, que são automáticos).
    db_event = ProcessEvent.model_validate(event)
    
    # 2. Adiciona à sessão e salva no banco
    session.add(db_event)
    session.commit()
    session.refresh(db_event) # Atualiza o objeto para incluir o ID e TIMESTAMP gerados

    # 3. Retorna o objeto criado
    return db_event