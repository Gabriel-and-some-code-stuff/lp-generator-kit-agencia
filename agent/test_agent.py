from agent_v1_robusto import setup_selenium
from bs4 import BeautifulSoup
import time

def testar_leitura(url):
    print(f"🕵️  Testando leitura de: {url}")
    
    driver = setup_selenium()
    if not driver:
        print("❌ Erro ao iniciar driver.")
        return

    try:
        driver.get(url)
        time.sleep(5) # Espera um pouco mais para garantir
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Remove lixo para ver o que sobra
        for tag in soup(["script", "style", "svg", "form", "footer", "nav", "noscript"]):
            tag.extract()
            
        texto = soup.get_text(separator=' ', strip=True)
        
        print("\n--- RESUMO DA EXTRAÇÃO ---")
        print(f"Tamanho do texto extraído: {len(texto)} caracteres")
        print(f"Primeiros 500 caracteres: \n{texto[:500]}...")
        
        images = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if src and src.startswith('http'):
                images.append(src)
                
        print(f"\nImagens encontradas: {len(images)}")
        if len(images) > 0:
            print(f"Exemplo: {images[0]}")
        else:
            print("⚠️ Nenhuma imagem válida encontrada (o fallback será usado).")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    site = input("Digite a URL para testar: ")
    testar_leitura(site)