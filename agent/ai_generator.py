import os
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import subprocess
import time
import re

# --- CONFIGURAÇÃO ---
# Coloque sua chave no arquivo .env ou substitua aqui (menos seguro)
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
GEMINI_API_KEY = "SUA_CHAVE_DO_GOOGLE_AQUI" 

# Caminho para sua planilha local (exporte do Google Sheets como CSV para testar)
PLANILHA_INPUT = "clientes.csv" 
PLANILHA_OUTPUT = "clientes_output.csv"

# Configura o Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Configuração do Modelo (Gemini 1.5 Flash é rápido e barato, Pro é mais inteligente)
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash", # Ou "gemini-1.5-pro"
  generation_config=generation_config,
)

def ler_instrucoes():
    """Lê o arquivo AGENT_INSTRUCTIONS.md na raiz do projeto."""
    try:
        # Ajuste o caminho se o script não estiver na raiz
        with open("AGENT_INSTRUCTIONS.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("❌ Erro: AGENT_INSTRUCTIONS.md não encontrado. Verifique o caminho.")
        return ""

def scrape_site(url):
    """Acessa o site e extrai texto relevante e imagens."""
    if not url.startswith('http'):
        url = 'https://' + url
        
    print(f"🕵️  Analisando: {url}...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove scripts e estilos para limpar o texto
        for script in soup(["script", "style", "svg", "path"]):
            script.extract()
            
        text = soup.get_text(separator=' ', strip=True)[:20000] # Limite para não estourar tokens
        
        # Tenta encontrar imagens grandes
        images = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = url.rstrip('/') + src
                
                if src.startswith('http'):
                    images.append(src)
        
        return {"text": text, "images": list(set(images[:8]))} # Remove duplicatas e limita
    except Exception as e:
        print(f"❌ Erro ao acessar {url}: {e}")
        return None

def gerar_config_ai(site_data, system_prompt):
    """Usa o Gemini para gerar o código do AppConfig.ts e a cor."""
    print("🧠 Gerando estratégia e copy com Gemini...")
    
    prompt = f"""
    {system_prompt}

    --- DADOS DO SITE DO CLIENTE ---
    URL: {site_data.get('url', 'N/A')}
    
    IMAGENS DISPONÍVEIS (Escolha as melhores para cada seção):
    {json.dumps(site_data['images'])}

    TEXTO DO SITE:
    {site_data['text']}
    
    --- SUA TAREFA ---
    Gere o JSON final contendo 'app_config' (o código TS completo) e 'primary_color' (Hex).
    """

    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        print(f"❌ Erro na IA: {e}")
        return None

def atualizar_arquivos(ai_output):
    """Sobrescreve os arquivos locais com o conteúdo gerado."""
    print("💾 Gravando arquivos...")
    
    if not ai_output:
        return False

    try:
        # 1. AppConfig.ts
        config_content = ai_output.get('app_config')
        if not config_content:
             # Fallback caso a IA não retorne a chave exata
             print("⚠️  Aviso: Estrutura JSON inesperada. Tentando salvar cru.")
             # Aqui você pode adicionar lógica de recuperação
             return False

        with open("src/utils/AppConfig.ts", "w", encoding="utf-8") as f:
            f.write(config_content)
            
        # 2. tailwind.config.js (Atualiza a cor)
        cor = ai_output.get('primary_color', '#03A9F4') # Azul padrão se falhar
        
        with open("tailwind.config.js", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Regex para trocar a cor 500
        new_content = re.sub(r"500: '#[A-Fa-f0-9]{6}'", f"500: '{cor}'", content)
        
        with open("tailwind.config.js", "w", encoding="utf-8") as f:
            f.write(new_content)
            
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar arquivos: {e}")
        return False

def build_and_deploy(cliente_nome):
    """Formata, Builda e Faz Deploy na Vercel."""
    print("🚀 Iniciando Build e Deploy...")
    
    # Nome do projeto na Vercel (limpo)
    project_slug = re.sub(r'[^a-z0-9-]', '', cliente_nome.lower().replace(' ', '-'))
    project_name = f"lp-{project_slug}"
    
    try:
        # 1. Formata o código (Crucial para o template)
        print("   - Formatando código...")
        subprocess.run("npm run format", shell=True, check=True, stdout=subprocess.DEVNULL)
        
        # 2. Deploy
        print(f"   - Enviando para Vercel ({project_name})...")
        # --prod: deploy produção
        # --yes: pular confirmações
        # --name: define o nome do projeto
        # --force: força rebuild se já existir
        cmd = f"vercel --prod --yes --force --name {project_name}"
        
        result = subprocess.run(
            cmd, 
            capture_output=True, text=True, shell=True
        )
        
        if result.returncode == 0:
            url = result.stdout.strip()
            # As vezes a vercel retorna mais texto, pegamos a url
            # Padrão: https://projeto.vercel.app
            urls = re.findall(r'https://[^\s]+vercel.app', url)
            if urls:
                final_url = urls[0]
                print(f"✅ Deploy Concluído! URL: {final_url}")
                return final_url
            else:
                return url # Retorna o output bruto se não achar url padrão
        else:
            print(f"❌ Erro no deploy Vercel:\n{result.stderr}")
            return "Erro Deploy"
            
    except Exception as e:
        print(f"❌ Erro no processo de build: {e}")
        return "Erro Processo"

def main():
    print("🤖 Iniciando Agente de Landing Pages (Powered by Gemini)...")
    system_prompt = ler_instrucoes()
    
    if not system_prompt:
        return

    # Lê o CSV (Col A=Cliente, Col C=Website)
    # Supondo que a planilha exportada tenha cabeçalhos na linha 1
    # Se não tiver, ajuste 'header=None' e use índices
    try:
        df = pd.read_csv(PLANILHA_INPUT)
    except FileNotFoundError:
        print(f"❌ Arquivo {PLANILHA_INPUT} não encontrado. Exporte sua planilha para CSV.")
        return

    # Garante que a coluna de output existe
    if 'Landing Page' not in df.columns:
        df['Landing Page'] = ""

    for index, row in df.iterrows():
        # Ajuste estes nomes conforme o cabeçalho do seu CSV
        cliente = str(row.iloc[0]) # Coluna A (índice 0)
        url = str(row.iloc[2])     # Coluna C (índice 2)
        
        # Pula se não tiver URL ou se já tiver sido gerado (opcional)
        if pd.isna(url) or url == 'nan' or not url.strip():
            continue
            
        print(f"\n==================================================")
        print(f"🏗️  Processando Cliente {index+1}: {cliente}")
        print(f"🔗  URL: {url}")
        print(f"==================================================")
        
        # 1. Scrape
        site_data = scrape_site(url)
        if not site_data:
            df.at[index, 'Landing Page'] = "Erro: Site inacessível"
            continue
            
        site_data['url'] = url
        
        # 2. IA Generation
        ai_output = gerar_config_ai(site_data, system_prompt)
        
        # 3. Atualizar Código Local
        sucesso_arquivos = atualizar_arquivos(ai_output)
        
        if sucesso_arquivos:
            # 4. Deploy
            final_url = build_and_deploy(cliente)
            
            # 5. Salvar na Coluna D (que no pandas seria índice 3, se existir, ou criamos nova)
            # Como criamos a coluna 'Landing Page', salvamos nela
            df.at[index, 'Landing Page'] = final_url
        else:
            df.at[index, 'Landing Page'] = "Erro: Falha na IA"
        
        # Salva o progresso a cada cliente (segurança)
        df.to_csv(PLANILHA_OUTPUT, index=False)
        
        # Pausa para respirar
        time.sleep(2)

    print("\n🏁 Processo finalizado! Verifique 'clientes_output.csv'.")

if __name__ == "__main__":
    main()