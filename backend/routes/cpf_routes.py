from fastapi import APIRouter, HTTPException
from models.cpf import CPFConsultaInput
from services.cpf_service import CPFService

router = APIRouter(prefix="/cpf", tags=["CPF"])

@router.post("/consultar")
async def consultar_cpf(input_data: CPFConsultaInput):
    """Consulta status do CPF"""
    try:
        result = await CPFService.consultar_cpf(input_data.cpf, input_data.nome)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))