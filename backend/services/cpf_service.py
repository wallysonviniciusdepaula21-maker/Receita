from models.cpf import CPFData
from datetime import datetime
import random

# Dados mockados para demonstração
MOCK_USERS = {
    "01230246258": {
        "name": "Natanael Sales Pantoja",
        "birth_date": "24/09/1975",
        "status": "IRREGULAR",
        "declaration_2023": "NÃO ENTREGUE",
        "protocol": "CTP9513859",
        "deadline": "20/12/2025",
        "status_type": "CRÍTICO"
    }
}

class CPFService:
    @staticmethod
    async def consultar_cpf(cpf: str) -> dict:
        # Remove formatação do CPF
        cpf_clean = cpf.replace(".", "").replace("-", "")
        
        # Verifica se CPF existe no mock
        if cpf_clean in MOCK_USERS:
            user_data = MOCK_USERS[cpf_clean]
            return {
                "success": True,
                "data": {
                    "name": user_data["name"],
                    "cpf": cpf,
                    "birthDate": user_data["birth_date"],
                    "status": user_data["status"],
                    "declaration2023": user_data["declaration_2023"],
                    "protocol": user_data["protocol"],
                    "deadline": user_data["deadline"],
                    "statusType": user_data["status_type"]
                }
            }
        
        # Gera dados aleatórios para qualquer outro CPF
        protocol = f"CTP{random.randint(1000000, 9999999)}"
        status = random.choice(["REGULAR", "IRREGULAR"])
        declaration = random.choice(["ENTREGUE", "NÃO ENTREGUE"])
        
        return {
            "success": True,
            "data": {
                "name": "Contribuinte Teste",
                "cpf": cpf,
                "birthDate": "01/01/1980",
                "status": status,
                "declaration2023": declaration,
                "protocol": protocol,
                "deadline": "31/12/2025",
                "statusType": "NORMAL" if status == "REGULAR" else "CRÍTICO"
            }
        }