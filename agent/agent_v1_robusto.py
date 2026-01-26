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
MODELO = "qwen"  # Recomendado: qwen (7b) ou deepseek-r1
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Raiz do projeto

# --- TEMPLATE PADRÃO (Para Reset) ---
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
    """Configura o Chrome em modo stealth para evitar bloqueios."""
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
        print(f"❌ Erro Driver: {e}")
        return None

def clean_json_string(text):
    """Limpeza cirúrgica do JSON retornado pela IA."""
    text = re.sub(r'```json', '', text, flags=re.IGNORECASE)
    text = re.sub(r'```', '', text)
    start = text.find('{')
    end = text.rfind('}') + 1
    if start != -1 and end != -1:
        return text[start:end]
    return text

def reset_to_default():
    """Restaura o projeto para o estado limpo original."""
    print("🔄 Resetando projeto para default...")
    config_path = os.path.join(BASE_PATH, "src", "utils", "AppConfig.ts")
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(DEFAULT_APP_CONFIG)
    
    # Reseta Tailwind para cor padrão (Sky Blue)
    tw_path = os.path.join(BASE_PATH, "tailwind.config.js")
    with open(tw_path, "r", encoding="utf-8") as f: content = f.read()
    new_content = re.sub(r"500: '#.*?'", "500: '#0ea5e9'", content)
    with open(tw_path, "w", encoding="utf-8") as f: f.write(new_content)

# --- SCRAPER INTELIGENTE (Inspirado no DeepSeek Crawler) ---

def scrape_smart(url):
    """Extrai conteúdo focado em metadata e estrutura, não apenas texto bruto."""
    if not url.startswith('http'): url = 'https://' + url
    
    print(f"🕵️  Deep Scraping: {url}")
    driver = setup_selenium()
    if not driver: return None

    try:
        driver.set_page_load_timeout(45)
        driver.get(url)
        time.sleep(5) # Aguarda hidratação do JS
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # 1. Tenta achar a Logo Oficial
        logo_url = ""
        # Procura por favicons ou meta tags primeiro (mais confiável)
        meta_logo = soup.find("meta", property="og:image")
        if meta_logo: logo_url = meta_logo["content"]
        
        # Se não achou, procura img com 'logo' no nome/classe
        if not logo_url:
            logo_img = soup.find("img", {"src": re.compile(r"logo", re.I)}) or \
                       soup.find("img", {"class": re.compile(r"logo", re.I)})
            if logo_img and logo_img.get("src"):
                src = logo_img["src"]
                if src.startswith("//"): logo_url = "https:" + src
                elif src.startswith("/"): logo_url = url.rstrip("/") + src
                else: logo_url = src

        # 2. Extração de Texto Hierárquica
        # Remove lixo
        for tag in soup(["script", "style", "svg", "form", "nav", "noscript", "iframe"]):
            tag.extract()
            
        # Pega H1, H2, H3 e P para dar contexto estruturado à IA
        content = []
        for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'li']):
            text = element.get_text(strip=True)
            if len(text) > 10: # Filtra textos muito curtos
                tag_name = element.name.upper()
                content.append(f"[{tag_name}]: {text}")
        
        full_text = "\n".join(content)[:6000] # Limite de tokens
        
        return {"text": full_text, "logo": logo_url, "url": url}

    except Exception as e:
        print(f"❌ Erro Scrape: {e}")
        return None
    finally:
        driver.quit()

# --- IA GENERATION (QWEN) ---

