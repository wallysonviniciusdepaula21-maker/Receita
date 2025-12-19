from models.darf import DARFData
import random

class DARFService:
    @staticmethod
    async def gerar_darf(protocol: str) -> dict:
        # Valores fixos para o protocolo conhecido
        if protocol == "CTP9513859":
            return {
                "success": True,
                "data": {
                    "protocolo": protocol,
                    "contribuinte": "Natanael Sales Pantoja",
                    "cpf": "012.302.462-58",
                    "periodoApuracao": "18/11/2024",
                    "dataVencimento": "20/12/2025",
                    "codigoReceita": "8045",
                    "numeroReferencia": protocol,
                    "valorPrincipal": 98.44,
                    "multa": 35.28,
                    "juros": 17.70,
                    "valorTotal": 149.42
                }
            }
        
        # Gera valores aleatórios para outros protocolos
        valor_principal = round(random.uniform(50, 500), 2)
        multa = round(valor_principal * 0.35, 2)
        juros = round(valor_principal * 0.18, 2)
        valor_total = round(valor_principal + multa + juros, 2)
        
        return {
            "success": True,
            "data": {
                "protocolo": protocol,
                "contribuinte": "Contribuinte Teste",
                "cpf": "000.000.000-00",
                "periodoApuracao": "01/01/2024",
                "dataVencimento": "31/12/2025",
                "codigoReceita": "8045",
                "numeroReferencia": protocol,
                "valorPrincipal": valor_principal,
                "multa": multa,
                "juros": juros,
                "valorTotal": valor_total
            }
        }