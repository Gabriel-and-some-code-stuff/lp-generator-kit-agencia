import time
import re
import os
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURAÇÃO DE CAMINHOS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_CONTEXTO = os.path.join(BASE_DIR, "contexto_para_cursor.txt")
APP_CONFIG_PATH = os.path.join(BASE_DIR, "src", "utils", "AppConfig.ts")
TAILWIND_CONFIG_PATH = os.path.join(BASE_DIR, "tailwind.config.js")

# --- TEMPLATES PADRÃO (FACTORY RESET) ---
DEFAULT_APP_CONFIG = """export const AppConfig = {
  site_name: 'Landing Page Generator',
  title: 'Template Padrão',
  description: 'Aguardando geração de conteúdo...',
  locale: 'pt-br',

  hero: {
    title: 'Aguardando Conteúdo',
    highlight: '---',
    description: 'O conteúdo será gerado automaticamente pelo agente.',
    button: 'Aguarde',
    buttonLink: '#',
  },

  features: [
    {
      title: 'Funcionalidade 1',
      description: 'Descrição pendente.',
      image: 'https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=800&q=80',
      imageAlt: 'Placeholder',
      reverse: false,
    },
  ],

  cta: {
    title: 'Aguardando Geração',
    subtitle: 'O sistema está pronto para processar novos dados.',
    button: 'Iniciar',
    link: '#',
  },

  footer: {
    company_name: 'Generator V1',
    contacts: ['Contato'],
  },
};
"""

DEFAULT_TAILWIND_CONFIG = """/** @type {import('tailwindcss').Config} */
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
          500: '#0ea5e9', // COR PADRÃO (SKY BLUE)
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
          500: '#a0aec0',
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

def print_swiss_header():
    print("\n" + "="*60)
    print("◼ LP GENERATOR KIT | V1 INDUSTRIAL WORKFLOW")
    print("="*60 + "\n")

def reset_ambiente():
    """Restaura os arquivos de configuração para o estado padrão."""
    print("🔄 [RESET] Restaurando ambiente para padrão de fábrica...")
    
    try:
        with open(APP_CONFIG_PATH, "w", encoding="utf-8") as f:
            f.write(DEFAULT_APP_CONFIG)
        
        with open(TAILWIND_CONFIG_PATH, "w", encoding="utf-8") as f:
            f.write(DEFAULT_TAILWIND_CONFIG)
            
        print("✅ [RESET] AppConfig.ts e tailwind.config.js limpos.")
    except Exception as e:
        print(f"❌ [ERRO] Falha no reset: {str(e)}")

def limpar_texto(texto):
    if not texto: return ""
    return re.sub(r'\s+', ' ', texto).strip()

def extrair_metadados(soup):
    title = soup.title.string if soup.title else "Sem título"
    meta_desc = soup.find("meta", attrs={"name": "description"})
    description = meta_desc["content"] if meta_desc else "Sem descrição"
    return title.strip(), description.strip()

def extrair_dados_site(url, nome_cliente):
    # 1. Reset Antes do Scraping (Garante pureza)
    reset_ambiente()
    
    print("-" * 60)
    print(f"🕵️  [SCRAPER] Iniciando leitura: {nome_cliente}")
    print(f"🔗 URL: {url}")
    print("-" * 60)
    
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    
    driver = None
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        if not url.startswith('http'): url = 'https://' + url
            
        driver.get(url)
        time.sleep(4)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extração
        page_title, page_desc = extrair_metadados(soup)
        for tag in soup(["script", "style", "svg", "noscript", "iframe", "header", "footer", "nav"]):
            tag.extract()
        
        texto_limpo = limpar_texto(soup.get_text(separator='\n'))[:8000]
        
        # Output para o Cursor
        output_content = f"""
=== DADOS DO CLIENTE ===
NOME: {nome_cliente}
URL: {url}
TITULO ATUAL: {page_title}
DESCRIÇÃO: {page_desc}

=== CONTEÚDO BRUTO DO SITE ===
{texto_limpo}

=== TAREFA PARA O AGENTE ===
1. Analise o nicho e a identidade visual baseada no conteúdo.
2. Reescreva todo o conteúdo seguindo o estilo SWISS (Objetivo, Claro).
3. Identifique a COR PRIMÁRIA da marca.

=== AÇÃO DE EDIÇÃO ===
Você deve editar DOIS arquivos agora:
1. `src/utils/AppConfig.ts`: Atualize com o novo copy e imagens.
2. `tailwind.config.js`: Atualize a cor `primary.500` com a cor da marca identificada.
"""

        with open(ARQUIVO_CONTEXTO, "w", encoding="utf-8") as f:
            f.write(output_content)
            
        print("\n✅ [SUCESSO] Contexto gerado.")
        
        # PROMPT OTIMIZADO PARA COMPOSER
        prompt_comando = (
            "@contexto_para_cursor.txt @AGENT_INSTRUCTIONS.MD @AppConfig.ts @tailwind.config.js "
            "Siga as instruções, EDITE o AppConfig.ts com o novo conteúdo e "
            "ALTERE a cor primary.500 no tailwind.config.js. "
            "Não pergunte, apenas aplique as mudanças nos arquivos."
        )
        
        print("\n" + "🚨 " * 5 + "PROMPT PARA O COMPOSER (CTRL+I)" + " 🚨" * 5)
        print("\nCopie e cole EXATAMENTE o texto abaixo no Composer:\n")
        print("-" * 20)
        print(prompt_comando)
        print("-" * 20 + "\n")
        
    except Exception as e:
        print(f"\n❌ [ERRO] {str(e)}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    print_swiss_header()
    try:
        if len(sys.argv) > 2:
            nome = sys.argv[1]
            link = sys.argv[2]
        else:
            nome = input("Nome do Cliente: ").strip()
            link = input("URL do Site: ").strip()
            
        if nome and link:
            extrair_dados_site(link, nome)
        else:
            print("❌ Dados inválidos.")
    except KeyboardInterrupt:
        print("\nOperação cancelada.")