from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class CPFData(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cpf: str
    name: str
    birth_date: str
    status: str  # REGULAR, IRREGULAR
    declaration_2023: str  # ENTREGUE, NÃO ENTREGUE
    protocol: str
    deadline: str
    status_type: str  # NORMAL, CRÍTICO
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CPFConsultaInput(BaseModel):
    cpf: str
    nome: str = ""  # Nome opcional - se vazio, gera automaticamente