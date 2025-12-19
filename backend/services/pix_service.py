from models.pix import PixPayment
from datetime import datetime, timedelta
import random
import string

class PixService:
    # Armazena pagamentos em memória (em produção seria no banco)
    payments = {}
    
    @staticmethod
    def generate_pix_code(protocol: str, value: float) -> str:
        """Gera um código PIX simulado"""
        # Código PIX simplificado (em produção seria gerado por API bancária)
        base = f"00020101021226940014br.gov.bcb.pix01257sercode.hypermall.eip.com.br/qrpix/v2/{protocol}"
        value_str = f"5802BR5925RECEITA FEDERAL DO BRA6009Sao Paulo62070503***"
        checksum = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"{base}52040000530398654{value}{value_str}6304{checksum}"
    
    @staticmethod
    async def gerar_pix(protocol: str, value: float, cpf: str) -> dict:
        """Gera um pagamento PIX"""
        pix_code = PixService.generate_pix_code(protocol, value)
        qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={pix_code[:100]}"
        expires_at = datetime.utcnow() + timedelta(hours=24)
        
        payment = {
            "protocol": protocol,
            "cpf": cpf,
            "value": value,
            "pixCode": pix_code,
            "qrCodeUrl": qr_code_url,
            "status": "PENDENTE",
            "expiresAt": expires_at.isoformat()
        }
        
        # Salva em memória
        PixService.payments[protocol] = payment
        
        return {
            "success": True,
            "data": payment
        }
    
    @staticmethod
    async def verificar_pagamento(protocol: str) -> dict:
        """Verifica status do pagamento PIX"""
        payment = PixService.payments.get(protocol)
        
        if not payment:
            return {
                "success": False,
                "message": "Pagamento não encontrado"
            }
        
        # Simula pagamento aleatório (5% de chance de estar pago)
        if payment["status"] == "PENDENTE" and random.random() < 0.05:
            payment["status"] = "PAGO"
            payment["paidAt"] = datetime.utcnow().isoformat()
        
        return {
            "success": True,
            "data": {
                "status": payment["status"],
                "paidAt": payment.get("paidAt")
            }
        }