from models.pix import PixPayment
from datetime import datetime, timedelta
import random
import string
from services.furia_pay_service import furia_pay_service

class PixService:
    # Armazena pagamentos em memória (em produção seria no banco)
    payments = {}
    
    @staticmethod
    async def gerar_pix(protocol: str, value: float, cpf: str, nome: str = "") -> dict:
        """
        Gera um pagamento PIX usando Furia Pay
        
        Args:
            protocol: Protocolo da transação
            value: Valor em reais
            cpf: CPF do pagador
            nome: Nome do pagador (opcional)
        """
        try:
            print(f"[PixService] Gerando PIX via Furia Pay - Valor: R$ {value:.2f}")
            
            # Se não tem nome, usa genérico
            if not nome:
                nome = "Contribuinte"
            
            # Cria transação no Furia Pay
            resultado = furia_pay_service.criar_transacao_pix(
                valor=value,
                cpf=cpf,
                nome=nome,
                protocol=protocol
            )
            
            if resultado['success']:
                # Salva dados em memória
                payment_data = {
                    'protocol': protocol,
                    'cpf': cpf,
                    'value': value,
                    'pixCode': resultado['pix_code'],
                    'qrCodeUrl': resultado.get('qr_code_url', ''),
                    'qrCodeBase64': resultado.get('qr_code_base64', ''),
                    'transactionId': resultado['transaction_id'],
                    'status': 'PENDENTE',
                    'expiresAt': resultado.get('expires_at')
                }
                
                PixService.payments[protocol] = payment_data
                
                print(f"[PixService] ✓ PIX gerado com sucesso - Transaction ID: {resultado['transaction_id']}")
                
                return {
                    'success': True,
                    'data': payment_data
                }
            else:
                print(f"[PixService] ✗ Erro ao gerar PIX: {resultado.get('error')}")
                return {
                    'success': False,
                    'error': resultado.get('error', 'Erro ao gerar PIX')
                }
                
        except Exception as e:
            print(f"[PixService] ✗ Exceção ao gerar PIX: {e}")
            return {
                'success': False,
                'error': f'Erro ao processar pagamento: {str(e)}'
            }
    
    @staticmethod
    async def verificar_pagamento(protocol: str) -> dict:
        """
        Verifica status do pagamento PIX consultando Furia Pay
        """
        try:
            payment = PixService.payments.get(protocol)
            
            if not payment:
                return {
                    'success': False,
                    'message': 'Pagamento não encontrado'
                }
            
            # Consulta status no Furia Pay
            transaction_id = payment.get('transactionId')
            resultado = furia_pay_service.buscar_transacao(transaction_id)
            
            if resultado['success']:
                # Atualiza status
                if resultado['paid']:
                    payment['status'] = 'PAGO'
                    payment['paidAt'] = resultado['paid_at']
                    print(f"[PixService] ✓ Pagamento confirmado! Protocolo: {protocol}")
                
                return {
                    'success': True,
                    'data': {
                        'status': payment['status'],
                        'paidAt': payment.get('paidAt')
                    }
                }
            else:
                return resultado
                
        except Exception as e:
            print(f"[PixService] Erro ao verificar pagamento: {e}")
            return {
                'success': False,
                'error': str(e)
            }