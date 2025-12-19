from fastapi import APIRouter, HTTPException
from models.pix import PixGenerateInput
from services.pix_service import PixService

router = APIRouter(prefix="/pix", tags=["PIX"])

@router.post("/gerar")
async def gerar_pix(input_data: PixGenerateInput):
    """Gera código PIX para pagamento"""
    try:
        result = await PixService.gerar_pix(
            input_data.protocol,
            input_data.value,
            input_data.cpf
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/verificar/{protocol}")
async def verificar_pagamento(protocol: str):
    """Verifica status do pagamento PIX"""
    try:
        result = await PixService.verificar_pagamento(protocol)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))