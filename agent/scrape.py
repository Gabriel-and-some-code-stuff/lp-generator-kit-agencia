import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def setup_selenium():
    """Configura o Chrome em modo headless."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")
    
    # Instala e configura o driver automaticamente
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_website(url):
    """Acessa a URL e retorna o texto limpo e imagens principais."""
    if not url.startswith('http'):
        url = 'https://' + url.strip()
        
    print(f"   🕵️  Lendo site: {url}...")
    driver = None
    try:
        driver = setup_selenium()
        driver.set_page_load_timeout(60)
        driver.get(url)
        time.sleep(5) # Espera carregamento de scripts
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove elementos inúteis
        for tag in soup(["script", "style", "svg", "path", "noscript", "form", "footer", "meta", "link", "iframe"]):
            tag.extract()
            
        # Extrai texto limpo
        text = soup.get_text(separator=' ', strip=True)
        # Limita tamanho para não estourar contexto do Llama3 (aprox 6k tokens)
        text = text[:15000] 
        
        # Extrai imagens (tenta pegar as maiores/mais relevantes)
        images = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                if src.startswith('//'): src = 'https:' + src
                elif src.startswith('/'): src = url.rstrip('/') + src
                
                if src.startswith('http') and not any(x in src for x in ['icon', 'logo', 'pixel', 'avatar']):
                    images.append(src)
        
        # Remove duplicatas
        unique_images = list(set(images))[:8]
        
        return {"text": text, "images": unique_images}

    except Exception as e:
        print(f"   ❌ Erro ao ler site: {e}")
        return None
    finally:
        if driver:
            driver.quit()