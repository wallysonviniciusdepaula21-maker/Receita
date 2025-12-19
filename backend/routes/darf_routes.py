from fastapi import APIRouter, HTTPException
from services.darf_service import DARFService

router = APIRouter(prefix="/darf", tags=["DARF"])

@router.get("/{protocol}")
async def obter_darf(protocol: str):
    """Obtém DARF pelo protocolo"""
    try:
        result = await DARFService.gerar_darf(protocol)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))