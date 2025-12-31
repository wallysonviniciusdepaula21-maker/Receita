#!/bin/bash
# Script de inicialização - Instala Playwright automaticamente

echo "🚀 Iniciando setup do servidor..."

# Verificar se o Playwright já está instalado
if [ ! -d "/pw-browsers/chromium-1200" ]; then
    echo "📦 Instalando Playwright Chromium..."
    playwright install chromium --with-deps 2>/dev/null || playwright install chromium
    echo "✅ Playwright instalado!"
else
    echo "✅ Playwright já instalado, pulando instalação..."
fi

# Iniciar o servidor FastAPI
echo "🚀 Iniciando servidor FastAPI..."
exec uvicorn server:app --host 0.0.0.0 --port 8001 --reload
