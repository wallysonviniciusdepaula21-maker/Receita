from playwright.async_api import async_playwright, Browser, Page
import asyncio
from typing import Optional, Dict
import os
from datetime import datetime

class YanBuscasService:
    """Serviço para consultar CPF no Yan Buscas"""
    
    def __init__(self):
        self.url_login = "https://yanbuscas.com/login"
        self.username = os.environ.get('YANBUSCAS_USER', 'joapedrs')
        self.password = os.environ.get('YANBUSCAS_PASS', 'jp1012')  # Senha correta
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.logged_in = False
        self.playwright = None
    
    async def iniciar_browser(self):
        """Inicia o navegador e faz login"""
        if self.browser:
            return
        
        print("[YanBuscas] Iniciando navegador...")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            executable_path='/pw-browsers/chromium-1200/chrome-linux/chrome',
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
        )
        self.page = await self.browser.new_page()
        await self.fazer_login()
    
    async def fazer_login(self):
        """Realiza login no Yan Buscas"""
        if self.logged_in:
            return
        
        try:
            print(f"[YanBuscas] Fazendo login em {self.url_login}")
            await self.page.goto(self.url_login, wait_until='networkidle', timeout=30000)
            
            # Preenche credenciais
            await self.page.fill('input[name="username"]', self.username)
            await self.page.fill('input[name="password"]', self.password)
            
            # Clica no botão de login
            await self.page.click('button[type="submit"]')
            
            # Aguarda redirecionamento para home (não dashboard)
            await self.page.wait_for_url('**/home**', timeout=30000)
            
            print("[YanBuscas] Login realizado com sucesso!")
            self.logged_in = True
            
        except Exception as e:
            print(f"[YanBuscas] Erro ao fazer login: {e}")
            raise Exception(f"Falha no login: {e}")
    
    async def consultar_cpf(self, cpf: str) -> Dict:
        """Consulta CPF e retorna nome e data de nascimento"""
        try:
            # Garante que está logado
            await self.iniciar_browser()
            
            cpf_clean = ''.join(filter(str.isdigit, cpf))
            print(f"[YanBuscas] Consultando CPF: {cpf_clean}")
            
            # Navega diretamente para o módulo CPF
            cpf_url = "https://yanbuscas.com/consultar?tipo=CPF"
            await self.page.goto(cpf_url, wait_until='networkidle', timeout=30000)
            await self.page.wait_for_timeout(2000)
            
            # Preenche o CPF no campo de texto
            await self.page.fill('input[type="text"]', cpf_clean)
            await self.page.wait_for_timeout(1000)
            
            # Clica em Consultar
            await self.page.click('button:has-text("Consultar")')
            
            # Aguarda resultado (pode demorar)
            await self.page.wait_for_timeout(5000)
            
            # Extrai o texto visível da página
            page_text = await self.page.evaluate('() => document.body.innerText')
            
            # Extrai NOME e DATA DE NASCIMENTO usando regex
            import re
            
            nome = None
            data_nascimento = None
            
            # Buscar NOME (formato: "NOME: XXXXX")
            nome_match = re.search(r'NOME:\s*([A-Z\s]+?)(?:\n|CPF:)', page_text)
            if nome_match:
                nome = nome_match.group(1).strip()
            
            # Buscar NASCIMENTO (formato: "NASCIMENTO: DD/MM/YYYY")
            nasc_match = re.search(r'NASCIMENTO:\s*(\d{2}/\d{2}/\d{4})', page_text)
            if nasc_match:
                data_nascimento = nasc_match.group(1).strip()
            
            if nome and data_nascimento:
                print(f"[YanBuscas] ✓ Dados encontrados - Nome: {nome}, Nasc: {data_nascimento}")
                return {
                    'success': True,
                    'nome': nome,
                    'data_nascimento': data_nascimento
                }
            else:
                print(f"[YanBuscas] ⚠ Dados não encontrados")
                print(f"[YanBuscas] Texto da página: {page_text[:500]}")
                return {'success': False, 'error': 'Dados não encontrados no resultado'}
                
        except Exception as e:
            print(f"[YanBuscas] ✗ Erro ao consultar CPF: {e}")
            return {'success': False, 'error': str(e)}
    
    async def fechar(self):
        """Fecha o navegador"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        self.browser = None
        self.page = None
        self.logged_in = False
        print("[YanBuscas] Navegador fechado")

# Instância global para reutilizar sessão
yan_buscas_service = YanBuscasService()