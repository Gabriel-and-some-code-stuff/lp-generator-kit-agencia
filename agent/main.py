import pandas as pd
import os

# Configurações
PLANILHA_INPUT = "clientes.csv"  # Nome do arquivo CSV exportado da planilha
PLANILHA_OUTPUT = "clientes_processados.csv" # Onde vamos salvar os resultados

def ler_planilha():
    """
    Lê o arquivo CSV exportado do Google Sheets.
    Assume que:
    - Coluna A (índice 0) é o Nome do Cliente
    - Coluna C (índice 2) é a URL do Site
    """
    if not os.path.exists(PLANILHA_INPUT):
        print(f"❌ Erro: Arquivo '{PLANILHA_INPUT}' não encontrado na raiz.")
        print("   -> Exporte sua planilha do Google como CSV e salve aqui.")
        return None

    try:
        # Lê o CSV. O header=0 significa que a primeira linha é o cabeçalho.
        # Ajuste 'usecols' se souber os nomes exatos das colunas, ou use índices.
        # Aqui, vamos ler tudo e filtrar pelo índice para garantir.
        df = pd.read_csv(PLANILHA_INPUT)
        
        print(f"✅ Planilha carregada com sucesso! Encontradas {len(df)} linhas.")
        return df
    
    except Exception as e:
        print(f"❌ Erro ao ler CSV: {e}")
        return None

def processar_clientes(df):
    """Itera sobre os clientes e extrai as informações básicas."""
    
    # Lista para guardar resultados (será útil na fase de escrita)
    resultados = []

    for index, row in df.iterrows():
        # Acessa por posição (iloc) ou nome da coluna se o CSV tiver cabeçalho limpo
        # Ajuste os índices conforme sua planilha real:
        # Coluna A -> índice 0 (Nome)
        # Coluna C -> índice 2 (URL)
        
        try:
            nome_cliente = str(row.iloc[0]).strip()
            url_site = str(row.iloc[2]).strip()
            
            # Validação básica
            if pd.isna(url_site) or url_site == 'nan' or not url_site.startswith('http'):
                print(f"⚠️  Linha {index + 2}: URL inválida ou vazia para {nome_cliente}. Pulando.")
                continue

            print(f"🚀 Processando Cliente {index + 1}: {nome_cliente}")
            print(f"   🔗 URL Alvo: {url_site}")
            
            # AQUI ENTRARÁ A FASE 2 (SCRAPING) E 3 (IA)
            # Por enquanto, apenas simulamos
            lp_gerada = "https://lp-teste.vercel.app" # Placeholder
            
            # Adiciona ao resultado para salvar depois
            resultados.append({
                "Nome": nome_cliente,
                "URL Original": url_site,
                "LP Gerada": lp_gerada
            })
            
        except Exception as e:
            print(f"❌ Erro na linha {index + 2}: {e}")

    return pd.DataFrame(resultados)

if __name__ == "__main__":
    print("🤖 Iniciando Agente de Landing Pages...")
    
    df_clientes = ler_planilha()
    
    if df_clientes is not None:
        df_resultados = processar_clientes(df_clientes)
        
        # Salva o output (simulando a escrita na Coluna E)
        if not df_resultados.empty:
            df_resultados.to_csv(PLANILHA_OUTPUT, index=False)
            print(f"\n💾 Resultados salvos em '{PLANILHA_OUTPUT}'")
        else:
            print("\n⚠️ Nenhum cliente processado com sucesso.")