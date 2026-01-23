import streamlit as st
import pandas as pd
import os
import sys

# --- CORREÇÃO DE IMPORTAÇÃO ---
# Isso garante que o Python encontre o arquivo 'agent_v1_robusto.py'
# mesmo se você rodar o comando da pasta raiz.
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from agent_v1_robusto import processar_cliente
except ImportError as e:
    st.error(f"Erro crítico de importação: {e}")
    st.info(f"O sistema tentou buscar no diretório: {current_dir}")
    st.stop()

# --- INÍCIO DA APP ---
st.set_page_config(page_title="Gerador de LPs - Agência", page_icon="🚀", layout="wide")

st.title("🚀 Gerador de Landing Pages de Alta Conversão")
st.markdown("---")

# Sidebar - Configurações Globais
st.sidebar.header("⚙️ Configurações")
modo_deploy = st.sidebar.checkbox("Ativar Deploy (Vercel)", value=False, help="Se marcado, vai subir para nuvem. Se não, apenas gera localmente.")
if modo_deploy:
    st.sidebar.warning("⚠️ O Deploy pode levar de 2 a 5 minutos por site.")

modelo_ia = st.sidebar.selectbox("Modelo IA", ["llama3", "mistral"], index=0)

# --- ÁREA PRINCIPAL ---

tab1, tab2 = st.tabs(["🎯 Gerador Único (Teste)", "📊 Processar em Lote (CSV)"])

# ABA 1: GERADOR ÚNICO (Para testes rápidos)
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dados do Cliente")
        nome_cliente = st.text_input("Nome da Empresa", placeholder="Ex: Clínica Sorriso")
        url_cliente = st.text_input("Site Atual (URL)", placeholder="Ex: www.clinicasorriso.com.br")
        
    with col2:
        st.subheader("Estratégia")
        objetivo = st.text_area("Objetivo da LP (Instrução para IA)", 
                               placeholder="Ex: Focar em implantes dentários e passar autoridade. O público é idoso.")
        cor_marca = st.color_picker("Cor da Marca (Opcional)", "#03A9F4")

    if st.button("🚀 Gerar Landing Page", type="primary"):
        if not nome_cliente or not url_cliente:
            st.error("Preencha Nome e URL.")
        else:
            with st.status("Processando...", expanded=True) as status:
                st.write("Iniciando Agente...")
                
                # Chama o backend
                resultado = processar_cliente(
                    nome=nome_cliente,
                    url=url_cliente,
                    objetivo_especifico=objetivo,
                    cor_personalizada=cor_marca,
                    modo_deploy=modo_deploy
                )
                
                # Exibe Logs
                for line in resultado['log']:
                    st.write(line)
                
                if resultado['status'] == 'success':
                    status.update(label="Concluído!", state="complete", expanded=False)
                    st.success("Landing Page Gerada com Sucesso!")
                    
                    st.markdown(f"### 🔗 URL Final: [{resultado['url']}]({resultado['url']})")
                    
                    st.subheader("📲 Mensagem de Abordagem Sugerida:")
                    st.code(resultado['whatsapp'], language="text")
                    
                    st.info("💡 Se rodou em modo local, inicie o servidor com `npm run dev` para visualizar em localhost:3000")
                else:
                    status.update(label="Erro", state="error")
                    st.error(f"Falha: {resultado.get('msg')}")

# ABA 2: LOTE (CSV)
with tab2:
    st.info("Faça upload de um CSV com as colunas: 'Nome', 'Site Atual'. Opcional: 'Objetivo'.")
    uploaded_file = st.file_uploader("Carregar CSV", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
        
        if st.button("▶️ Processar Lista Completa"):
            st.warning("Isso pode demorar. Não feche a aba.")
            progress_bar = st.progress(0)
            
            resultados = []
            
            for index, row in df.iterrows():
                # Processamento
                nome = row.get('Nome', f"Cliente {index}")
                url = row.get('Site Atual')
                obj = row.get('Objetivo', None) # Se tiver na planilha, usa
                
                if pd.isna(url): continue
                
                st.write(f"Processando {nome}...")
                res = processar_cliente(nome, url, objetivo_especifico=obj, modo_deploy=modo_deploy)
                
                # Salva resultado no DF temporário
                resultados.append({
                    "Nome": nome,
                    "URL Original": url,
                    "Novo Site": res.get('url', 'Erro'),
                    "Mensagem": res.get('whatsapp', '')
                })
                
                # Atualiza barra
                progress_bar.progress((index + 1) / len(df))
            
            # Download
            res_df = pd.DataFrame(resultados)
            csv = res_df.to_csv(index=False).encode('utf-8')
            
            st.success("Lote Finalizado!")
            st.download_button(
                "📥 Baixar Relatório Final",
                csv,
                "resultados_lp.csv",
                "text/csv",
                key='download-csv'
            )