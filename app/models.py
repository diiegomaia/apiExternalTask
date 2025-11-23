from typing import Optional
from sqlmodel import Field, SQLModel
# Importar datetime é essencial para o timestamp
from datetime import datetime, timedelta


# Define o schema da tabela no PostgreSQL
class ProcessEvent(SQLModel, table=True):
    # ID DINÂMICO: O banco de dados (PostgreSQL) cria o ID sequencialmente
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # TIMESTAMP DINÂMICO: O Python/SQLModel cria o timestamp no momento da inserção
    def brazil_time():
        return datetime.utcnow() - timedelta(hours=3)

    timestamp: datetime = Field(default_factory=brazil_time, nullable=False)
    
  
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
 
class ProcessEventHomolog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # TIMESTAMP DINÂMICO: O Python/SQLModel cria o timestamp no momento da inserção
    def brazil_time():
        return datetime.utcnow() - timedelta(hours=3)

    timestamp: datetime = Field(default_factory=brazil_time, nullable=False)

    currentTaskName: str
    subjectName: Optional[str] = None
    subjectId: Optional[str] = None
    instanceId: Optional[str] = None
    senderUserName: Optional[str] = None
    senderUserId: Optional[str] = None
    currentGroupName: Optional[str] = None
    currentGroupId: Optional[str] = None


# Define o schema de entrada da API (o que o Camunda envia)
# Não incluímos 'id' nem 'timestamp' aqui, pois são gerados no backend.
class ProcessEventCreate(SQLModel):
    # Todos os seus campos customizados que vêm no 'body' do Groovy
    production: bool = True
    currentTaskName: str
    subjectName: Optional[str] = None
    subjectId: Optional[str] = None
    instanceId: Optional[str] = None
    senderUserName: Optional[str] = None
    senderUserId: Optional[str] = None
    currentGroupName: Optional[str] = None
    currentGroupId: Optional[str] = None

    # Campo que você pode usar para salvar todas as outras variáveis (opcional)
  


