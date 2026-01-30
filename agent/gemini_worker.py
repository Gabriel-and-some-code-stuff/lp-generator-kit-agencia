#!/usr/bin/env python3
# gemini_worker.py
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# --- CONFIGURAÇÃO ---
load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")

# Caminhos Relativos
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
CONTEXT_FILE = PROJECT_ROOT / "contexto_para_cursor.txt"
SYSTEM_PROMPT_FILE = CURRENT_DIR / "prompts" / "system.md"
APP_CONFIG_PATH = PROJECT_ROOT / "src" / "utils" / "AppConfig.ts"
TAILWIND_CONFIG_PATH = PROJECT_ROOT / "tailwind.config.js"
CSS_DIR = CURRENT_DIR / "downloaded_css"

# Delimitadores de Segurança (Devem bater com o System Prompt)
DELIMITERS = {
    "app_config": {
        "start": "<<<<APP_CONFIG_START>>>>",
        "end": "<<<<APP_CONFIG_END>>>>"
    },
    "tailwind": {
        "start": "<<<<TAILWIND_START>>>>",
        "end": "<<<<TAILWIND_END>>>>"
    }
}

def setup_client():
    if not API_KEY:
        print("❌ Erro Crítico: A variável 'GEMINI_API_KEY' não foi encontrada.")
        print("   -> Verifique se você criou o arquivo .env na raiz do projeto.")
        sys.exit(1)
    return genai.Client(api_key=API_KEY)

def load_text(path: Path) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo não encontrado: {path}")
        sys.exit(1)

def extract_content_with_delimiters(text: str, start_tag: str, end_tag: str) -> str | None:
    """
    Extrai conteúdo exato entre delimitadores personalizados.
    Muito mais seguro que Regex em blocos Markdown.
    """
    if start_tag not in text or end_tag not in text:
        return None
    
    try:
        # Encontra o início do conteúdo (após a tag de início)
        start_index = text.find(start_tag) + len(start_tag)
        # Encontra o fim do conteúdo
        end_index = text.find(end_tag)
        
        if start_index >= end_index:
            return None
            
        content = text[start_index:end_index].strip()
        
        # Remove fences de markdown se o modelo tiver colocado acidentalmente dentro dos delimitadores
        content = content.replace("```typescript", "").replace("```javascript", "").replace("```ts", "").replace("```js", "").replace("```", "")
        
        return content.strip()
    except Exception as e:
        print(f"⚠️ Erro durante extração: {e}")
        return None

def validate_content(content: str, file_type: str) -> bool:
    """Validação básica de sanidade (Sanity Check)."""
    if not content or len(content) < 50:
        return False
        
    if file_type == "app_config":
        if "export const AppConfig" not in content:
            return False
        # Verifica se o locale está definido como pt-br
        if "locale: 'pt-br'" not in content and 'locale: "pt-br"' not in content:
            print("⚠️ Aviso: O AppConfig gerado pode não estar em PT-BR.")
            
    if file_type == "tailwind":
        if "module.exports" not in content:
            return False
        if "colors:" not in content:
            return False
            
    return True

def save_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Arquivo salvo: {path}")


def load_css_files(path: Path) -> str:
    """Concatena o conteúdo de todos os arquivos .css no diretório fornecido."""
    css_contents = []
    if not path.exists():
        return ""
    try:
        for f in sorted(path.glob("*.css")):
            try:
                with open(f, "r", encoding="utf-8") as fh:
                    css_contents.append(f"/* FILE: {f.name} */\n" + fh.read())
            except Exception as e:
                print(f"⚠️ Aviso: não foi possível ler CSS {f}: {e}")
    except Exception as e:
        print(f"⚠️ Aviso ao listar CSS em {path}: {e}")
    return "\n\n".join(css_contents)


def main():

    print("--- INICIANDO AGENTE GEMINI (Hardened Framework) ---")

    client = setup_client()

    print("📂 Lendo contexto e instruções...")
    raw_html_context = load_text(CONTEXT_FILE)
    system_instruction = load_text(SYSTEM_PROMPT_FILE)

    # REFORÇO DE CONTEXTO (Context Coupling)
    css_files_content = load_css_files(CSS_DIR)
    full_prompt = f"""
    ===== SOURCE HTML (INPUT) =====
    The following HTML represents the client's current website.
    Use this content to fill the AppConfig.
    
    {raw_html_context}
    
    ===== END OF SOURCE HTML =====
    
    ===== CSS FILES (INPUT) =====
    The following CSS files (external and inlined by the scraper) are provided to help identify colors, variables, and styles used by the site.
    {css_files_content}

    ===== END OF CSS FILES =====

    CRITICAL INSTRUCTIONS FOR GENERATION:
    1. **LANGUAGE:** All generated text MUST be in **BRAZILIAN PORTUGUESE (PT-BR)**. Do not output English.
    2. **COLOR:** Find the PRIMARY ACTION color (Buttons/Links) in the HTML and the provided CSS. Prioritize colors defined in CSS (variables in :root, rules for .btn/.cta/a:hover, etc.). Do not use white/gray as primary.
    3. **FOOTER:** Extract all contact info and links. Do not leave the footer empty.
    4. **STRUCTURE:** Follow the System Prompt rules for Multiples of 3/4 in grids.
    5. **DELIMITERS:** You MUST wrap the output in the requested delimiters:
       {DELIMITERS['app_config']['start']} ... {DELIMITERS['app_config']['end']}
       and
       {DELIMITERS['tailwind']['start']} ... {DELIMITERS['tailwind']['end']}
    """

    print("⏳ O Agente está analisando e aplicando o framework 'Hardened'...")

    try:
        # Temperatura 0.0 é crucial para seguir regras estritas
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.0, 
                top_p=0.8,
                top_k=40,
                max_output_tokens=8192
            ),
            contents=[full_prompt]
        )

        ai_output = response.text

    except Exception as e:
        print("❌ Erro na chamada à API do Gemini:")
        print(e)
        sys.exit(1)

    print("💾 Processando e Validando resposta...")

    # Extração AppConfig
    app_config_code = extract_content_with_delimiters(
        ai_output, 
        DELIMITERS['app_config']['start'], 
        DELIMITERS['app_config']['end']
    )
    
    if app_config_code and validate_content(app_config_code, "app_config"):
        save_file(APP_CONFIG_PATH, app_config_code)
    else:
        print("⚠️ ERRO CRÍTICO: Falha na geração ou validação do AppConfig.ts")
        # print("Debug - Output:", ai_output) # Descomente se necessário

    # Extração Tailwind
    tailwind_code = extract_content_with_delimiters(
        ai_output, 
        DELIMITERS['tailwind']['start'], 
        DELIMITERS['tailwind']['end']
    )
    
    if tailwind_code and validate_content(tailwind_code, "tailwind"):
        save_file(TAILWIND_CONFIG_PATH, tailwind_code)
    else:
        print("⚠️ ERRO CRÍTICO: Falha na geração ou validação do tailwind.config.js")

    print("--- PROCESSO CONCLUÍDO ---")
    print("👉 Verifique se o AppConfig.ts está em Português.")

if __name__ == "__main__":
    main()