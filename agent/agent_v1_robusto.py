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
MODELO = "gemma:2b"

# --- UTILITÁRIOS ---

def setup_selenium():
    """Configura o Chrome em modo headless."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
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
        text = text[start:end]
    
    # Remove quebras de linha que podem quebrar o JSON
    text = text.replace('\n', ' ').replace('\r', '')
    return text

def validar_conteudo_config(conteudo):
    """Verifica se o conteúdo do AppConfig é válido e não um placeholder."""
    if not conteudo or not isinstance(conteudo, str):
        return False
    if "TS code here" in conteudo:
        return False
    if "export const AppConfig" not in conteudo:
        return False
    if len(conteudo) < 50: # Muito curto para ser um config válido
        return False
    return True

def gerar_app_config_fallback(nome, url, imagens):
    """Gera um AppConfig padrão usando os dados extraídos, caso a IA falhe."""
    img1 = imagens[0] if len(imagens) > 0 else '/assets/images/feature.svg'
    img2 = imagens[1] if len(imagens) > 1 else '/assets/images/feature2.svg'
    
    return f"""export const AppConfig = {{
  site_name: '{nome}',
  title: '{nome} | Soluções de Qualidade',
  description: 'Conheça a {nome} e nossas soluções especializadas.',
  locale: 'pt-br',
  hero: {{
    title: 'Transforme seu Negócio com a {nome}',
    highlight: 'Excelência',
    description: 'Oferecemos as melhores soluções do mercado para atender suas necessidades com qualidade e eficiência.',
    button: 'Falar Conosco',
    buttonLink: '{url}',
  }},
  features: [
    {{
      title: 'Nossos Diferenciais',
      description: 'Compromisso com a qualidade e satisfação do cliente.',
      image: '{img1}',
      imageAlt: 'Destaque 1',
      reverse: false,
    }},
    {{
      title: 'Soluções Completas',
      description: 'Tecnologia e inovação para impulsionar seus resultados.',
      image: '{img2}',
      imageAlt: 'Destaque 2',
      reverse: true,
    }},
  ],
  cta: {{
    title: 'Pronto para começar?',
    subtitle: 'Entre em contato com nossa equipe hoje mesmo.',
    button: 'Solicitar Orçamento',
    link: '{url}',
  }},
  footer: {{
    company_name: '{nome}',
    contacts: ['Entre em contato pelo site oficial'],
  }},
}};"""

# --- CORE FUNCTIONS ---

def processar_cliente(nome, url, objetivo_especifico=None, cor_personalizada=None, modo_deploy=False):
    log = []
    
    def add_log(msg):
        print(msg)
        log.append(msg)

    add_log(f"🚀 Iniciando: {nome}")
    
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
        for tag in soup(["script", "style", "svg", "form", "footer", "nav", "header"]):
            tag.extract()
            
        text = soup.get_text(separator=' ', strip=True)[:3000]
        
        images = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if src and src.startswith('http') and not any(x in src.lower() for x in ['icon', 'logo', 'pixel']):
                images.append(src)
        
        if len(images) < 2:
            images = [
                "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=800&q=80",
                "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=800&q=80"
            ]
            
        site_data = {"text": text, "images": list(set(images))[:2], "url": url}
        
    except Exception as e:
        if driver: driver.quit()
        return {"status": "error", "log": log, "msg": f"Scrape Error: {str(e)}"}
    finally:
        if driver: driver.quit()

    # 2. IA GENERATION
    add_log(f"🧠 Pensando com {MODELO}...")
    
    prompt = f"""
    Você é um assistente JSON. Gere a configuração de um site.
    
    DADOS:
    Nome: {nome}
    Texto: "{site_data['text'][:500]}"
    Objetivo: "{objetivo_especifico if objetivo_especifico else 'Vender serviços'}"
    Img1: "{site_data['images'][0]}"
    Img2: "{site_data['images'][-1]}"
    
    Retorne APENAS um JSON válido neste formato exato (sem markdown):
    {{
        "app_config": "export const AppConfig = {{ site_name: '{nome}', title: 'Título Aqui', description: 'Descrição Aqui', locale: 'pt-br', hero: {{ title: 'Título Hero', highlight: 'Destaque', description: 'Descrição Hero', button: 'Botão', buttonLink: '#' }}, features: [ {{ title: 'Feature 1', description: 'Desc 1', image: '{site_data['images'][0]}', imageAlt: 'Img 1', reverse: false }}, {{ title: 'Feature 2', description: 'Desc 2', image: '{site_data['images'][-1]}', imageAlt: 'Img 2', reverse: true }} ], cta: {{ title: 'CTA Título', subtitle: 'CTA Subtítulo', button: 'Ação', link: '#' }}, footer: {{ company_name: '{nome}', contacts: ['Contato'] }} }};",
        "primary_color": "#03A9F4",
        "whatsapp_message": "Olá! Veja seu novo site."
    }}
    """
    
    json_res = {}
    config_code = ""
    
    try:
        response = requests.post(OLLAMA_API_URL, json={
            "model": MODELO,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.1, 
                "num_ctx": 4096,
                "num_predict": 1500
            }
        })
        
        if response.status_code == 200:
            raw_response = response.json()['response']
            clean_response = clean_json_string(raw_response)
            try:
                json_res = json.loads(clean_response)
                config_code = json_res.get('app_config', '')
            except:
                pass
                
    except Exception as e:
        add_log(f"⚠️ Erro IA: {str(e)}")

    # 3. ATUALIZAR ARQUIVOS (COM FALLBACK)
    add_log("💾 Salvando arquivos...")
    try:
        base_path = "." if os.path.exists("src") else ".."
        
        # LÓGICA DE FALLBACK CRÍTICA
        if not validar_conteudo_config(config_code):
            add_log("⚠️ IA gerou configuração inválida. Usando Fallback Seguro.")
            config_code = gerar_app_config_fallback(nome, url, site_data['images'])
            json_res['whatsapp_message'] = "Olá! Criei uma versão otimizada do seu site. O que acha?"
            json_res['primary_color'] = "#03A9F4"

        # Converte para string se ainda for objeto (segurança extra)
        if not isinstance(config_code, str):
             config_code = gerar_app_config_fallback(nome, url, site_data['images'])

        with open(f"{base_path}/src/utils/AppConfig.ts", "w", encoding="utf-8") as f:
            f.write(config_code)
            
        cor_final = cor_personalizada if cor_personalizada else json_res.get('primary_color', '#03A9F4')
        tw_path = f"{base_path}/tailwind.config.js"
        
        if os.path.exists(tw_path):
            with open(tw_path, "r", encoding="utf-8") as f: content = f.read()
            new_content = re.sub(r"500: '#[a-fA-F0-9]{6}'", f"500: '{cor_final}'", content)
            with open(tw_path, "w", encoding="utf-8") as f: f.write(new_content)
        
    except Exception as e:
        return {"status": "error", "log": log, "msg": f"Erro Arquivos: {str(e)}"}

    # 4. DEPLOY
    final_url = "http://localhost:3000"
    if modo_deploy:
        add_log("☁️ Deploy Vercel...")
        slug = re.sub(r'[^a-z0-9-]', '', nome.lower().replace(' ', '-'))[:30]
        cmd = f"vercel --prod --yes --force --name lp-{slug}"
        try:
            subprocess.run("npx prettier --write src/utils/AppConfig.ts", shell=True, stderr=subprocess.DEVNULL, cwd=base_path)
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300, cwd=base_path)
            if result.returncode == 0:
                urls = re.findall(r'https://[^\s]+\.vercel\.app', result.stdout)
                final_url = urls[0] if urls else "URL não encontrada"
            else:
                add_log(f"Erro Deploy: {result.stderr[:100]}")
        except Exception as e:
            final_url = f"Erro Deploy: {str(e)}"

    add_log("✅ Sucesso!")
    return {
        "status": "success", 
        "log": log, 
        "url": final_url, 
        "whatsapp": json_res.get('whatsapp_message', 'Olá!'),
        "color_used": cor_final
    }

if __name__ == "__main__":
    print("Use o Dashboard: streamlit run agent/dashboard.py")