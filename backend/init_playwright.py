"""
Módulo de inicialização - Garante que Playwright está instalado
"""
import subprocess
import sys
import os
from pathlib import Path

def ensure_playwright_installed():
    """Garante que o Playwright está instalado antes de iniciar o servidor"""
    
    # Verificar se os navegadores já estão instalados
    browser_path = Path("/pw-browsers/chromium-1200")
    
    if not browser_path.exists():
        print("=" * 80)
        print("🔧 INSTALANDO PLAYWRIGHT CHROMIUM...")
        print("=" * 80)
        
        try:
            # Instalar navegadores do Playwright
            result = subprocess.run(
                ["playwright", "install", "chromium"],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos
            )
            
            if result.returncode == 0:
                print("✅ Playwright Chromium instalado com sucesso!")
            else:
                print(f"⚠️ Aviso ao instalar Playwright: {result.stderr}")
                # Tentar instalar dependências do sistema
                subprocess.run(
                    ["playwright", "install-deps", "chromium"],
                    capture_output=True,
                    timeout=300
                )
                # Tentar novamente
                subprocess.run(
                    ["playwright", "install", "chromium"],
                    capture_output=True,
                    timeout=300
                )
                print("✅ Playwright instalado (segunda tentativa)")
        
        except Exception as e:
            print(f"⚠️ Erro ao instalar Playwright: {e}")
            print("⚠️ Sistema continuará, mas scraping pode não funcionar")
    else:
        print("✅ Playwright já instalado, pulando instalação...")

# Executar na importação do módulo
if __name__ != "__main__":
    ensure_playwright_installed()
