#!/bin/bash
# Script para instalar navegadores Playwright no deploy

echo "🔧 Instalando navegadores Playwright..."

# Instalar Chromium
playwright install chromium --with-deps

# Verificar se foi instalado
if [ $? -eq 0 ]; then
    echo "✅ Chromium instalado com sucesso!"
else
    echo "❌ Erro ao instalar Chromium"
    exit 1
fi

echo "✅ Setup completo!"
