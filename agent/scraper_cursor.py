import sys
import os
import requests
from bs4 import BeautifulSoup, Comment

# --- CONFIGURAÇÃO DE CAMINHOS ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
OUTPUT_CONTEXT_FILE = "contexto_para_cursor.txt"
OUTPUT_CLEAN_HTML_FILE = "clean_source.html"
CONTEXT_FILE_PATH = os.path.join(PROJECT_ROOT, OUTPUT_CONTEXT_FILE)
CLEAN_HTML_PATH = os.path.join(CURRENT_DIR, OUTPUT_CLEAN_HTML_FILE)

# Caminhos dos arquivos de configuração para resetar
APP_CONFIG_PATH = os.path.join(PROJECT_ROOT, "src", "utils", "AppConfig.ts")
TAILWIND_CONFIG_PATH = os.path.join(PROJECT_ROOT, "tailwind.config.js")

# --- CONTEÚDO DEFAULT (RESET) ---
DEFAULT_APP_CONFIG = """export const AppConfig = {
  site_name: 'Landing Page Template',
  title: 'Título Otimizado para SEO | Nicho do Cliente',
  description:
    'Descrição persuasiva e focada em conversão para os motores de busca (150-160 caracteres).',
  locale: 'pt-br',

  logo: {
    url: '',
    width: 200,
    height: 50,
    alt: 'Logo da Empresa',
  },

  hero: {
    title: 'Headline de Alto Impacto e Conversão',
    highlight: 'Destaque Principal',
    description:
      'Subtítulo persuasivo que explica a proposta de valor única do negócio e incentiva a ação imediata do visitante.',
    button: 'Chamada para Ação',
    secondaryButton: 'Saiba Mais',
    buttonLink: '#',
    image:
      'https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=80',
  },

  trust: {
    stats: [
      { value: '+10', label: 'Anos de Experiência' },
      { value: '+500', label: 'Projetos Realizados' },
      { value: '100%', label: 'Satisfação' },
      { value: '24/7', label: 'Suporte' },
    ],
  },

  problem: {
    title: 'Identifique a Dor do Seu Cliente Aqui',
    description:
      'Descreva o cenário atual e os problemas que o cliente enfrenta antes de contratar seus serviços.',
    items: [
      'Problema comum número 1',
      'Dificuldade técnica ou operacional',
      'Custo elevado com soluções ineficientes',
      'Falta de suporte especializado',
    ],
  },

  solution: {
    title: 'A Solução Ideal para o Problema',
    subtitle: 'Nossa Abordagem',
    cards: [
      {
        title: 'Solução 1',
        description:
          'Explicação detalhada de como este serviço resolve uma dor específica.',
      },
      {
        title: 'Solução 2',
        description:
          'Benefício claro e direto que diferencia sua empresa da concorrência.',
      },
      {
        title: 'Solução 3',
        description:
          'Vantagem competitiva focada em resultado e eficiência operacional.',
      },
    ],
  },

  howItWorks: {
    title: 'Como Funciona o Processo',
    steps: [
      {
        title: '1. Contato Inicial',
        description: 'O cliente entra em contato e solicita um orçamento.',
      },
      {
        title: '2. Análise',
        description:
          'Nossa equipe avalia a necessidade e propõe a melhor solução.',
      },
      {
        title: '3. Execução',
        description:
          'Realizamos o serviço com excelência e prazo garantido em contrato.',
      },
      {
        title: '4. Entrega',
        description:
          'Você recebe o resultado esperado com total suporte pós-venda.',
      },
    ],
  },

  benefits: {
    title: 'Principais Vantagens',
    items: [
      'Benefício exclusivo número 1',
      'Garantia de qualidade e procedência',
      'Economia de tempo e recursos',
      'Atendimento personalizado',
    ],
  },

  socialProof: {
    title: 'O que dizem nossos clientes',
    testimonials: [
      {
        name: 'Nome do Cliente',
        role: 'Cargo / Empresa',
        text: 'Depoimento focado em resultados. O serviço mudou a forma como operamos e trouxe eficiência.',
      },
      {
        name: 'Nome do Cliente',
        role: 'Cargo / Empresa',
        text: 'Excelente atendimento e suporte técnico. A equipe foi muito atenciosa desde o início.',
      },
      {
        name: 'Nome do Cliente',
        role: 'Cargo / Empresa',
        text: 'Profissionalismo e entrega no prazo. Superou as expectativas de qualidade.',
      },
    ],
    logos: [],
    gallery: [],
  },

  faq: {
    title: 'Perguntas Frequentes',
    questions: [
      {
        q: 'Pergunta comum sobre o serviço?',
        a: 'Resposta clara e objetiva que remove objeções de compra imediatamente.',
      },
      {
        q: 'Quais são as formas de pagamento?',
        a: 'Aceitamos cartões, boleto e transferência bancária facilitada.',
      },
      {
        q: 'Qual o prazo de atendimento?',
        a: 'Nosso prazo médio é de 24 a 48 horas úteis após a confirmação.',
      },
    ],
  },

  cta: {
    title: 'Pronto para começar?',
    subtitle:
      'Entre em contato hoje mesmo e solicite um orçamento sem compromisso.',
    button: 'Falar com Consultor',
    link: '#',
  },

  footer: {
    company_name: 'Nome da Empresa',
    description: 'Breve descrição institucional para o rodapé.',
    contacts: [
      'Endereço Físico, Cidade - UF',
      '(00) 0000-0000',
      'contato@empresa.com.br',
    ],
    links: [
      { label: 'Início', link: '/' },
      { label: 'Serviços', link: '/#services' },
      { label: 'Sobre', link: '/#about' },
      { label: 'Contato', link: '/#contact' },
    ],
    social: [],
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

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com/'
}

def reset_configs():
    """Restaura AppConfig.ts e tailwind.config.js para o estado original."""
    print("🔄 Resetando arquivos de configuração para o padrão...", file=sys.stderr)
    try:
        with open(APP_CONFIG_PATH, "w", encoding="utf-8") as f:
            f.write(DEFAULT_APP_CONFIG)
        with open(TAILWIND_CONFIG_PATH, "w", encoding="utf-8") as f:
            f.write(DEFAULT_TAILWIND_CONFIG)
        print("✅ Configurações resetadas com sucesso.", file=sys.stderr)
    except Exception as e:
        print(f"⚠️ Erro ao resetar configurações: {e}", file=sys.stderr)

def clean_html(html_source: str) -> str:
    """
    Higieniza o HTML para entregar apenas a estrutura e conteúdo textual ao LLM.
    """
    try:
        soup = BeautifulSoup(html_source, 'html.parser')

        tags_to_remove = ["script", "style", "noscript", "iframe", "svg", "link", "meta", "head", "form"]
        for tag in soup(tags_to_remove):
            tag.decompose()

        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        for tag in soup.find_all(True):
            attrs = dict(tag.attrs)
            allowed_attrs = ['class', 'id', 'src', 'href', 'alt', 'title', 'role']
            for attr in attrs:
                if attr not in allowed_attrs:
                    del tag.attrs[attr]

        return soup.prettify()
    except Exception as e:
        return f"Erro ao limpar HTML: {str(e)}\nConteúdo parcial: {html_source[:500]}"

def run_scraper(url: str):
    # 1. Resetar configurações antes de começar
    reset_configs()

    try:
        print(f"🕵️  Acessando {url}...", file=sys.stderr)
        
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        if response.encoding is None:
            response.encoding = 'utf-8'
            
        raw_html = response.text
        
        print("🧹 Limpando código fonte...", file=sys.stderr)
        final_html = clean_html(raw_html)
        
        try:
            with open(CLEAN_HTML_PATH, "w", encoding="utf-8") as f:
                f.write(final_html)
        except Exception as e:
            print(f"⚠️ Aviso: Não foi possível salvar clean_source.html: {e}", file=sys.stderr)
        
        context_content = f"""=== URL ALVO ===
{url}