def generate_lp_config(site_data, objetivo):
    print(f"🧠 Gerando Copy B2B com {MODELO}...")
    
    prompt = f"""
    Você é um Copywriter Especialista em B2B e Conversão (Estilo Unbounce/ClickFunnels).
    
    OBJETIVO: Criar o JSON de configuração para uma Landing Page de alta performance.
    CLIENTE: {site_data['url']}
    OBJETIVO DO CLIENTE: {objetivo}
    LOGO DETECTADA: {site_data['logo']}
    
    CONTEXTO DO SITE (Estruturado):
    {site_data['text']}
    
    DIRETRIZES:
    1. **Gramática Impecável:** Português do Brasil, formal mas persuasivo.
    2. **Estrutura PAS:** Problema (Hero), Agitação (Features), Solução (CTA).
    3. **Imagens:** Use URLs do Unsplash de alta qualidade que combinem com o nicho.
    4. **Logo:** Se a LOGO DETECTADA estiver vazia, deixe vazio. Se tiver, use-a.
    
    Gere APENAS o JSON abaixo preenchido. NÃO MUDE A ESTRUTURA DAS CHAVES.
    
    {{
        "app_config": "export const AppConfig = {{ site_name: 'NOME DA EMPRESA', title: 'HEADLINE SEO', description: 'META DESC', locale: 'pt-br', primary_color: '#HEX_COR', hero: {{ title: 'HEADLINE IMPACTANTE (PROBLEMA/BENEFÍCIO)', highlight: 'DESTAQUE', description: 'SUBTITULO PERSUASIVO', button: 'CTA PRIMÁRIO', buttonLink: '{site_data['url']}', image: 'URL_UNSPLASH_HERO_HD' }}, features: [ {{ title: 'BENEFÍCIO 1', description: 'COMO RESOLVE', image: 'URL_UNSPLASH_1', imageAlt: 'alt', reverse: false }}, {{ title: 'BENEFÍCIO 2', description: 'COMO RESOLVE', image: 'URL_UNSPLASH_2', imageAlt: 'alt', reverse: true }} ], socialProof: {{ title: 'Empresas que confiam', logos: [] }}, cta: {{ title: 'CTA FINAL', subtitle: 'GARANTIA/ESCASSEZ', button: 'CTA FINAL', link: '{site_data['url']}' }}, footer: {{ company_name: 'NOME', contacts: ['CONTATOS'] }} }};",
        "primary_color": "#HEX_COR",
        "whatsapp_message": "Olá! Analisei o site da [EMPRESA] e criei uma proposta de Landing Page focada em conversão. Segue o link: [LINK]"
    }}
    """
    
    try:
        res = requests.post(OLLAMA_API_URL, json={
            "model": MODELO,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.2, "num_ctx": 8192}
        })
        return json.loads(clean_json_string(res.json()['response']))
    except Exception as e:
        print(f"❌ Erro IA: {e}")
        return None

# --- PROCESSADOR CENTRAL ---

def run_agent(nome, url, objetivo, modo_deploy):
    # 1. Reset (Segurança)
    reset_to_default()
    
    # 2. Scrape
    data = scrape_smart(url)
    if not data: return {"status": "error", "msg": "Falha no Scrape"}
    
    # 3. AI
    config = generate_lp_config(data, objetivo)
    if not config: return {"status": "error", "msg": "Falha na IA"}
    
    # 4. Write Files
    try:
        # AppConfig
        ts_path = os.path.join(BASE_PATH, "src", "utils", "AppConfig.ts")
        with open(ts_path, "w", encoding="utf-8") as f:
            f.write(config['app_config'])
            
        # Tailwind
        tw_path = os.path.join(BASE_PATH, "tailwind.config.js")
        with open(tw_path, "r", encoding="utf-8") as f: content = f.read()
        new_tw = re.sub(r"500: '#.*?'", f"500: '{config['primary_color']}'", content)
        with open(tw_path, "w", encoding="utf-8") as f: f.write(new_tw)
        
    except Exception as e:
        return {"status": "error", "msg": f"Erro escrita: {e}"}
    
    # 5. Deploy
    final_url = "http://localhost:3000"
    if modo_deploy:
        print("☁️ Deploying...")
        slug = re.sub(r'[^a-z0-9-]', '', nome.lower().replace(' ', '-'))[:30]
        cmd = f"vercel --prod --yes --force --name lp-{slug}"
        try:
            # Roda prettier
            subprocess.run("npx prettier --write src/utils/AppConfig.ts", shell=True, cwd=BASE_PATH, stderr=subprocess.DEVNULL)
            # Deploy
            res = subprocess.run(cmd, shell=True, cwd=BASE_PATH, capture_output=True, text=True, timeout=300)
            if res.returncode == 0:
                urls = re.findall(r'https://[^\s]+\.vercel\.app', res.stdout)
                final_url = urls[0] if urls else "URL não encontrada"
            else:
                return {"status": "error", "msg": f"Deploy falhou: {res.stderr[:100]}"}
        except Exception as e:
            return {"status": "error", "msg": f"Erro Deploy: {e}"}
            
    # 6. Finaliza
    return {
        "status": "success",
        "url": final_url,
        "whatsapp": config['whatsapp_message'].replace("[LINK]", final_url).replace("[EMPRESA]", nome)
    }

if __name__ == "__main__":
    print("Execute via Dashboard.")