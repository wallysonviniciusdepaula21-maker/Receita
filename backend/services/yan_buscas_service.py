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
        self.password = os.environ.get('YANBUSCAS_PASS', 'ip1012')
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
            args=['--no-sandbox', '--disable-setuid-sandbox']
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
            await self.page.fill('input[name="username"], input[type="text"]', self.username)
            await self.page.fill('input[name="password"], input[type="password"]', self.password)
            
            # Clica no botão de login
            await self.page.click('button[type="submit"], button:has-text("Entrar"), button:has-text("Login")')
            
            # Aguarda redirecionamento para dashboard
            await self.page.wait_for_url('**/dashboard**', timeout=15000)
            
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
            
            # Navega para o módulo CPF (Consulta básica)
            # Procura pelo card/botão "CPF" ou "Consulta básica"
            await self.page.goto('https://yanbuscas.com/dashboard', wait_until='networkidle')
            
            # Clica no módulo CPF
            await self.page.click('a:has-text("CPF"), button:has-text("CPF"), div:has-text("CPF")')
            await self.page.wait_for_timeout(2000)
            
            # Preenche o CPF
            await self.page.fill('input[placeholder*="CPF"], input[name*="cpf"]', cpf_clean)
            
            # Clica em Consultar
            await self.page.click('button:has-text("Consultar"), button:has-text("Buscar")')
            
            # Aguarda resultado
            await self.page.wait_for_timeout(3000)
            
            # Extrai NOME e DATA DE NASCIMENTO do resultado
            # Procura por elementos que contenham "NOME:" e "NASCIMENTO:"
            page_content = await self.page.content()
            
            nome = None
            data_nascimento = None
            
            # Tenta extrair usando diferentes seletores
            try:
                # Método 1: Procurar por texto específico
                nome_element = await self.page.query_selector('text=NOME:')
                if nome_element:
                    parent = await nome_element.evaluate('el => el.parentElement.innerText')
                    nome = parent.replace('NOME:', '').strip()
                
                nasc_element = await self.page.query_selector('text=NASCIMENTO:')
                if nasc_element:
                    parent = await nasc_element.evaluate('el => el.parentElement.innerText')
                    data_nascimento = parent.replace('NASCIMENTO:', '').strip()
            except:
                pass
            
            # Método 2: Regex no conteúdo da página
            if not nome:
                import re
                nome_match = re.search(r'NOME[:\s]+([A-Z\s]+)', page_content)
                if nome_match:
                    nome = nome_match.group(1).strip()
                
                nasc_match = re.search(r'NASCIMENTO[:\s]+(\d{2}/\d{2}/\d{4})', page_content)
                if nasc_match:
                    data_nascimento = nasc_match.group(1).strip()
            
            if nome and data_nascimento:
                print(f"[YanBuscas] Dados encontrados - Nome: {nome}, Nasc: {data_nascimento}")
                return {
                    'success': True,
                    'nome': nome,
                    'data_nascimento': data_nascimento
                }
            else:
                print(f"[YanBuscas] Dados não encontrados na página")
                return {'success': False, 'error': 'Dados não encontrados'}
                
        except Exception as e:
            print(f"[YanBuscas] Erro ao consultar CPF: {e}")
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