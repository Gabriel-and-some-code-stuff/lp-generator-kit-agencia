import pandas as pd
import time
import os
import json
import re
import subprocess
import requests
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURAÇÕES ---
OLLAMA_API_URL = "http://localhost:11434/api/generate"
# Usando Qwen 7B -> Excelente balanceamento entre performance e inteligência
MODELO = "qwen" 
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Raiz do projeto

# --- TEMPLATE PADRÃO (Para Reset e Fallback) ---
DEFAULT_APP_CONFIG = """
export const AppConfig = {
  site_name: 'Landing Page Generator',
  title: 'Soluções de Alto Impacto para seu Negócio',
  description: 'Aumente suas vendas e autoridade com nossa estratégia digital.',
  locale: 'pt-br',
  primary_color: '#0ea5e9', // Sky 500
  hero: {
    title: 'Transforme Visitantes em Clientes',
    highlight: 'Resultados Reais',
    description: 'Nossa metodologia comprovada ajuda empresas a escalarem suas operações com previsibilidade e segurança.',
    button: 'Agendar Consultoria',
    buttonLink: '#',
    image: 'https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=1200&q=80',
  },
  features: [
    {
      title: 'Estratégia Personalizada',
      description: 'Não acreditamos em receitas prontas. Criamos um plano único para o seu momento.',
      image: 'https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=800&q=80',
      imageAlt: 'Estratégia',
      reverse: false,
    },
    {
      title: 'Tecnologia de Ponta',
      description: 'Ferramentas modernas que garantem velocidade e estabilidade.',
      image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=800&q=80',
      imageAlt: 'Tecnologia',
      reverse: true,
    }
  ],
  socialProof: {
    title: 'Confiança de grandes marcas',
    logos: []
  },
  cta: {
    title: 'Pronto para o próximo nível?',
    subtitle: 'Fale com nossos especialistas e descubra o potencial do seu negócio.',
    button: 'Começar Agora',
    link: '#',
  },
  footer: {
    company_name: 'Agência Digital',
    contacts: ['contato@agencia.com'],
  },
};
"""

# --- UTILITÁRIOS ---

