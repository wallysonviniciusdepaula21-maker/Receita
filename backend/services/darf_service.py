from models.darf import DARFData
from datetime import datetime, timedelta
import hashlib
import random

class DARFService:
    # Valores fixos conforme solicitado
    VALOR_PRINCIPAL = 98.44
    MULTA = 35.28
    JUROS = 17.70
    VALOR_TOTAL = 149.42
    
    @staticmethod
    def extrair_nome_protocolo(protocol: str) -> str:
        """Extrai nome do contribuinte baseado no protocolo"""
        # Em produção, isso buscaria no banco de dados
        # Por enquanto, retorna nome genérico
        return "Contribuinte"
    
    @staticmethod
    def extrair_cpf_protocolo(protocol: str) -> str:
        """Extrai CPF baseado no protocolo"""
        # Em produção, buscaria no banco
        return "000.000.000-00"
    
    @staticmethod
    async def gerar_darf(protocol: str) -> dict:
        """Gera DARF com valores fixos para qualquer protocolo"""
        
        # Datas dinâmicas - prazo é HOJE
        data_hoje = datetime.now()
        periodo_apuracao = (data_hoje - timedelta(days=random.randint(30, 60))).strftime("%d/%m/%Y")
        data_vencimento = data_hoje.strftime("%d/%m/%Y")  # PRAZO É HOJE
        
        return {
            "success": True,
            "data": {
                "protocolo": protocol,
                "contribuinte": "Contribuinte",  # Será preenchido pelo frontend com dados salvos
                "cpf": "000.000.000-00",  # Será preenchido pelo frontend
                "periodoApuracao": periodo_apuracao,
                "dataVencimento": data_vencimento,
                "codigoReceita": "8045",
                "numeroReferencia": protocol,
                "valorPrincipal": DARFService.VALOR_PRINCIPAL,
                "multa": DARFService.MULTA,
                "juros": DARFService.JUROS,
                "valorTotal": DARFService.VALOR_TOTAL
            }
        }