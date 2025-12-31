from models.cpf import CPFData
from datetime import datetime, timedelta
import random
import hashlib
from services.yan_buscas_service import yan_buscas_service

class CPFService:
    @staticmethod
    def validar_cpf(cpf: str) -> bool:
        """Valida CPF usando algoritmo oficial"""
        # Remove caracteres não numéricos
        cpf_numbers = ''.join(filter(str.isdigit, cpf))
        
        # Verifica se tem 11 dígitos
        if len(cpf_numbers) != 11:
            return False
        
        # Verifica se todos os dígitos são iguais
        if cpf_numbers == cpf_numbers[0] * 11:
            return False
        
        # Valida primeiro dígito verificador
        soma = sum(int(cpf_numbers[i]) * (10 - i) for i in range(9))
        digito1 = (soma * 10 % 11) % 10
        
        if digito1 != int(cpf_numbers[9]):
            return False
        
        # Valida segundo dígito verificador
        soma = sum(int(cpf_numbers[i]) * (11 - i) for i in range(10))
        digito2 = (soma * 10 % 11) % 10
        
        if digito2 != int(cpf_numbers[10]):
            return False
        
        return True
    
    @staticmethod
    def formatar_cpf(cpf: str) -> str:
        """Formata CPF para padrão XXX.XXX.XXX-XX"""
        cpf_numbers = ''.join(filter(str.isdigit, cpf))
        return f"{cpf_numbers[:3]}.{cpf_numbers[3:6]}.{cpf_numbers[6:9]}-{cpf_numbers[9:]}"
    
    @staticmethod
    def gerar_protocolo(cpf: str) -> str:
        """Gera protocolo consistente baseado no CPF"""
        cpf_numbers = ''.join(filter(str.isdigit, cpf))
        # Usa hash para gerar número consistente
        hash_object = hashlib.md5(cpf_numbers.encode())
        hash_hex = hash_object.hexdigest()
        # Pega primeiros 7 dígitos do hash
        numero = int(hash_hex[:7], 16) % 10000000
        return f"CTP{numero:07d}"
    
    @staticmethod
    async def consultar_cpf(cpf: str) -> dict:
        """Consulta CPF usando Yan Buscas (dados reais)"""
        # Remove formatação
        cpf_clean = ''.join(filter(str.isdigit, cpf))
        
        # Valida CPF
        if not CPFService.validar_cpf(cpf_clean):
            return {
                "success": False,
                "message": "CPF inválido"
            }
        
        # Formata CPF
        cpf_formatado = CPFService.formatar_cpf(cpf_clean)
        
        # Busca dados reais no Yan Buscas
        print(f"[CPFService] Consultando CPF no Yan Buscas: {cpf_clean}")
        resultado = await yan_buscas_service.consultar_cpf(cpf_clean)
        
        if not resultado['success']:
            return {
                "success": False,
                "message": f"Erro ao consultar CPF: {resultado.get('error', 'Dados não encontrados')}"
            }
        
        # Usa dados reais do Yan Buscas
        nome = resultado['nome']
        data_nascimento = resultado['data_nascimento']
        
        # Gera protocolo consistente
        protocol = CPFService.gerar_protocolo(cpf_clean)
        
        # Define status baseado em algum critério (exemplo: CPFs pares são irregulares)
        ultimo_digito = int(cpf_clean[-1])
        status = "IRREGULAR" if ultimo_digito % 2 == 0 else "REGULAR"
        declaration = "NÃO ENTREGUE" if status == "IRREGULAR" else "ENTREGUE"
        status_type = "CRÍTICO" if status == "IRREGULAR" else "NORMAL"
        
        # Calcular prazo (hoje + 21 dias)
        prazo_final = (datetime.now() + timedelta(days=21)).strftime("%d/%m/%Y")
        
        return {
            "success": True,
            "data": {
                "name": nome,
                "cpf": cpf_formatado,
                "birthDate": data_nascimento,
                "status": status,
                "declaration2023": declaration,
                "protocol": protocol,
                "deadline": prazo_final,
                "statusType": status_type
            }
        }