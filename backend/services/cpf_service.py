from models.cpf import CPFData
from datetime import datetime
import random
import hashlib
import requests

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
    def gerar_nome_generico(cpf: str) -> str:
        """Gera nome genérico mas consistente baseado no CPF"""
        cpf_numbers = ''.join(filter(str.isdigit, cpf))
        
        nomes = [
            "João Silva Santos", "Maria Oliveira Costa", "José Santos Lima",
            "Ana Paula Ferreira", "Carlos Eduardo Souza", "Juliana Alves Pereira",
            "Pedro Henrique Rodrigues", "Fernanda Costa Martins", "Lucas Almeida Santos",
            "Mariana Santos Silva", "Rafael Oliveira Costa", "Gabriela Lima Souza",
            "Felipe Santos Rodrigues", "Camila Ferreira Alves", "Bruno Costa Lima",
            "Larissa Oliveira Santos", "Thiago Silva Costa", "Beatriz Almeida Ferreira",
            "Rodrigo Santos Oliveira", "Natália Costa Silva", "Guilherme Lima Santos",
            "Isabela Ferreira Costa", "Matheus Oliveira Lima", "Amanda Santos Silva"
        ]
        
        # Usa CPF como seed para escolher nome consistente
        index = int(cpf_numbers[:3]) % len(nomes)
        return nomes[index]
    
    @staticmethod
    def gerar_data_nascimento(cpf: str) -> str:
        """Gera data de nascimento consistente baseado no CPF"""
        cpf_numbers = ''.join(filter(str.isdigit, cpf))
        
        # Usa dígitos do CPF para gerar data
        dia = (int(cpf_numbers[0:2]) % 28) + 1  # 1-28
        mes = (int(cpf_numbers[2:4]) % 12) + 1  # 1-12
        ano = 1950 + (int(cpf_numbers[4:6]) % 50)  # 1950-1999
        
        return f"{dia:02d}/{mes:02d}/{ano}"
    
    @staticmethod
    async def buscar_nome_receita(cpf: str) -> dict:
        """Tenta buscar nome na Receita Federal (API gratuita)"""
        try:
            cpf_numbers = ''.join(filter(str.isdigit, cpf))
            # API gratuita da ReceitaWS (pode ter limitação de requisições)
            url = f"https://www.receitaws.com.br/v1/cpf/{cpf_numbers}"
            
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'OK' and data.get('nome'):
                    return {
                        'success': True,
                        'nome': data.get('nome'),
                        'data_nascimento': data.get('data_nascimento', '')
                    }
        except Exception as e:
            print(f"Erro ao consultar ReceitaWS: {e}")
        
        return {'success': False}
    
    @staticmethod
    async def consultar_cpf(cpf: str) -> dict:
        """Consulta CPF e retorna dados (real ou gerado)"""
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
        
        # Tenta buscar nome real na Receita Federal
        resultado_receita = await CPFService.buscar_nome_receita(cpf_clean)
        
        if resultado_receita['success']:
            # Usa dados reais da Receita
            nome = resultado_receita['nome']
            data_nascimento = resultado_receita.get('data_nascimento') or CPFService.gerar_data_nascimento(cpf_clean)
        else:
            # Gera dados consistentes baseados no CPF
            nome = CPFService.gerar_nome_generico(cpf_clean)
            data_nascimento = CPFService.gerar_data_nascimento(cpf_clean)
        
        # Gera protocolo consistente
        protocol = CPFService.gerar_protocolo(cpf_clean)
        
        # Define status baseado em algum critério (exemplo: CPFs pares são irregulares)
        ultimo_digito = int(cpf_clean[-1])
        status = "IRREGULAR" if ultimo_digito % 2 == 0 else "REGULAR"
        declaration = "NÃO ENTREGUE" if status == "IRREGULAR" else "ENTREGUE"
        status_type = "CRÍTICO" if status == "IRREGULAR" else "NORMAL"
        
        return {
            "success": True,
            "data": {
                "name": nome,
                "cpf": cpf_formatado,
                "birthDate": data_nascimento,
                "status": status,
                "declaration2023": declaration,
                "protocol": protocol,
                "deadline": "20/12/2025",
                "statusType": status_type
            }
        }