import os
import re
import sys
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# --- CONFIGURAÇÃO ---
# 1. Carrega variáveis do arquivo .env (resolve o problema da chave não lida)
load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")

# Caminhos Relativos
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
CONTEXT_FILE = PROJECT_ROOT / "contexto_para_cursor.txt"
SYSTEM_PROMPT_FILE = CURRENT_DIR / "prompts" / "system.md"
APP_CONFIG_PATH = PROJECT_ROOT / "src" / "utils" / "AppConfig.ts"
TAILWIND_CONFIG_PATH = PROJECT_ROOT / "tailwind.config.js"

def setup_client():
    if not API_KEY:
        print("❌ Erro Crítico: A variável 'GEMINI_API_KEY' não foi encontrada.")
        print("   -> Verifique se você criou o arquivo .env na raiz do projeto.")
        sys.exit(1)
    
    # Inicializa o cliente com a nova SDK
    return genai.Client(api_key=API_KEY)

def load_text(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo não encontrado: {path}")
        sys.exit(1)

def extract_code(text, lang):
    """
    Extrai o conteúdo de blocos de código Markdown.
    """
    pattern = rf"```{lang}\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def save_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Arquivo salvo: {path.name}")

def main():
    print("--- INICIANDO AGENTE GEMINI (v2) ---")
    
    client = setup_client()
    
    print("📂 Lendo contexto e instruções...")
    raw_html_context = load_text(CONTEXT_FILE)
    system_instruction = load_text(SYSTEM_PROMPT_FILE)
    
    full_prompt = f"""
    CONTEXTO DO SITE (HTML BRUTO):
    {raw_html_context}
    """

    print("⏳ O Agente está pensando...")
    
    try:
        # Chamada usando a nova SDK google-genai
        response = client.models.generate_content(
            model="gemini-2.0-flash", # Ou "gemini-1.5-pro" se preferir
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
                top_p=0.8,
                top_k=40,
                max_output_tokens=8192
            ),
            contents=[full_prompt]
        )
        
        ai_output = response.text
        
    except Exception as e:
        print(f"❌ Erro na API do Gemini: {e}")
        sys.exit(1)

    print("💾 Processando resposta...")
    
    # 1. Processar AppConfig
    app_config_code = extract_code(ai_output, "typescript") or extract_code(ai_output, "ts")
    if app_config_code:
        save_file(APP_CONFIG_PATH, app_config_code)
    else:
        print("⚠️  ALERTA: Não foi possível extrair o AppConfig.ts.")

    # 2. Processar Tailwind
    tailwind_code = extract_code(ai_output, "javascript") or extract_code(ai_output, "js")
    if tailwind_code:
        save_file(TAILWIND_CONFIG_PATH, tailwind_code)
    else:
        print("⚠️  ALERTA: Não foi possível extrair o tailwind.config.js.")

    print("--- PROCESSO CONCLUÍDO ---")
    print("👉 Rode 'npm run dev' para testar.")

if __name__ == "__main__":
    main() 