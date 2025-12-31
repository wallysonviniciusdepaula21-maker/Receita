from fastapi import APIRouter, BackgroundTasks
from services.pre_consulta_service import pre_consulta_service

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/pre-consultar")
async def iniciar_pre_consulta(background_tasks: BackgroundTasks):
    """Inicia pré-consulta dos 3000 CPFs em background"""
    
    status = await pre_consulta_service.get_status()
    
    if status["em_progresso"]:
        return {
            "message": "Pré-consulta já em andamento",
            "status": status
        }
    
    # Executar em background
    background_tasks.add_task(pre_consulta_service.pre_consultar_3000)
    
    return {
        "success": True,
        "message": "Pré-consulta iniciada em background",
        "info": "Use /admin/status para acompanhar o progresso"
    }

@router.get("/status")
async def status_pre_consulta():
    """Retorna status da pré-consulta"""
    return await pre_consulta_service.get_status()

@router.get("/cache-count")
async def contar_cache():
    """Retorna quantos CPFs estão em cache"""
    from motor.motor_asyncio import AsyncIOMotorClient
    import os
    
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'test_database')]
    
    total = await db.cpf_cache.count_documents({})
    
    return {
        "total_em_cache": total,
        "message": f"{total} CPFs disponíveis para consulta instantânea"
    }
