from typing import Optional
from sqlmodel import Field, SQLModel
# Importar datetime é essencial para o timestamp
from datetime import datetime

# Define o schema da tabela no PostgreSQL
class ProcessEvent(SQLModel, table=True):
    # ID DINÂMICO: O banco de dados (PostgreSQL) cria o ID sequencialmente
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # TIMESTAMP DINÂMICO: O Python/SQLModel cria o timestamp no momento da inserção
    timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    
  
    # Metadados de Workflow Customizados (Extraídos do Payload Groovy)
    currentTaskName: str
    subjectName: Optional[str] = None
    subjectId: Optional[str] = None
    instanceId: Optional[str] = None
    senderUserName: Optional[str] = None
    senderUserId: Optional[str] = None
    currentGroupName: Optional[str] = None
    currentGroupId: Optional[str] = None
    
    # Dados brutos de todas as variáveis, caso necessário para mineração
    # Nota: Usamos str para JSON, que será armazenado como TEXT/VARCHAR no SQL
 


# Define o schema de entrada da API (o que o Camunda envia)
# Não incluímos 'id' nem 'timestamp' aqui, pois são gerados no backend.
class ProcessEventCreate(SQLModel):
    # Adicionamos case_id e activity_name para validação (são as chaves primárias do log)
    
    # Todos os seus campos customizados que vêm no 'body' do Groovy
    currentTaskName: str
    subjectName: Optional[str] = None
    subjectId: Optional[str] = None
    instanceId: Optional[str] = None
    senderUserName: Optional[str] = None
    senderUserId: Optional[str] = None
    currentGroupName: Optional[str] = None
    currentGroupId: Optional[str] = None

    # Campo que você pode usar para salvar todas as outras variáveis (opcional)
  


