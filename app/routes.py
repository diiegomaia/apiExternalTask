from fastapi import APIRouter, Depends
from sqlmodel import Session
from .database import get_session
from .models import ProcessEvent, ProcessEventHomolog, ProcessEventCreate, FeedbackCreate

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
# Escolhe a tabela com base no 'production'
    if event.production:
        db_event = ProcessEvent.model_validate(event.model_dump(exclude={"production"}))
    else:
        db_event = ProcessEventHomolog.model_validate(event.model_dump(exclude={"production"}))
    
    # 2. Adiciona à sessão e salva no banco
    session.add(db_event)
    session.commit()
    session.refresh(db_event) # Atualiza o objeto para incluir o ID e TIMESTAMP gerados

    # 3. Retorna o objeto criado
    return db_event

# ============================================
# ROTA: CRIAR FEEDBACK
# ============================================

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime, timedelta
from .database import get_session
from .models import Feedback, FeedbackCreate




@router.post("/feedback/enviar", response_model=Feedback, status_code=201)
def criar_feedback(
    feedback: FeedbackCreate,
    session: Session = Depends(get_session)
):
    """
    Recebe um feedback do usuário (avaliação com estrelas + comentário opcional)
    e salva no banco de dados.
    """
    # Converter o modelo Pydantic para o modelo de banco
    db_feedback = Feedback.model_validate(feedback.model_dump())
    
    # Adicionar à sessão e salvar
    session.add(db_feedback)
    session.commit()
    session.refresh(db_feedback)
    
    return db_feedback


# ============================================
# ROTA: VERIFICAR SE USUÁRIO JÁ DEU FEEDBACK
# ============================================

@router.get("/feedback/verificar/{user_id}")
def verificar_feedback(
    user_id: str,
    session: Session = Depends(get_session)
):
    """
    Verifica se o usuário já enviou feedback nos últimos 30 dias.
    Retorna: { "feedback_dado": true/false }
    """
    # Data de 30 dias atrás
    data_limite = datetime.now() - timedelta(days=30)
    
    # Buscar feedbacks do usuário nos últimos 30 dias
    statement = select(Feedback).where(
        Feedback.user_id == user_id,
        Feedback.created_at >= data_limite
    )
    
    resultado = session.exec(statement).first()
    
    return {
        "feedback_dado": resultado is not None,
        "user_id": user_id
    }

