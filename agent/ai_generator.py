import json
import requests
import re

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODELO = "llama3" 

def ler_instrucoes():
    """Lê o arquivo de instruções mestre."""
    try:
        # Tenta ler na raiz ou na pasta pai
        paths = ["AGENT_INSTRUCTIONS.md", "../AGENT_INSTRUCTIONS.md"]
        for path in paths:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
            except FileNotFoundError:
                continue
        return ""
    except Exception:
        return ""

def extract_json(text):
    """
    Tenta extrair um JSON válido de uma string que pode conter texto extra.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = text[start:end]
                return json.loads(json_str)
        except:
            pass
    return None

def gerar_config_site(site_data):
    """Envia dados para o Ollama e recebe o JSON de configuração."""
    print(f"   🧠 Raciocinando com {MODELO}...")
    
    instrucoes = ler_instrucoes()
    if not instrucoes:
        print("   ❌ Erro: AGENT_INSTRUCTIONS.md não encontrado.")
        return None

    user_prompt = f"""
    {instrucoes}

    --- DADOS DO SITE ATUAL ---
    URL: {site_data.get('url')}
    IMAGENS DISPONÍVEIS: {json.dumps(site_data['images'])}
    CONTEÚDO DO SITE: {site_data['text']}
    
    --- SUA TAREFA ---
    Analise o conteúdo, identifique o nicho e gere o JSON de configuração para a nova Landing Page.
    
    IMPORTANTE: Retorne APENAS o JSON válido. Não escreva nada antes ou depois.
    O JSON deve ter exatamente estas chaves:
    {{
        "app_config": "Código TypeScript completo do AppConfig aqui...",
        "primary_color": "#HEXCODE"
    }}
    """
    
    payload = {
        "model": MODELO,
        "prompt": user_prompt,
        "stream": False,
        "format": "json", # Força saída JSON
        "options": {
            "temperature": 0.6,
            "num_ctx": 8192
        }
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        # Usa a função de limpeza para evitar erros
        json_limpo = extract_json(result['response'])
        if not json_limpo:
             print("   ❌ Erro: O modelo não retornou um JSON válido.")
             return None
             
        return json_limpo
        
    except Exception as e:
        print(f"   ❌ Erro no Ollama: {e}")
        return None