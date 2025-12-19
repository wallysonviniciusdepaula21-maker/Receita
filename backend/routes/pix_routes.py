from fastapi import APIRouter, HTTPException
from models.pix import PixGenerateInput
from services.pix_service import PixService
from pydantic import BaseModel

router = APIRouter(prefix="/pix", tags=["PIX"])

class PixGenerateInputExtended(BaseModel):
    protocol: str
    value: float
    cpf: str
    nome: str = ""  # Opcional

@router.post("/gerar")
async def gerar_pix(input_data: PixGenerateInputExtended):
    """Gera código PIX para pagamento usando Furia Pay"""
    try:
        result = await PixService.gerar_pix(
            input_data.protocol,
            input_data.value,
            input_data.cpf,
            input_data.nome
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

@router.post("/webhook")
async def webhook_furia_pay(payload: dict):
    """Webhook para receber notificações do Furia Pay"""
    try:
        print(f"[Webhook] Recebido do Furia Pay: {payload}")
        
        # Processar webhook conforme documentação Furia Pay
        transaction_id = payload.get('id')
        status = payload.get('status')
        external_ref = payload.get('externalRef')  # Nosso protocol
        
        if status == 'paid' and external_ref:
            # Atualizar status do pagamento
            if external_ref in PixService.payments:
                PixService.payments[external_ref]['status'] = 'PAGO'
                PixService.payments[external_ref]['paidAt'] = payload.get('paidAt')
                print(f"[Webhook] ✓ Pagamento confirmado via webhook - Protocol: {external_ref}")
        
        return {'success': True, 'message': 'Webhook processado'}
        
    except Exception as e:
        print(f"[Webhook] Erro: {e}")
        return {'success': False, 'error': str(e)}