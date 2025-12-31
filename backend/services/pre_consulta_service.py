"""
Serviço de pré-consulta e cache de CPFs
Consulta CPFs em background e salva no MongoDB para respostas rápidas
"""
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorClient
import os
import asyncio
from datetime import datetime
from services.yan_buscas_service import yan_buscas_service
from services.cpf_service import CPFService

class PreConsultaService:
    """Serviço para pré-consultar CPFs e armazenar em cache"""
    
    def __init__(self):
        # Conexão MongoDB
        mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client[os.environ.get('DB_NAME', 'test_database')]
        self.collection = self.db.cpf_cache
        
        # Estatísticas
        self.total_cpfs = 0
        self.consultados = 0
        self.erros = 0
        self.em_progresso = False
    
    async def get_status(self):
        """Retorna status da pré-consulta"""
        total_cache = await self.collection.count_documents({})
        
        return {
            "em_progresso": self.em_progresso,
            "total_cpfs": self.total_cpfs,
            "consultados": self.consultados,
            "em_cache": total_cache,
            "erros": self.erros,
            "progresso_percentual": (self.consultados / self.total_cpfs * 100) if self.total_cpfs > 0 else 0
        }
    
    async def consultar_cpf_com_cache(self, cpf: str):
        """Verifica cache primeiro, se não encontrar consulta no Yan Buscas"""
        
        # Remover formatação do CPF
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        
        # Buscar no cache primeiro
        cached = await self.collection.find_one(
            {"cpf": {"$regex": cpf_limpo}},
            {"_id": 0}
        )
        
        if cached:
            print(f"[Cache] ✓ CPF encontrado no cache: {cpf}")
            return {
                "success": True,
                "data": {
                    "name": cached["name"],
                    "cpf": cached["cpf"],
                    "birthDate": cached["birthDate"],
                    "status": cached["status"],
                    "declaration2023": cached["declaration2023"],
                    "protocol": cached["protocol"],
                    "deadline": cached["deadline"],
                    "statusType": cached["statusType"]
                },
                "from_cache": True
            }
        
        # Se não está no cache, consulta no Yan Buscas
        print(f"[Cache] CPF não encontrado no cache, consultando Yan Buscas: {cpf}")
        result = await CPFService.consultar_cpf(cpf)
        
        # Salvar no cache para próximas consultas
        if result.get("success"):
            data = result["data"]
            await self.collection.update_one(
                {"cpf": data["cpf"]},
                {
                    "$set": {
                        "cpf": data["cpf"],
                        "name": data["name"],
                        "birthDate": data["birthDate"],
                        "status": data["status"],
                        "declaration2023": data["declaration2023"],
                        "protocol": data["protocol"],
                        "deadline": data["deadline"],
                        "statusType": data["statusType"],
                        "updated_at": datetime.utcnow()
                    },
                    "$setOnInsert": {
                        "consulted_at": datetime.utcnow()
                    }
                },
                upsert=True
            )
            print(f"[Cache] ✓ CPF salvo no cache: {cpf}")
        
        result["from_cache"] = False
        return result
    
    async def pre_consultar_3000(self):
        """Pré-consulta os 3000 CPFs do arquivo Excel em background"""
        
        if self.em_progresso:
            return {"error": "Pré-consulta já em andamento"}
        
        self.em_progresso = True
        self.consultados = 0
        self.erros = 0
        
        try:
            # Carregar arquivo Excel
            df = pd.read_excel('/app/mensagens_3000_PRONTO.xlsx')
            cpfs = df['cpf'].unique().tolist()
            self.total_cpfs = len(cpfs)
            
            print(f"[PreConsulta] Iniciando pré-consulta de {self.total_cpfs} CPFs...")
            
            for idx, cpf in enumerate(cpfs):
                try:
                    # Verificar se já está no cache
                    cpf_limpo = ''.join(filter(str.isdigit, cpf))
                    existe = await self.collection.find_one({"cpf": {"$regex": cpf_limpo}})
                    
                    if existe:
                        print(f"[PreConsulta] {idx+1}/{self.total_cpfs} - {cpf} já em cache, pulando...")
                        self.consultados += 1
                        continue
                    
                    # Consultar no Yan Buscas
                    print(f"[PreConsulta] {idx+1}/{self.total_cpfs} - Consultando {cpf}...")
                    result = await CPFService.consultar_cpf(cpf)
                    
                    if result.get("success"):
                        # Salvar no cache
                        data = result["data"]
                        await self.collection.insert_one({
                            "cpf": data["cpf"],
                            "name": data["name"],
                            "birthDate": data["birthDate"],
                            "status": data["status"],
                            "declaration2023": data["declaration2023"],
                            "protocol": data["protocol"],
                            "deadline": data["deadline"],
                            "statusType": data["statusType"],
                            "consulted_at": datetime.utcnow(),
                            "updated_at": datetime.utcnow()
                        })
                        print(f"[PreConsulta] ✓ {cpf} consultado e salvo")
                        self.consultados += 1
                    else:
                        print(f"[PreConsulta] ✗ Erro ao consultar {cpf}")
                        self.erros += 1
                    
                    # Aguardar um pouco entre consultas (evitar sobrecarga)
                    await asyncio.sleep(2)
                
                except Exception as e:
                    print(f"[PreConsulta] ✗ Erro em {cpf}: {e}")
                    self.erros += 1
                
                # Log de progresso a cada 50 CPFs
                if (idx + 1) % 50 == 0:
                    progresso = (idx + 1) / self.total_cpfs * 100
                    print(f"[PreConsulta] Progresso: {progresso:.1f}% ({idx+1}/{self.total_cpfs})")
            
            print(f"[PreConsulta] ✓ Concluído! {self.consultados} consultados, {self.erros} erros")
        
        except Exception as e:
            print(f"[PreConsulta] ✗ Erro fatal: {e}")
        
        finally:
            self.em_progresso = False
        
        return {
            "success": True,
            "total": self.total_cpfs,
            "consultados": self.consultados,
            "erros": self.erros
        }

# Instância global
pre_consulta_service = PreConsultaService()
