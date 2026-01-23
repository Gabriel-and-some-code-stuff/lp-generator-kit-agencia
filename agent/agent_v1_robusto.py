import pandas as pd
import time
import os
import json
import re
import subprocess
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURAÇÕES ---
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODELO = "llama3"

# --- UTILITÁRIOS ---

def setup_selenium():
    """Configura o Chrome em modo headless."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # User agent para evitar bloqueios básicos
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        print(f"Erro no Driver: {e}")
        return None

def clean_json_string(text):
    """Limpa o output da IA para extrair apenas o JSON."""
    text = re.sub(r'```json', '', text, flags=re.IGNORECASE)
    text = re.sub(r'```', '', text)
    start = text.find('{')
    end = text.rfind('}') + 1
    if start != -1 and end != -1:
        return text[start:end]
    return text

# --- CORE FUNCTIONS (Chamadas pelo Dashboard) ---

def processar_cliente(nome, url, objetivo_especifico=None, cor_personalizada=None, modo_deploy=False):
    """
    Função principal que orquestra todo o processo para UM cliente.
    Retorna um dicionário com status e resultados.
    """
    log = [] # Lista para retornar logs para a UI
    
    def add_log(msg):
        print(msg)
        log.append(msg)

    add_log(f"🚀 Iniciando processamento para: {nome}")
    
    # 1. SCRAPE
    add_log(f"🕵️ Lendo site: {url}")
    site_data = None
    driver = setup_selenium()
    
    if not driver:
        return {"status": "error", "log": log, "msg": "Falha ao iniciar Chrome Driver"}

    try:
        driver.set_page_load_timeout(30)
        if not url.startswith('http'): url = 'https://' + url
        driver.get(url)
        time.sleep(3)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Remove lixo
        for tag in soup(["script", "style", "svg", "form", "footer", "nav"]):
            tag.extract()
            
        text = soup.get_text(separator=' ', strip=True)[:10000]
        
        # Imagens
        images = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if src and src.startswith('http') and not any(x in src.lower() for x in ['icon', 'logo', 'pixel']):
                images.append(src)
        
        # Fallback images se não achar nada
        if len(images) < 2:
            images = [
                "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=800&q=80",
                "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=800&q=80"
            ]
            
        site_data = {"text": text, "images": list(set(images))[:5], "url": url}
        
    except Exception as e:
        if driver: driver.quit()
        return {"status": "error", "log": log, "msg": f"Erro no Scrape: {str(e)}"}
    finally:
        if driver: driver.quit()

    # 2. IA GENERATION
    add_log(f"🧠 Raciocinando com {MODELO}...")
    
    prompt_sistema = """
    Você é um especialista em CRO. Gere um JSON estrito para configurar uma Landing Page.
    O JSON deve conter: 'app_config' (código TS completo), 'primary_color' (hex), 'whatsapp_message'.
    Use o Framework PAS (Problema-Agitação-Solução) nos textos.
    """
    
    prompt_usuario = f"""
    DADOS DO SITE: {site_data['url']}
    CONTEÚDO EXTRAÍDO: {site_data['text']}
    IMAGENS: {json.dumps(site_data['images'])}
    
    OBJETIVO ESTRATÉGICO DO CLIENTE (PRIORIDADE MÁXIMA): {objetivo_especifico if objetivo_especifico else "Vender mais serviços/produtos principais."}
    
    Gere o JSON de configuração.
    """
    
    try:
        add_log(f"📡 Conectando em: {OLLAMA_API_URL}")
        response = requests.post(OLLAMA_API_URL, json={
            "model": MODELO,
            "prompt": prompt_sistema + "\n" + prompt_usuario,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.6, "num_ctx": 8192}
        })
        
        if response.status_code != 200:
            # DEBUG DETALHADO AQUI
            error_details = f"Status: {response.status_code} | Resposta: {response.text}"
            add_log(f"❌ Erro Ollama: {error_details}")
            
            if response.status_code == 404:
                add_log("💡 DICA: O modelo 'llama3' pode não estar instalado. Rode 'ollama list' no terminal.")
                
            return {"status": "error", "log": log, "msg": f"Ollama recusou conexão. {error_details}"}
            
        json_res = json.loads(clean_json_string(response.json()['response']))
        
    except Exception as e:
        return {"status": "error", "log": log, "msg": f"Erro de Conexão IA: {str(e)}"}

    # 3. ATUALIZAR ARQUIVOS
    add_log("💾 Atualizando código fonte...")
    try:
        # Caminho relativo considerando execução da raiz ou folder agent
        base_path = "." if os.path.exists("src") else ".."
        
        # AppConfig
        config_code = json_res.get('app_config', '')
        if "export const AppConfig" not in config_code:
            # Fallback se a IA mandou só o objeto
            config_code = f"export const AppConfig = {json.dumps(config_code, indent=2)};"
            
        with open(f"{base_path}/src/utils/AppConfig.ts", "w", encoding="utf-8") as f:
            f.write(config_code)
            
        # Tailwind Color (Prioridade: Cor da UI > Cor da IA)
        cor_final = cor_personalizada if cor_personalizada else json_res.get('primary_color', '#03A9F4')
        
        tw_path = f"{base_path}/tailwind.config.js"
        with open(tw_path, "r", encoding="utf-8") as f: content = f.read()
        new_content = re.sub(r"500: '#.*?'", f"500: '{cor_final}'", content)
        with open(tw_path, "w", encoding="utf-8") as f: f.write(new_content)
        
    except Exception as e:
        return {"status": "error", "log": log, "msg": f"Erro Arquivos: {str(e)}"}

    # 4. DEPLOY (Opcional - V2)
    final_url = "http://localhost:3000 (Modo Local)"
    if modo_deploy:
        add_log("☁️ Iniciando Deploy Vercel...")
        
        # Nome do projeto
        slug = re.sub(r'[^a-z0-9-]', '', nome.lower().replace(' ', '-'))[:30]
        cmd = f"vercel --prod --yes --force --name lp-{slug}"
        
        try:
            # Roda prettier antes
            subprocess.run("npx prettier --write src/utils/AppConfig.ts", shell=True, stderr=subprocess.DEVNULL, cwd=base_path)
            
            # Deploy
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300, cwd=base_path)
            
            if result.returncode == 0:
                urls = re.findall(r'https://[^\s]+\.vercel\.app', result.stdout)
                final_url = urls[0] if urls else "URL não encontrada"
            else:
                add_log(f"Erro Deploy Output: {result.stderr[:200]}")
                final_url = "Erro no Deploy"
        except Exception as e:
            final_url = f"Erro Deploy Script: {str(e)}"

    add_log("✅ Processo Finalizado!")
    
    # 5. RETORNO PARA UI
    return {
        "status": "success",
        "log": log,
        "url": final_url,
        "whatsapp": json_res.get('whatsapp_message', 'Olá!'),
        "color_used": cor_final
    }

# Função de compatibilidade para rodar via terminal direto
if __name__ == "__main__":
    print("Execute 'streamlit run agent/dashboard.py' para usar a interface.")