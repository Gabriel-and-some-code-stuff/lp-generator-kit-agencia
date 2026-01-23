import pandas as pd
import time
import os
from scrape import scrape_website
from ai_generator import gerar_config_site
from deploy import atualizar_arquivos_locais, deploy_vercel

PLANILHA_INPUT = "clientes.csv" 
PLANILHA_OUTPUT = "clientes_processados.csv"

def main():
    print("\n🤖 INICIANDO AGENTE GERADOR DE LPs (Ollama)")
    print("===========================================\n")

    # Verifica planilha
    caminho_csv = PLANILHA_INPUT
    if not os.path.exists(caminho_csv):
        caminho_csv = "../" + PLANILHA_INPUT
        if not os.path.exists(caminho_csv):
            print(f"❌ Planilha '{PLANILHA_INPUT}' não encontrada.")
            return

    try:
        df = pd.read_csv(caminho_csv)
    except Exception as e:
        print(f"❌ Erro ao ler CSV: {e}")
        return

    # Garante que a coluna de output existe (Novo Site - Coluna D)
    if 'Novo Site' not in df.columns:
        df['Novo Site'] = ""

    for index, row in df.iterrows():
        try:
            # Tenta pegar pelo nome da coluna, fallback para índice
            # A=0, B=1, C=2 (Site Atual), D=3 (Novo Site)
            cliente = str(row.get('Nome', row.iloc[0]))
            url_atual = str(row.get('Site Atual', row.iloc[2]))
            novo_site_atual = str(row.get('Novo Site', row.iloc[3])) if len(row) > 3 else ""
        except Exception:
            print("⚠️ Erro ao ler linha da planilha. Pulando.")
            continue

        # Validações para pular
        if pd.isna(url_atual) or len(url_atual) < 5 or url_atual == 'nan':
            continue
        
        # Se já tem site gerado, pula
        if "vercel.app" in novo_site_atual:
            print(f"⏩ {cliente}: Já processado. Pulando.")
            continue

        print(f"\n▶️  Processando: {cliente}")
        
        # 1. Scrape
        site_data = scrape_website(url_atual)
        if not site_data:
            df.at[index, 'Novo Site'] = "Erro: Site Off"
            continue
        site_data['url'] = url_atual
        
        # 2. IA Generation
        config = gerar_config_site(site_data)
        
        # 3. Build & Deploy
        if atualizar_arquivos_locais(config):
            final_url = deploy_vercel(cliente)
            print(f"   ✅ SUCESSO: {final_url}")
            # Se usou nome da coluna, salva nela, senão usa índice
            if 'Novo Site' in df.columns:
                df.at[index, 'Novo Site'] = final_url
            else:
                 df.iloc[index, 3] = final_url
        else:
            print("   ❌ Falha na geração da IA")
            if 'Novo Site' in df.columns:
                df.at[index, 'Novo Site'] = "Erro IA"
            
        # Salva o progresso
        df.to_csv(PLANILHA_OUTPUT, index=False)
        
        # Pausa para não sobrecarregar
        time.sleep(2)

    print(f"\n🏁 FIM. Resultados salvos em '{PLANILHA_OUTPUT}'.")

if __name__ == "__main__":
    main()