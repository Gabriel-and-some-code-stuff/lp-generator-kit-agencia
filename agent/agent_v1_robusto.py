import os
import json
import re
import time
import requests # Ainda usado para o scrape
from openai import OpenAI # Nova forma de conexão
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURAÇÕES DO LM STUDIO ---
# O LM Studio roda localmente na porta 1234 e emula a API da OpenAI
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
MODELO_IDENTIFIER = "local-model" # O LM Studio usa o modelo que estiver carregado na interface

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- TEMPLATES (MANTIDOS IGUAIS PELA SEGURANÇA) ---
TEMPLATE_APP_CONFIG = """
export const AppConfig = {{
  site_name: '{site_name}',
  title: '{title}',
  description: '{description}',
  locale: 'pt-br',
  primary_color: '{primary_color}',
  hero: {{
    title: '{hero_title}',
    highlight: '{hero_highlight}',
    description: '{hero_description}',
    button: '{hero_button}',
    buttonLink: '{hero_link}',
    image: '{hero_image}',
  }},
  features: {features_json},
  socialProof: {{
    title: 'Confiança de grandes marcas',
    logos: [] 
  }},
  cta: {{
    title: '{cta_title}',
    subtitle: '{cta_subtitle}',
    button: '{cta_button}',
    link: '{cta_link}',
  }},
  footer: {{
    company_name: '{company_name}',
    contacts: {contacts_json},
  }},
}};
"""

TEMPLATE_TAILWIND = """
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
      '4xl': '2.25rem',
      '5xl': '3rem',
      '6xl': '4rem',
    },
    extend: {
      colors: {
        primary: {
          100: '#E6F6FE',
          200: '#C0EAFC',
          300: '#9ADDFB',
          400: '#4FC3F7',
          500: '%s',
          600: '#0398DC',
          700: '#026592',
          800: '#014C6E',
          900: '#013349',
        },
        gray: {
          100: '#f7fafc',
          200: '#edf2f7',
          300: '#e2e8f0',
          400: '#cbd5e0',
          500: '#0ea5e9',
          600: '#718096',
          700: '#4a5568',
          800: '#2d3748',
          900: '#1a202c',
        },
      },
      lineHeight: {
        hero: '4.5rem',
      },
    },
  },
  plugins: [],
};
"""

# Dados de Fallback (Segurança)
DEFAULT_DATA = {
    "site_name": "Landing Page Generator",
    "title": "Soluções de Alto Impacto para seu Negócio",
    "description": "Aumente suas vendas e autoridade com nossa estratégia digital.",
    "primary_color": "#0ea5e9",
    "hero_title": "Transforme Visitantes em Clientes",
    "hero_highlight": "Resultados Reais",
    "hero_description": "Nossa metodologia comprovada ajuda empresas a escalarem suas operações com previsibilidade e segurança.",
    "hero_button": "Agendar Consultoria",
    "hero_link": "#",
    "hero_image": "https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=1200&q=80",
    "cta_title": "Pronto para o próximo nível?",
    "cta_subtitle": "Fale com nossos especialistas e descubra o potencial do seu negócio.",
    "cta_button": "Começar Agora",
    "cta_link": "#",
    "company_name": "Agência Digital",
    "features_json": json.dumps([
        { "title": "Estratégia", "description": "Plano único.", "image": "https://images.unsplash.com/photo-1552664730-d307ca884978", "imageAlt": "Estratégia", "reverse": False },
        { "title": "Tecnologia", "description": "Ferramentas modernas.", "image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f", "imageAlt": "Tecnologia", "reverse": True }
    ]),
    "contacts_json": json.dumps(["contato@agencia.com"])
}

# --- UTILS ---

def ler_instrucoes_agente():
    path = os.path.join(BASE_PATH, "AGENT_INSTRUCTIONS.MD")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "Gere uma landing page B2B."

def limpar_texto_radical(texto):
    """Remove lixo do scrape que possa confundir o modelo."""
    texto = re.sub(r'[^\w\s.,!?;:()\-@R$]', '', texto) # Mantém R$ e chars básicos
    return re.sub(r'\s+', ' ', texto).strip()

def sanitizar_features(features_raw):
    """Garante que o JSON de features não quebre o React."""
    if not isinstance(features_raw, list):
        return json.loads(DEFAULT_DATA['features_json'])
    
    clean = []
    for item in features_raw:
        if not isinstance(item, dict): continue
        
        # Garante string
        desc = item.get('description', '')
        if isinstance(desc, dict):
            desc = str(desc.get('text', str(desc))) # Tenta salvar se for objeto
        
        clean.append({
            "title": str(item.get('title', 'Benefício')),
            "description": str(desc),
            "image": str(item.get('image', 'https://via.placeholder.com/800')),
            "imageAlt": str(item.get('imageAlt', 'Imagem')),
            "reverse": bool(item.get('reverse', False))
        })
    return json.dumps(clean, ensure_ascii=False)

