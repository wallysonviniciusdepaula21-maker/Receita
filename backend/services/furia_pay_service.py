import requests
import base64
import os
from typing import Dict
import uuid
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

class FuriaPayService:
    """Serviço para integração com Furia Pay BR"""
    
    def __init__(self):
        self.base_url = "https://api.furiapaybr.com/v1"
        self.public_key = os.getenv('FURIAPAY_PUBLIC_KEY')
        self.secret_key = os.getenv('FURIAPAY_SECRET_KEY')
        
        if not self.public_key or not self.secret_key:
            raise ValueError("Chaves do Furia Pay não configuradas no .env")
        
        # Cria autenticação Basic
        credentials = f"{self.public_key}:{self.secret_key}"
        self.auth_header = 'Basic ' + base64.b64encode(credentials.encode()).decode()
    
    def criar_transacao_pix(self, valor: float, cpf: str, nome: str, protocol: str) -> Dict:
        """
        Cria uma transação PIX no Furia Pay
        
        Args:
            valor: Valor em reais (ex: 149.42)
            cpf: CPF do pagador
            nome: Nome completo do pagador
            protocol: Protocolo único da transação
        
        Returns:
            Dict com dados da transação incluindo QR Code PIX
        """
        try:
            # Converte valor para centavos
            valor_centavos = int(valor * 100)
            
            # Monta payload conforme documentação Furia Pay
            payload = {
                "amount": valor_centavos,
                "paymentMethod": "pix",
                "items": [
                    {
                        "title": "Regularização DARF - Imposto de Renda",
                        "unitPrice": valor_centavos,
                        "quantity": 1,
                        "tangible": False,
                        "externalRef": ""
                    }
                ],
                "customer": {
                    "name": nome,
                    "email": f"{cpf.replace('.', '').replace('-', '')}@regularizacao.temp",
                    "phone": None,
                    "document": {
                        "type": "cpf",
                        "number": cpf.replace('.', '').replace('-', '')
                    }
                },
                "externalRef": protocol
            }
            
            # Faz requisição para API
            headers = {
                'Authorization': self.auth_header,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            print(f"[FuriaPay] Criando transação PIX - Valor: R$ {valor:.2f}")
            print(f"[FuriaPay] Public Key: {self.public_key[:20]}...")
            print(f"[FuriaPay] Secret Key: {self.secret_key[:20]}...")
            print(f"[FuriaPay] Auth Header: {self.auth_header[:60]}...")
            
            response = requests.post(
                f"{self.base_url}/transactions",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            print(f"[FuriaPay] Status Code: {response.status_code}")
            print(f"[FuriaPay] Response: {response.text[:200]}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"[FuriaPay] ✓ Transação criada com sucesso - ID: {data.get('id')}")
                
                # Extrai informações do PIX
                pix_data = data.get('pix', {})
                
                return {
                    'success': True,
                    'transaction_id': data.get('id'),
                    'status': data.get('status'),
                    'pix_code': pix_data.get('qrcode', ''),  # Código PIX copia e cola
                    'qr_code_url': f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={pix_data.get('qrcode', '')}",  # Gera QR Code
                    'expires_at': pix_data.get('expirationDate'),
                    'amount': valor
                }
            else:
                error_data = response.json() if response.text else {}
                print(f"[FuriaPay] ✗ Erro ao criar transação - Status: {response.status_code}")
                print(f"[FuriaPay] Resposta: {error_data}")
                
                return {
                    'success': False,
                    'error': error_data.get('message', 'Erro ao criar transação PIX'),
                    'details': error_data
                }
                
        except Exception as e:
            print(f"[FuriaPay] ✗ Exceção ao criar transação: {e}")
            return {
                'success': False,
                'error': f'Erro na comunicação com Furia Pay: {str(e)}'
            }
    
    def buscar_transacao(self, transaction_id: str) -> Dict:
        """
        Busca status de uma transação
        
        Args:
            transaction_id: ID da transação no Furia Pay
        
        Returns:
            Dict com dados atualizados da transação
        """
        try:
            headers = {
                'Authorization': self.auth_header,
                'Accept': 'application/json'
            }
            
            response = requests.get(
                f"{self.base_url}/transactions/{transaction_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'status': data.get('status'),
                    'paid': data.get('status') == 'paid',
                    'paid_at': data.get('paidAt'),
                    'data': data
                }
            else:
                return {
                    'success': False,
                    'error': 'Transação não encontrada'
                }
                
        except Exception as e:
            print(f"[FuriaPay] Erro ao buscar transação: {e}")
            return {
                'success': False,
                'error': str(e)
            }

# Instância global
furia_pay_service = FuriaPayService()