from fastapi import APIRouter, Depends
from sqlmodel import Session
from .database import get_session
from .models import ProcessEvent, ProcessEventHomolog, ProcessEventCreate, FeedbackCreate

router = APIRouter()




from datetime import datetime, timedelta

def brazil_time():
    return datetime.utcnow() - timedelta(hours=3)

@router.post("/events/log", response_model=ProcessEvent, status_code=201)
def create_process_event(
    event: ProcessEventCreate,
    session: Session = Depends(get_session)
):
    data = event.model_dump(exclude={"production"})
    
    # Usa o timestamp passado ou gera automaticamente
    if not data.get("timestamp"):
        data["timestamp"] = brazil_time()

    if event.production:
        db_event = ProcessEvent.model_validate(data)
    else:
        db_event = ProcessEventHomolog.model_validate(data)

    session.add(db_event)
    session.commit()
    session.refresh(db_event)

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
        Feedback.timestamp >= data_limite  # ← MUDAR created_at para timestamp
    )
    
    resultado = session.exec(statement).first()
    
    return {
        "feedback_dado": resultado is not None,
        "user_id": user_id
    }