=== INSTRUÇÃO ===
Analise o HTML abaixo. Extraia:
1. Paleta de cores (para tailwind.config.js)
2. Textos, Imagens e Links para preencher o AppConfig.ts (Hero, Features, Footer, etc)

=== CÓDIGO FONTE (HIGIENIZADO) ===
{final_html}
"""
        with open(CONTEXT_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(context_content)
            
        print(f"✅ Sucesso! Contexto gerado em: {CONTEXT_FILE_PATH}", file=sys.stderr)

    except requests.exceptions.MissingSchema:
        print(f"\n❌ Erro: URL inválida. Certifique-se de incluir http:// ou https://", file=sys.stderr)
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Erro: Falha na conexão. Verifique a URL ou sua internet.", file=sys.stderr)
    except Exception as e:
        print(f"\n❌ Erro crítico: {str(e)}", file=sys.stderr)

def normalize_url(url: str) -> str:
    url = url.strip()
    if not url.startswith('http'):
        return 'https://' + url
    return url

def main():
    url = ""
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if "http" in arg or "www" in arg or "." in arg:
                url = arg
                break
    
    if not url:
        try:
            url = input("Digite a URL do site para clonar: ")
        except KeyboardInterrupt:
            return

    if url:
        run_scraper(normalize_url(url))
    else:
        print("URL inválida.")

if __name__ == "__main__":
    main()