def aplicar_configuracao(dados):
    # Sanitização final antes de escrever
    dados['features_json'] = sanitizar_features(dados.get('features_json'))
    
    contacts = dados.get('contacts_json', [])
    if not isinstance(contacts, list): contacts = ["Contato via site"]
    dados['contacts_json'] = json.dumps([str(c) for c in contacts], ensure_ascii=False)

    # Fallback de campos vazios
    for k, v in DEFAULT_DATA.items():
        if k not in dados or not dados[k]:
            if 'json' not in k: dados[k] = v

    # Escreve AppConfig.ts
    try:
        with open(f"{BASE_PATH}/src/utils/AppConfig.ts", "w", encoding="utf-8") as f:
            f.write(TEMPLATE_APP_CONFIG.format(**dados))
    except Exception as e:
        print(f"Erro escrevendo AppConfig: {e}")

    # Escreve Tailwind
    try:
        cor = dados.get('primary_color', '#0ea5e9')
        if not cor.startswith('#'): cor = '#0ea5e9'
        with open(f"{BASE_PATH}/tailwind.config.js", "w", encoding="utf-8") as f:
            f.write(TEMPLATE_TAILWIND % cor)
    except Exception as e:
        print(f"Erro escrevendo Tailwind: {e}")

def setup_selenium():
    opt = Options()
    opt.add_argument("--headless=new")
    opt.add_argument("--no-sandbox")
    opt.add_argument("--disable-dev-shm-usage")
    opt.add_argument("--disable-blink-features=AutomationControlled")
    try:
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opt)
    except:
        return None

# --- LOOP PRINCIPAL ---

def processar_cliente(nome, url, objetivo_especifico=None, cor_personalizada=None, modo_deploy=False):
    log = []
    def add_log(msg):
        print(msg)
        log.append(msg)

    add_log(f"🚀 [LM STUDIO] Iniciando: {nome}")
    
    # 1. Scrape
    site_text = ""
    driver = setup_selenium()
    if driver:
        try:
            add_log(f"🕵️ Lendo site: {url}")
            driver.get(url if url.startswith('http') else f'https://{url}')
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            for tag in soup(["script", "style", "nav", "footer", "svg"]): tag.extract()
            site_text = limpar_texto_radical(soup.get_text())[:2000]
        except Exception as e:
            add_log(f"⚠️ Erro Scrape: {e}")
        finally:
            driver.quit()

    # 2. IA (Via OpenAI Client -> LM Studio)
    add_log("🧠 Gerando estratégia e copy...")
    instrucoes = ler_instrucoes_agente()
    
    system_prompt = f"""
    {instrucoes}
    Você é um assistente JSON estrito. NÃO responda com markdown. NÃO explique nada. Apenas JSON.
    """
    
    user_prompt = f"""
    CLIENTE: {nome}
    SITE ATUAL: {site_text}
    OBJETIVO: {objetivo_especifico or 'Vendas B2B'}
    
    Gere o JSON de configuração seguindo estritamente este schema:
    {{
      "site_name": "Nome",
      "title": "Titulo SEO",
      "description": "Descricao",
      "primary_color": "#HEX",
      "hero_title": "Headline",
      "hero_highlight": "Destaque",
      "hero_description": "Texto Hero",
      "hero_button": "CTA",
      "hero_link": "{url}",
      "hero_image": "URL Unsplash válida",
      "features_json": [
        {{ "title": "Titulo", "description": "Texto", "image": "URL", "imageAlt": "alt", "reverse": false }},
        {{ "title": "Titulo", "description": "Texto", "image": "URL", "imageAlt": "alt", "reverse": true }}
      ],
      "cta_title": "Chamada Final",
      "cta_subtitle": "Texto Apoio",
      "cta_button": "Botão",
      "cta_link": "{url}",
      "company_name": "{nome}",
      "contacts_json": ["Contato"],
      "whatsapp_message": "Msg abordagem..."
    }}
    """

    try:
        completion = client.chat.completions.create(
            model=MODELO_IDENTIFIER,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=2000
        )
        
        raw_content = completion.choices[0].message.content
        
        # Tenta extrair JSON se houver texto em volta
        try:
            json_match = re.search(r'\{.*\}', raw_content, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = raw_content
            
            dados_ia = json.loads(json_str)
            
            if cor_personalizada: dados_ia['primary_color'] = cor_personalizada
            
            add_log("💾 Salvando arquivos...")
            aplicar_configuracao(dados_ia)
            
        except json.JSONDecodeError:
            add_log(f"❌ Erro JSON da IA. Raw: {raw_content[:100]}...")
            return {"status": "error", "log": log, "msg": "JSON inválido gerado pela IA"}

    except Exception as e:
        add_log(f"❌ Erro Conexão LM Studio: {e}")
        add_log("💡 Dica: Verifique se o 'Local Server' está rodando no LM Studio (Porta 1234)")
        return {"status": "error", "log": log, "msg": str(e)}

    # 3. Finalização
    add_log("✅ Concluído!")
    return {
        "status": "success",
        "log": log,
        "url": "http://localhost:3000",
        "whatsapp": dados_ia.get('whatsapp_message', ''),
        "color_used": dados_ia.get('primary_color')
    }

if __name__ == "__main__":
    print("Inicie o servidor no LM Studio e rode via dashboard.py")