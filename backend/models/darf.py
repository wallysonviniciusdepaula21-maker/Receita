from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class DARFData(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    protocol: str
    contribuinte: str
    cpf: str
    periodo_apuracao: str
    data_vencimento: str
    codigo_receita: str
    numero_referencia: str
    valor_principal: float
    multa: float
    juros: float
    valor_total: float
    created_at: datetime = Field(default_factory=datetime.utcnow)