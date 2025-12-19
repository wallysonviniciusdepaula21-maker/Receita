from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class PixPayment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    protocol: str
    cpf: str
    value: float
    pix_code: str
    qr_code_url: str
    status: str  # PENDENTE, PAGO, EXPIRADO
    expires_at: datetime
    paid_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PixGenerateInput(BaseModel):
    protocol: str
    value: float
    cpf: str