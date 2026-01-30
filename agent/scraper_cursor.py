import sys
import os
import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup, Comment

# --- CONFIGURAÇÃO DE CAMINHOS ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
OUTPUT_CONTEXT_FILE = "contexto_para_cursor.txt"
OUTPUT_CLEAN_HTML_FILE = "clean_source.html"
CONTEXT_FILE_PATH = os.path.join(PROJECT_ROOT, OUTPUT_CONTEXT_FILE)
CLEAN_HTML_PATH = os.path.join(CURRENT_DIR, OUTPUT_CLEAN_HTML_FILE)
CSS_DIR = os.path.join(CURRENT_DIR, "downloaded_css")

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
    buttonLink: '#contact',
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
    link: '#contact',
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
      { label: 'Serviços', link: '#services' },
      { label: 'Sobre', link: '#about' },
      { label: 'Contato', link: '#contact' },
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

def extract_logo_and_images(soup, base_url: str) -> dict:
    """Extrai candidatos de logo e imagens hero com dimensões."""
    extraction = {
        "logo": None,
        "logo_dims": None,
        "hero_images": [],
    }
    
    if not soup:
        return extraction

    # 1. Procurar logo
    logo_selectors = ['[class*="logo"]', '[id*="logo"]', '[class*="brand"]', 'nav img', 'header img']
    for selector in logo_selectors:
        try:
            el = soup.select_one(selector)
            if not el:
                continue
            # If the selector matched a container (div, a, etc.), find an <img> inside
            img_tag = el if getattr(el, 'name', None) == 'img' else el.find('img')
            
            if img_tag and img_tag.get('src'):
                try:
                    url = urljoin(base_url, img_tag['src'])
                except Exception:
                    url = img_tag.get('src') or None
                width = (img_tag.get('width', '') or '').replace('px', '')
                height = (img_tag.get('height', '') or '').replace('px', '')
                extraction["logo"] = url
                extraction["logo_dims"] = f"{width}x{height}" if width and height else "unknown"
                break
        except Exception:
            pass
    
    # 2. Procurar imagens hero (largas, em seções principais)
    for img in soup.find_all('img'):
        if not img or not img.get('src'):
            continue
        src = urljoin(base_url, img['src'])
        # Skip pequenas imagens (provavelmente ícones)
        width = img.get('width', '').replace('px', '')
        height = img.get('height', '').replace('px', '')
        
        try:
            if width and height and int(width) > 300 and int(height) > 200:
                extraction["hero_images"].append({
                    "url": src,
                    "dimensions": f"{width}x{height}",
                    "alt": img.get('alt', 'N/A')
                })
        except ValueError:
            # Dimensões não são números, skip
            pass
    
    return extraction

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

