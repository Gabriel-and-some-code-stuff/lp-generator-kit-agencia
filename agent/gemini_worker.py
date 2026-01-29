import os
import re
import sys
import time
import google.generativeai as genai
from pathlib import Path

# --- CONFIGURAÇÃO ---
# Para uso empresarial/pessoal rápido, a API Key é a via mais fácil.
# Se estiver usando Vertex AI (GCP), a configuração muda levemente, mas vamos focar no padrão.
API_KEY = os.environ.get("GEMINI_API_KEY")

# Caminhos Relativos (Baseados na estrutura do seu projeto)
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
CONTEXT_FILE = PROJECT_ROOT / "contexto_para_cursor.txt"
SYSTEM_PROMPT_FILE = CURRENT_DIR / "prompts" / "system.md"
APP_CONFIG_PATH = PROJECT_ROOT / "src" / "utils" / "AppConfig.ts"
TAILWIND_CONFIG_PATH = PROJECT_ROOT / "tailwind.config.js"

def setup_gemini():
    if not API_KEY:
        print("❌ Erro Crítico: A variável de ambiente 'GEMINI_API_KEY' não está definida.")
        print("   -> Defina com: export GEMINI_API_KEY='sua_chave_aqui' (Linux/Mac) ou set GEMINI_API_KEY='...' (Windows)")
        sys.exit(1)
        
    genai.configure(api_key=API_KEY)
    
    # Configurações para garantir código limpo e consistente
    generation_config = {
        "temperature": 0.2, # Baixa temperatura = Mais precisão, menos "alucinação" criativa
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 8192,
    }
    
    # Usando o modelo Pro 1.5 (Melhor custo-benefício e janela de contexto para ler HTML inteiro)
    # Se tiver acesso ao 1.5 Pro (versão mais recente), use. Senão 'gemini-1.5-flash' é ultra rápido.
    model_name = "gemini-3.0-pro-latest" 
    
    print(f"🤖 Conectando ao modelo: {model_name}")
    return genai.GenerativeModel(
        model_name=model_name, 
        generation_config=generation_config
    )

def load_text(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo não encontrado: {path}")
        # Se for o system prompt, é crítico. Se for o contexto, talvez o scraper falhou.
        sys.exit(1)

def extract_code(text, lang):
    """
    Extrai o conteúdo de blocos de código Markdown.
    Ex: ```typescript ... ```
    """
    pattern = rf"```{lang}\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def save_file(path, content):
    # Cria diretórios se não existirem
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Arquivo salvo com sucesso: {path.name}")

def main():
    print("--- INICIANDO AGENTE GEMINI ---")
    
    # 1. Setup
    model = setup_gemini()
    
    # 2. Carregar Inputs
    print("📂 Lendo dados do scraper...")
    raw_html_context = load_text(CONTEXT_FILE)
    
    print("brain Carregando instruções do sistema (Prompt Perfeito)...")
    system_instruction = load_text(SYSTEM_PROMPT_FILE)
    
    # 3. Montar Prompt
    # Combinamos a Persona (System) com os Dados (User)
    full_prompt = f"""
{system_instruction}

---
Abaixo está o conteúdo bruto extraído do site do cliente. Use-o como fonte da verdade.

=== CONTEXTO DO SITE (HTML) ===
{raw_html_context}
"""

    # 4. Inferência
    print("⏳ O Agente está pensando... (Isso pode levar uns 30s)")
    try:
        response = model.generate_content(full_prompt)
        ai_output = response.text
    except Exception as e:
        print(f"❌ Erro na API do Gemini: {e}")
        sys.exit(1)

    # 5. Processamento e Salvamento
    print("💾 Processando resposta e gerando arquivos...")
    
    # Extrair AppConfig (TypeScript)
    app_config_code = extract_code(ai_output, "typescript")
    if not app_config_code:
        # Tenta fallback para 'ts' ou sem tag se o modelo esquecer
        app_config_code = extract_code(ai_output, "ts")
        
    if app_config_code:
        save_file(APP_CONFIG_PATH, app_config_code)
    else:
        print("⚠️  ALERTA: O Agente não retornou um bloco de código TypeScript válido para o AppConfig.")
        # Debug: Salvar o raw response para entender o erro
        with open("debug_gemini_response.md", "w", encoding="utf-8") as f:
            f.write(ai_output)

    # Extrair Tailwind Config (JavaScript)
    tailwind_code = extract_code(ai_output, "javascript")
    if not tailwind_code:
        tailwind_code = extract_code(ai_output, "js")
        
    if tailwind_code:
        save_file(TAILWIND_CONFIG_PATH, tailwind_code)
    else:
        print("⚠️  ALERTA: O Agente não retornou um bloco JavaScript válido para o Tailwind.")

    print("--- PROCESSO CONCLUÍDO ---")
    print("👉 Agora rode 'npm run dev' para ver o site mágico!")

if __name__ == "__main__":
    main()