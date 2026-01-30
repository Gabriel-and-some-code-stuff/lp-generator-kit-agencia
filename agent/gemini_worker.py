#!/usr/bin/env python3
# gemini_worker.py
import os
import re
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

def robust_extract_code(text: str, target_signature: str) -> str | None:
    """
    Extrai código de blocos markdown ``` ``` contendo a assinatura alvo.
    Possui fallback direto no texto bruto.
    """
    pattern = r"```(?:\w+)?\s*\n(.*?)\n```"
    matches = re.findall(pattern, text, re.DOTALL)

    best_match = None

    for match in matches:
        if target_signature in match:
            best_match = match
            break

    if not best_match and target_signature in text:
        start_index = text.find(target_signature)
        best_match = text[start_index:]
        if len(best_match) > 20000:
            best_match = best_match[:20000]

    if best_match:
        lines = best_match.splitlines()
        cleaned_lines = []
        for line in lines:
            if "src/utils/AppConfig.ts" in line or "tailwind.config.js" in line:
                continue
            cleaned_lines.append(line)
        return "\n".join(cleaned_lines).strip()

    return None

def save_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Arquivo salvo: {path}")

def main():
    print("--- INICIANDO AGENTE GEMINI (v2.5 - Flash) ---")

    client = setup_client()

    print("📂 Lendo contexto e instruções...")
    raw_html_context = load_text(CONTEXT_FILE)
    system_instruction = load_text(SYSTEM_PROMPT_FILE)

    full_prompt = f"""
CONTEXTO DO SITE (HTML BRUTO):
{raw_html_context}
"""

    print("⏳ O Agente está analisando e gerando código...")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1,
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

    print("💾 Processando resposta do Gemini...")

    # AppConfig.ts
    app_config_code = robust_extract_code(ai_output, "export const AppConfig =")
    if app_config_code:
        save_file(APP_CONFIG_PATH, app_config_code)
    else:
        print("⚠️ ALERTA: Não foi possível extrair o AppConfig.ts.")
        print(ai_output[:1000])

    # tailwind.config.js
    tailwind_code = robust_extract_code(ai_output, "module.exports = {")
    if tailwind_code:
        save_file(TAILWIND_CONFIG_PATH, tailwind_code)
    else:
        print("⚠️ ALERTA: Não foi possível extrair o tailwind.config.js.")

    print("--- PROCESSO CONCLUÍDO ---")
    print("👉 Rode 'npm run dev' para testar.")

if __name__ == "__main__":
    main()