def clean_html(html_source: str, base_url: str) -> str:
    """
    Higieniza o HTML para entregar apenas a estrutura e conteúdo textual ao LLM.
    Inclui extração e inlining de CSS.
    """
    try:
        soup = BeautifulSoup(html_source, 'html.parser')

        if not soup:
            return ""

        # 1. Remover elementos desnecessários
        # CRÍTICO: Removido "style" desta lista para permitir extração de cores inline/header
        tags_to_remove = ["script", "noscript", "iframe", "svg", "meta", "form"]
        for tag_name in tags_to_remove:
            for tag in soup.find_all(tag_name):
                try:
                    tag.decompose()
                except Exception:
                    pass

        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        # 2. RESOLVER URLS RELATIVAS
        # Imagens
        for img in soup.find_all('img'):
            if img and img.get('src'):
                img['src'] = urljoin(base_url, img['src'])
                if img.get('srcset'): del img['srcset']
                if img.get('loading'): del img['loading']
                if img.get('class'): del img['class']
        
        # Links
        for a in soup.find_all('a'):
            if a and a.get('href'):
                a['href'] = urljoin(base_url, a['href'])

        # 2.5. Trazer CSS externo (link rel=stylesheet) e resolver recursos dentro dele
        combined_css = ""
        try:
            os.makedirs(CSS_DIR, exist_ok=True)
        except Exception:
            pass

        for link in soup.find_all('link'):
            if not link:
                continue
                
            href = link.get('href')
            if not href:
                try:
                    link.decompose()
                except Exception:
                    pass
                continue

            rel = link.get('rel') or []
            if isinstance(rel, str):
                rels = [rel]
            else:
                try:
                    rels = list(rel)
                except Exception:
                    rels = []

            if any('stylesheet' in (r or '').lower() for r in rels):
                abs_href = urljoin(base_url, href)
                print(f"🧩 Baixando CSS: {abs_href}", file=sys.stderr)
                try:
                    resp = requests.get(abs_href, headers=HEADERS, timeout=15)
                    resp.raise_for_status()
                    css_text = resp.text

                    # Resolver url(...) dentro do CSS para URLs absolutas
                    def repl_url(match):
                        inner = match.group(1).strip()
                        inner = re.sub(r'^["\']|["\']$', '', inner)
                        return "url('{}')".format(urljoin(abs_href, inner))
                    
                    # Regex mais robusto para URLs em CSS
                    css_text = re.sub(r'url\(([^)]+)\)', repl_url, css_text)

                    # Resolver @import e incorporar conteúdo importado
                    def repl_import(match):
                        imp_raw = match.group(1).strip()
                        imp = re.sub(r'^["\']|["\']$', '', imp_raw)
                        imp_abs = urljoin(abs_href, imp)
                        try:
                            r2 = requests.get(imp_abs, headers=HEADERS, timeout=15)
                            r2.raise_for_status()
                            imp_css = r2.text
                            def repl_inner_url(m):
                                inner = m.group(1).strip()
                                inner = re.sub(r'^["\']|["\']$', '', inner)
                                return "url('{}')".format(urljoin(imp_abs, inner))
                            imp_css = re.sub(r'url\(([^)]+)\)', repl_inner_url, imp_css)
                            return imp_css
                        except Exception as e:
                            print(f"⚠️ Aviso: falha ao baixar @import {imp_abs}: {e}", file=sys.stderr)
                            return ''
                    
                    css_text = re.sub(r"@import\s+(?:url\()?['\"]?([^'\"\)]+)['\"]?\)?\s*;", repl_import, css_text)

                    combined_css += f"\n/* Inlined from: {abs_href} */\n" + css_text

                    # Salvar arquivo CSS localmente para inspeção
                    try:
                        filename = os.path.basename(abs_href.split('?')[0]) or 'style.css'
                        # Sanitize filename
                        filename = re.sub(r'[^\w\-_\.]', '_', filename)
                        out_path = os.path.join(CSS_DIR, filename)
                        with open(out_path, 'w', encoding='utf-8') as cf:
                            cf.write(css_text)
                    except Exception as e:
                        print(f"⚠️ Aviso: não foi possível salvar CSS em {CSS_DIR}: {e}", file=sys.stderr)

                except Exception as e:
                    print(f"⚠️ Falha ao baixar CSS {abs_href}: {e}", file=sys.stderr)

            # Remover a referência <link> para evitar redundância e confusão
            try:
                link.decompose()
            except Exception:
                pass

        # Se encontramos CSS externo, adicionar dentro de <style> no HTML higienizado
        if combined_css:
            style_tag = soup.new_tag('style')
            style_tag.string = combined_css
            if soup.head:
                soup.head.append(style_tag)
            else:
                soup.insert(0, style_tag)

        # 3. Limpeza final de atributos
        allowed_attrs = ['class', 'id', 'src', 'href', 'alt', 'title', 'role', 'style']
        for tag in soup.find_all(True):
            if not tag.attrs:
                continue
                
            attrs = dict(tag.attrs)
            for attr in list(attrs.keys()):
                if attr not in allowed_attrs:
                    try:
                        tag.attrs.pop(attr, None)
                    except Exception:
                        pass

        return soup.prettify()
    except Exception as e:
        # Tenta retornar pelo menos o conteúdo parcial seguro
        partial = html_source[:500] if html_source else "Vazio"
        return f"Erro ao limpar HTML: {str(e)}\nConteúdo parcial: {partial}"

