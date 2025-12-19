#!/usr/bin/env python3
"""Script de teste para debugar integração Yan Buscas"""
import asyncio
from playwright.async_api import async_playwright
import os

async def testar_yan_buscas():
    cpf = "10362198950"
    username = "joapedrs"
    password = "jp1012"  # Senha correta
    
    print(f"[TESTE] Iniciando teste com CPF: {cpf}")
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=True,  # Headless porque não temos display
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )
    
    page = await browser.new_page()
    
    try:
        # 1. LOGIN
        print(f"\n[1] Acessando página de login...")
        await page.goto("https://yanbuscas.com/login", wait_until='networkidle', timeout=30000)
        await page.screenshot(path='/tmp/step1_login_page.png')
        print(f"    Screenshot salvo: step1_login_page.png")
        
        # Verificar campos disponíveis
        print(f"\n[2] Verificando campos de login...")
        await page.wait_for_timeout(2000)
        
        # Tentar diferentes seletores
        inputs = await page.query_selector_all('input')
        print(f"    Encontrados {len(inputs)} campos input")
        
        for i, inp in enumerate(inputs):
            input_type = await inp.get_attribute('type')
            input_name = await inp.get_attribute('name')
            input_placeholder = await inp.get_attribute('placeholder')
            print(f"    Input {i}: type={input_type}, name={input_name}, placeholder={input_placeholder}")
        
        # Preencher username
        print(f"\n[3] Preenchendo username: {username}")
        username_selectors = [
            'input[name="username"]',
            'input[type="text"]',
            'input[placeholder*="usuário" i]',
            'input[placeholder*="user" i]'
        ]
        
        for selector in username_selectors:
            try:
                await page.fill(selector, username, timeout=2000)
                print(f"    ✓ Username preenchido com seletor: {selector}")
                break
            except:
                continue
        
        # Preencher password
        print(f"\n[4] Preenchendo senha...")
        await page.fill('input[type="password"]', password)
        print(f"    ✓ Senha preenchida")
        
        await page.screenshot(path='/tmp/step2_credentials_filled.png')
        
        # Clicar em login
        print(f"\n[5] Clicando em botão de login...")
        button_selectors = [
            'button[type="submit"]',
            'button:has-text("Entrar")',
            'button:has-text("Login")',
            'input[type="submit"]'
        ]
        
        for selector in button_selectors:
            try:
                await page.click(selector, timeout=2000)
                print(f"    ✓ Clicou em: {selector}")
                break
            except:
                continue
        
        # Aguardar redirecionamento
        print(f"\n[6] Aguardando redirecionamento...")
        await page.wait_for_timeout(5000)
        current_url = page.url
        print(f"    URL atual: {current_url}")
        
        # Verificar se houve erro de login
        page_text = await page.evaluate('() => document.body.innerText')
        if 'incorreto' in page_text.lower() or 'inválido' in page_text.lower() or 'erro' in page_text.lower():
            print(f"    ⚠ POSSÍVEL ERRO DE LOGIN detectado")
            print(f"    Mensagem: {page_text[:500]}")
        
        await page.screenshot(path='/tmp/step3_after_login.png')
        
        # 7. PROCURAR MÓDULO CPF
        print(f"\n[7] Procurando módulo CPF (Consulta Básica)...")
        
        # Tentar acessar diretamente a URL do módulo CPF
        cpf_url = "https://yanbuscas.com/consultar?tipo=CPF"
        print(f"    Acessando URL direta: {cpf_url}")
        await page.goto(cpf_url, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(3000)
        print(f"    URL atual: {page.url}")
        await page.screenshot(path='/tmp/step4_cpf_module.png')
        
        # 8. PREENCHER CPF
        print(f"\n[8] Procurando campo de CPF...")
        
        # Tentar múltiplos seletores
        all_inputs = await page.query_selector_all('input')
        print(f"    Encontrados {len(all_inputs)} campos input na página")
        
        for i, inp in enumerate(all_inputs):
            input_type = await inp.get_attribute('type')
            input_name = await inp.get_attribute('name')
            input_placeholder = await inp.get_attribute('placeholder')
            input_id = await inp.get_attribute('id')
            print(f"    Input {i}: type={input_type}, name={input_name}, id={input_id}, placeholder={input_placeholder}")
        
        # Tentar preencher o primeiro input de texto
        text_inputs = await page.query_selector_all('input[type="text"], input:not([type])')
        
        if text_inputs:
            print(f"    Preenchendo CPF no primeiro campo de texto: {cpf}")
            await text_inputs[0].fill(cpf)
            await page.wait_for_timeout(1000)
            await page.screenshot(path='/tmp/step5_cpf_filled.png')
            
            # 9. CLICAR EM CONSULTAR
            print(f"\n[9] Procurando botão de consulta...")
            search_buttons = await page.query_selector_all('button:has-text("Consultar"), button:has-text("Buscar"), button:has-text("Pesquisar")')
            
            if search_buttons:
                print(f"    Clicando em consultar...")
                await search_buttons[0].click()
                await page.wait_for_timeout(5000)
                await page.screenshot(path='/tmp/step6_result.png')
                
                # 10. EXTRAIR RESULTADO
                print(f"\n[10] Extraindo resultado...")
                result_content = await page.content()
                
                # Salvar HTML para análise
                with open('/tmp/result_page.html', 'w', encoding='utf-8') as f:
                    f.write(result_content)
                print(f"    HTML salvo em: result_page.html")
                
                # Procurar por NOME e DATA DE NASCIMENTO
                import re
                
                # Buscar NOME
                nome_patterns = [
                    r'NOME[:\s]*([A-Z\s]+)',
                    r'Nome[:\s]*([A-Z][a-z\s]+)',
                    r'nome[:\s]*([A-Z][a-z\s]+)'
                ]
                
                for pattern in nome_patterns:
                    match = re.search(pattern, result_content)
                    if match:
                        print(f"    ✓ NOME encontrado: {match.group(1).strip()}")
                        break
                
                # Buscar DATA DE NASCIMENTO
                nasc_patterns = [
                    r'NASCIMENTO[:\s]*(\d{2}/\d{2}/\d{4})',
                    r'Data\s+de\s+Nascimento[:\s]*(\d{2}/\d{2}/\d{4})',
                    r'Nascimento[:\s]*(\d{2}/\d{2}/\d{4})'
                ]
                
                for pattern in nasc_patterns:
                    match = re.search(pattern, result_content)
                    if match:
                        print(f"    ✓ DATA encontrada: {match.group(1)}")
                        break
                
                # Tentar pegar todo texto visível
                print(f"\n[11] Texto visível na página:")
                body_text = await page.evaluate('() => document.body.innerText')
                print(body_text[:1000])  # Primeiros 1000 caracteres
        
        print(f"\n[TESTE] Finalizado! Verifique os screenshots em /tmp/")
        print(f"        step1_login_page.png")
        print(f"        step2_credentials_filled.png")
        print(f"        step3_after_login.png")
        print(f"        step4_cpf_module.png")
        print(f"        step5_cpf_filled.png")
        print(f"        step6_result.png")
        
        await page.wait_for_timeout(5000)  # Esperar para ver
        
    except Exception as e:
        print(f"\n[ERRO] {e}")
        await page.screenshot(path='/tmp/error_screenshot.png')
    
    finally:
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    asyncio.run(testar_yan_buscas())
