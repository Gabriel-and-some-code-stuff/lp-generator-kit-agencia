import time
import re
import os
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Nome do arquivo que o Cursor vai ler
ARQUIVO_CONTEXTO = "contexto_para_cursor.txt"

def limpar_texto(texto):
    """
    Remove excesso de espaços e caracteres irrelevantes para economizar tokens
    do Cursor, mantendo a semântica para o Copywriting.
    """
    # Mantém pontuação, acentos, R$ e caracteres alfanuméricos
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

def extrair_dados_site(url, nome_cliente):
    print(f"🕵️  Iniciando leitura de: {nome_cliente} ({url})...")
    
    # Configuração 'Headless' leve (não abre janela)
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3") # Silencia logs do chrome
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Adiciona protocolo se faltar
        if not url.startswith('http'):
            url = 'https://' + url
            
        driver.get(url)
        # Tempo para carregar JavaScript (React/Angular sites)
        time.sleep(5) 
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Remove navegação, rodapé e scripts para focar no conteúdo principal
        for tag in soup(["script", "style", "nav", "footer", "svg", "noscript", "iframe", "header"]):
            tag.extract()
            
        # Extrai texto visível
        texto_bruto = soup.get_text(separator='\n')
        texto_limpo = limpar_texto(texto_bruto)[:6000] # 6k caracteres é um bom contexto pro Claude
        
        # Salva o arquivo para o Cursor
        path_arquivo = os.path.join(os.getcwd(), ARQUIVO_CONTEXTO)
        
        with open(path_arquivo, "w", encoding="utf-8") as f:
            f.write(f"=== DADOS DO CLIENTE ===\n")
            f.write(f"NOME: {nome_cliente}\n")
            f.write(f"URL ORIGINAL: {url}\n")
            f.write(f"\n=== CONTEÚDO EXTRAÍDO DO SITE ===\n")
            f.write(texto_limpo)
            
        print(f"✅ Sucesso! Dados salvos em: {ARQUIVO_CONTEXTO}")
        print(f"👉 PRÓXIMO PASSO: Abra o Composer do Cursor (Ctrl+I) e digite: 'Gerar LP'")
        
    except Exception as e:
        print(f"❌ Erro ao ler o site: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    # Modo interativo simples
    print("--- 🤖 FERRAMENTA DE PREPARAÇÃO PARA O CURSOR ---")
    try:
        nome = input("Nome do Cliente: ")
        link = input("Link do Site: ")
        if nome and link:
            extrair_dados_site(link, nome)
        else:
            print("❌ Dados inválidos.")
    except KeyboardInterrupt:
        print("\nOperação cancelada.")