def run_scraper(url: str):
    reset_configs()

    try:
        print(f"🕵️  Acessando {url}...", file=sys.stderr)
        
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        if response.encoding is None:
            response.encoding = 'utf-8'
            
        raw_html = response.text
        
        print("🧹 Limpando código fonte e resolvendo URLs...", file=sys.stderr)
        final_html = clean_html(raw_html, url)
        
        # NOVO: Extrair logo e imagens antes de salvar (usando html bruto para não perder dados na limpeza)
        soup_for_extraction = BeautifulSoup(raw_html, 'html.parser')
        image_data = extract_logo_and_images(soup_for_extraction, url)
        
        try:
            with open(CLEAN_HTML_PATH, "w", encoding="utf-8") as f:
                f.write(final_html)
        except Exception as e:
            print(f"⚠️ Aviso: Não foi possível salvar clean_source.html: {e}", file=sys.stderr)
        
        # NOVO: Montar seção de análise de imagens
        images_section = "=== IMAGENS EXTRAÍDAS (ANÁLISE) ===\n"
        if image_data["logo"]:
            images_section += f"LOGO ENCONTRADO:\n  URL: {image_data['logo']}\n  Dimensões: {image_data['logo_dims']}\n\n"
        else:
            images_section += "LOGO: Não encontrado. Deixe 'logo.url' vazio no AppConfig.\n\n"
        
        if image_data["hero_images"]:
            images_section += "IMAGENS CANDIDATAS PARA HERO (verificar aspect ratio 16:9 ou 4:3):\n"
            for i, img in enumerate(image_data["hero_images"][:5], 1):  # Limitar a 5
                images_section += f"  {i}. {img['url']}\n     Dimensões: {img['dimensions']}\n     Alt: {img['alt']}\n"
            images_section += "\nFAVOR VALIDAR: Essas imagens têm aspect ratio apropriada para hero?\n\n"
        else:
            images_section += "IMAGENS HERO: Nenhuma imagem grande encontrada. Deixe 'hero.image' vazio ou use apenas se fornecido.\n\n"
        
        context_content = f"""=== URL ALVO ===
{url}

{images_section}

=== INSTRUÇÃO ===
Analise o HTML abaixo. Extraja:
1. Paleta de cores (para tailwind.config.js) - IMPORTANTE: O CSS foi baixado e incorporado no HTML abaixo dentro de tags <style>. Procure por cores hexadecimais em classes de botões, headers ou backgrounds.
2. Textos e Links para preencher o AppConfig.ts
3. USE AS IMAGENS EXTRAÍDAS ACIMA QUANDO APROPRIADO:
   - Se LOGO foi encontrado, use sua URL no AppConfig.logo.url
   - Se LOGO não foi encontrado, deixe AppConfig.logo.url vazio ('')
   - Para hero, escolha uma imagem HERO apropriada (aspect ratio 16:9 ou 4:3)
   - NUNCA use static.photos para logo ou hero a menos que absolutamente nenhuma alternativa exista
4. As URLs de imagem já foram tratadas e são absolutas.

=== CÓDIGO FONTE (HIGIENIZADO E COM CSS INLINE) ===
{final_html}
"""
        with open(CONTEXT_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(context_content)
            
        print(f"✅ Sucesso! Contexto gerado em: {CONTEXT_FILE_PATH}", file=sys.stderr)
        if image_data["logo"]:
            print(f"  📸 Logo extraído: {image_data['logo']}", file=sys.stderr)
        if image_data["hero_images"]:
            print(f"  🖼️  {len(image_data['hero_images'])} imagens hero encontradas", file=sys.stderr)

    except requests.exceptions.MissingSchema:
        print(f"\n❌ Erro: URL inválida.", file=sys.stderr)
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Erro: Falha na conexão.", file=sys.stderr)
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