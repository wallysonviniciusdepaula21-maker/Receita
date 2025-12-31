"""
Script para importar dados da base Excel para MongoDB
Importa os 98.000 registros (ou subconjunto) para consulta rápida
"""
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorClient
import os
import asyncio
from datetime import datetime
import random
import re

async def importar_base_para_mongodb(limite=None):
    """Importa dados do Excel para MongoDB"""
    
    # Conexão MongoDB
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'test_database')]
    collection = db.cpf_cache
    
    print("=" * 80)
    print("📊 IMPORTANDO DADOS PARA MONGODB")
    print("=" * 80)
    
    # Carregar Excel
    print("\n📂 Carregando base_98000_scraped.xlsx...")
    df = pd.read_excel('/app/base_98000_scraped.xlsx')
    
    if limite:
        df = df.head(limite)
    
    print(f"✅ {len(df)} registros carregados")
    
    # Processar e importar
    importados = 0
    erros = 0
    duplicados = 0
    
    for idx, row in df.iterrows():
        try:
            cpf = str(row['scraped_cpf']).strip() if pd.notna(row['scraped_cpf']) else ''
            nome = str(row['scraped_nome']).strip() if pd.notna(row['scraped_nome']) else ''
            data_nasc = str(row['scraped_data_nascimento']).strip() if pd.notna(row['scraped_data_nascimento']) else ''
            telefone = str(row['Celular']).strip() if pd.notna(row['Celular']) else ''
            
            # Validar CPF
            if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
                continue
            
            # Verificar se já existe
            existe = await collection.find_one({"cpf": cpf})
            if existe:
                duplicados += 1
                continue
            
            # Gerar protocolo único
            protocolo = f"CTP{random.randint(1000000, 9999999)}"
            
            # Preparar documento
            documento = {
                "cpf": cpf,
                "name": nome,
                "birthDate": data_nasc,
                "status": "IRREGULAR",  # Todos da base são irregulares
                "declaration2023": "NÃO ENTREGUE",
                "protocol": protocolo,
                "deadline": datetime.now().strftime("%d/%m/%Y"),  # Prazo é hoje
                "statusType": "CRÍTICO",
                "telefone": telefone,
                "consulted_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # Inserir no MongoDB
            await collection.insert_one(documento)
            importados += 1
            
            # Log de progresso
            if (importados % 500) == 0:
                print(f"  Progresso: {importados}/{len(df)} ({importados/len(df)*100:.1f}%)")
        
        except Exception as e:
            erros += 1
            if erros < 5:  # Mostrar apenas primeiros erros
                print(f"  ⚠️ Erro no registro {idx}: {e}")
    
    print("\n" + "=" * 80)
    print("✅ IMPORTAÇÃO CONCLUÍDA!")
    print("=" * 80)
    print(f"  Importados: {importados}")
    print(f"  Duplicados (pulados): {duplicados}")
    print(f"  Erros: {erros}")
    print(f"  Total no banco: {await collection.count_documents({})}")
    print("=" * 80)
    
    await client.close()
    return {"importados": importados, "duplicados": duplicados, "erros": erros}

if __name__ == "__main__":
    # Importar os 3000 primeiros (ou todos se quiser)
    asyncio.run(importar_base_para_mongodb(limite=3000))
