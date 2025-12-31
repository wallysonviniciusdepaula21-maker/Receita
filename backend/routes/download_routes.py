from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter(prefix="/download", tags=["Download"])

@router.get("/mensagens-3000")
async def download_mensagens_3000():
    """Download do arquivo com 3000 mensagens"""
    file_path = "/app/mensagens_3000.csv"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    return FileResponse(
        path=file_path,
        filename="mensagens_whatsapp_3000.csv",
        media_type="text/csv"
    )

@router.get("/mensagens-completo")
async def download_mensagens_completo():
    """Download do arquivo completo com 97k mensagens"""
    file_path = "/app/mensagens_whatsapp_base_98k.csv"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    return FileResponse(
        path=file_path,
        filename="mensagens_whatsapp_completo.csv",
        media_type="text/csv"
    )

@router.get("/cpf-telefone")
async def download_cpf_telefone():
    """Download do arquivo com CPF e telefone consolidado"""
    file_path = "/app/cpf_telefone_consolidado.txt"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    return FileResponse(
        path=file_path,
        filename="cpf_telefone_consolidado.txt",
        media_type="text/plain"
    )