def setup_selenium():
    """Configura o Chrome em modo headless otimizado."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-size=1920,1080")
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
    
    # Remove quebras de linha perigosas dentro de strings JSON não escapadas
    text = text.replace('\n', ' ').replace('\r', '')
    return text

def validar_conteudo_config(conteudo):
    """Validação estrita do conteúdo gerado."""
    if not conteudo or not isinstance(conteudo, str): return False
    if "TS code here" in conteudo: return False
    if "export const AppConfig" not in conteudo: return False
    # Qwen as vezes gera comentários no início, garantimos que tem o export
    if len(conteudo) < 100: return False
    return True

def reset_to_default():
    """Restaura o projeto para o estado limpo original."""
    print("🔄 Resetando projeto para default...")
    config_path = os.path.join(BASE_PATH, "src", "utils", "AppConfig.ts")
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(DEFAULT_APP_CONFIG)
    
    # Reseta Tailwind para cor padrão (Sky Blue)
    tw_path = os.path.join(BASE_PATH, "tailwind.config.js")
    with open(tw_path, "r", encoding="utf-8") as f: content = f.read()
    # Usa regex para encontrar qualquer cor definida e resetar
    new_content = re.sub(r"500: '#.*?'", "500: '#0ea5e9'", content)
    with open(tw_path, "w", encoding="utf-8") as f: f.write(new_content)

def gerar_app_config_fallback(nome, url):
    """Gera um AppConfig padrão de alta qualidade se a IA falhar."""
    # Retorna o template default com dados básicos do cliente
    return DEFAULT_APP_CONFIG.replace('Landing Page Generator', nome).replace('#', url)

# --- CORE FUNCTIONS ---

def processar_cliente(nome, url, objetivo_especifico=None, cor_personalizada=None, modo_deploy=False):
    log = []
    def add_log(msg):
        print(msg)
        log.append(msg)

    # 1. Reset Inicial
    reset_to_default()
    add_log(f"🚀 [AGENTE QWEN] Iniciando: {nome}")
    
    # 2. SCRAPE INTELIGENTE
    add_log(f"🕵️ Analisando identidade digital: {url}")
    site_data = None
    driver = setup_selenium()
    
    if not driver: return {"status": "error", "log": log, "msg": "Falha driver"}

    try:
        driver.set_page_load_timeout(45)
        if not url.startswith('http'): url = 'https://' + url
        driver.get(url)
        time.sleep(4)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Tenta pegar logo (meta tags ou img com class logo)
        logo_url = ""
        meta_logo = soup.find("meta", property="og:image")
        if meta_logo: logo_url = meta_logo["content"]
        
        # Limpeza
        for tag in soup(["script", "style", "svg", "form", "footer", "nav", "header", "noscript"]):
            tag.extract()
            
        text = soup.get_text(separator=' ', strip=True)[:3000] # Qwen aguenta um pouco mais de contexto
        
        site_data = {"text": text, "url": url, "logo": logo_url}
        
    except Exception as e:
        if driver: driver.quit()
        return {"status": "error", "log": log, "msg": f"Scrape Error: {str(e)}"}
    finally:
        if driver: driver.quit()

    # 3. IA COPYWRITER PRO (QWEN)
    add_log(f"🧠 Criando Copy de Alta Conversão ({MODELO})...")
    
    prompt = f"""
    Você é um Arquiteto de Informação e Copywriter Sênior.
    Sua missão é criar o JSON de configuração para uma Landing Page moderna e persuasiva para a empresa "{nome}".
    
    CONTEXTO EXTRAÍDO DO SITE ATUAL:
    {site_data['text']}
    
    OBJETIVO ESTRATÉGICO:
    {objetivo_especifico if objetivo_especifico else 'Criar autoridade imediata, modernizar a marca e vender o serviço principal.'}
    
    DIRETRIZES DE DESIGN E COPY (SWISS STYLE):
    1. Ignore o site antigo. Crie uma "Nova Realidade" premium e minimalista.
    2. Use Português do Brasil impecável, tom profissional e direto.
    3. Escolha uma categoria de imagem do Unsplash abaixo baseada no nicho:
       - Corporativo: https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=800
       - Saúde: https://images.unsplash.com/photo-1629909613654-28e377c37b09?w=800
       - Construção: https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=800
       - Tech: https://images.unsplash.com/photo-1518770660439-4636190af475?w=800
       - Logística: https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=800
    
    FORMATO DE SAÍDA (JSON ÚNICO E VÁLIDO):
    {{
        "app_config": "export const AppConfig = {{ site_name: '{nome}', title: 'TITULO SEO | PROMESSA', description: 'DESCRIÇÃO SEO', locale: 'pt-br', primary_color: '#HEX_COR', hero: {{ title: 'HEADLINE IMPACTANTE', highlight: 'DESTAQUE', description: 'TEXTO DE APOIO PERSUASIVO', button: 'CTA PRINCIPAL', buttonLink: '{url}', image: 'URL_UNSPLASH_ESCOLHIDA' }}, features: [ {{ title: 'BENEFÍCIO 1', description: 'DESCRIÇÃO DO BENEFÍCIO', image: 'URL_UNSPLASH_ESCOLHIDA', imageAlt: 'Alt Text 1', reverse: false }}, {{ title: 'BENEFÍCIO 2', description: 'DESCRIÇÃO DO BENEFÍCIO', image: 'URL_UNSPLASH_ESCOLHIDA', imageAlt: 'Alt Text 2', reverse: true }} ], socialProof: {{ title: 'Empresas que confiam', logos: [] }}, cta: {{ title: 'CHAMADA FINAL', subtitle: 'REMOÇÃO DE OBJEÇÃO', button: 'CTA FINAL', link: '{url}' }}, footer: {{ company_name: '{nome}', contacts: ['Contato via Site'] }} }};",
        "primary_color": "#HEXCODE_MODERNO",
        "whatsapp_message": "Olá {nome}, vi seu site e criei uma versão premium focada em conversão: [LINK]"
    }}
    """
    
    json_res = {}
    config_code = ""
    cor_final = "#000000"
    
    try:
        response = requests.post(OLLAMA_API_URL, json={
            "model": MODELO,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.2, # Qwen é criativo, 0.2 segura ele na estrutura
                "num_ctx": 4096,
                "num_predict": 2500
            }
        })
        
        if response.status_code == 200:
            raw_response = response.json()['response']
            clean_response = clean_json_string(raw_response)
            json_res = json.loads(clean_response)
            config_code = json_res.get('app_config', '')
            cor_final = json_res.get('primary_color', '#03A9F4')
        else:
            add_log(f"⚠️ Erro API IA: {response.text}")
            if "model requires more system memory" in response.text:
                 add_log("❌ Memória insuficiente. Feche navegadores/abas extras.")

    except Exception as e:
        add_log(f"⚠️ Erro IA Exception: {str(e)}")

    # 4. ATUALIZAR ARQUIVOS
    add_log("💾 Aplicando Design System...")
    try:
        base_path = "." if os.path.exists("src") else ".."
        
        # Validação e Fallback
        if not validar_conteudo_config(config_code):
            add_log("⚠️ IA gerou conteúdo instável. Aplicando Template Premium de Fallback.")
            config_code = gerar_app_config_fallback(nome, url)
            cor_final = "#1E293B" 

        # Salva AppConfig
        with open(f"{base_path}/src/utils/AppConfig.ts", "w", encoding="utf-8") as f:
            f.write(config_code)
            
        # Salva Cores (Tailwind)
        cor_usuario = cor_personalizada if cor_personalizada else cor_final
        tw_path = f"{base_path}/tailwind.config.js"
        if os.path.exists(tw_path):
            with open(tw_path, "r", encoding="utf-8") as f: content = f.read()
            # Regex robusto para achar a cor, não importa o formato
            new_content = re.sub(r"500: '#.*?'", f"500: '{cor_usuario}'", content)
            with open(tw_path, "w", encoding="utf-8") as f: f.write(new_content)
        
    except Exception as e:
        return {"status": "error", "log": log, "msg": f"Erro Arquivos: {str(e)}"}

    # 5. DEPLOY
    final_url = "http://localhost:3000"
    if modo_deploy:
        add_log("☁️ Subindo para Vercel...")
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

    add_log("✅ Landing Page Pronta!")
    return {
        "status": "success", 
        "log": log, 
        "url": final_url, 
        "whatsapp": json_res.get('whatsapp_message', f"Olá {nome}, criei um novo site para você: {final_url}"),
        "color_used": cor_usuario
    }

if __name__ == "__main__":
    print("Use o Dashboard: streamlit run agent/dashboard.py")