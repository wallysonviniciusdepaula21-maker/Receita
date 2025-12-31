from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class CPFCache(BaseModel):
    """Modelo para cache de dados do CPF no MongoDB"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cpf: str
    name: str
    birthDate: str
    status: str  # IRREGULAR, REGULAR
    declaration2023: str  # NÃO ENTREGUE, ENTREGUE
    protocol: str
    deadline: str
    statusType: str  # CRÍTICO, NORMAL
    telefone: Optional[str] = None
    consulted_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
