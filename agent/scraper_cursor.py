import sys
import os
import requests
from bs4 import BeautifulSoup, Comment

# --- CONFIGURAÇÃO ---
OUTPUT_CONTEXT_FILE = "contexto_para_cursor.txt"
OUTPUT_CLEAN_HTML_FILE = "clean_source.html"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
CONTEXT_FILE_PATH = os.path.join(PROJECT_ROOT, OUTPUT_CONTEXT_FILE)
CLEAN_HTML_PATH = os.path.join(CURRENT_DIR, OUTPUT_CLEAN_HTML_FILE)

# Headers para simular um navegador real e evitar bloqueios simples
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com/'
}

def clean_html(html_source: str) -> str:
    """
    Higieniza o HTML para entregar apenas a estrutura e conteúdo textual ao LLM.
    Remove scripts, estilos, iframes e comentários.
    """
    try:
        soup = BeautifulSoup(html_source, 'html.parser')

        # Remove tags que não são conteúdo visível ou estrutura relevante
        tags_to_remove = ["script", "style", "noscript", "iframe", "svg", "link", "meta", "head", "form"]
        for tag in soup(tags_to_remove):
            tag.decompose()

        # Remove comentários HTML
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        # Limpar atributos excessivos
        for tag in soup.find_all(True):
            attrs = dict(tag.attrs)
            # Mantemos apenas atributos essenciais para identificação visual/semântica
            allowed_attrs = ['class', 'id', 'src', 'href', 'alt', 'title', 'role']
            for attr in attrs:
                if attr not in allowed_attrs:
                    del tag.attrs[attr]

        return soup.prettify()
    except Exception as e:
        return f"Erro ao limpar HTML: {str(e)}\nConteúdo parcial: {html_source[:500]}"

def run_scraper(url: str):
    try:
        print(f"🕵️  Acessando {url}...", file=sys.stderr)
        
        # Timeout de 15s para evitar travamentos
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status() # Lança erro se status != 200
        
        # Detectar encoding automaticamente
        if response.encoding is None:
            response.encoding = 'utf-8'
            
        raw_html = response.text
        
        # 2. Limpar o HTML
        print("🧹 Limpando código fonte...", file=sys.stderr)
        final_html = clean_html(raw_html)
        
        # 3. Salvar HTML Limpo
        try:
            with open(CLEAN_HTML_PATH, "w", encoding="utf-8") as f:
                f.write(final_html)
        except Exception as e:
            print(f"⚠️ Aviso: Não foi possível salvar clean_source.html: {e}", file=sys.stderr)
        
        # 4. Gerar Contexto para o Agente
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
        print(f"   Agora o agente pode gerar o site baseando-se neste arquivo.", file=sys.stderr)

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
    # Tenta pegar argumento da linha de comando
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if "http" in arg or "www" in arg or "." in arg:
                url = arg
                break
    
    # Se não veio por argumento, pede input
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