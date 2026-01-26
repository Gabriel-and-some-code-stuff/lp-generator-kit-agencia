import streamlit as st
import pandas as pd
import os
import sys

# Corrige imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from agent_v1_robusto import run_agent, MODELO
except ImportError:
    st.error("Erro: agent_v1_robusto.py não encontrado.")
    st.stop()

st.set_page_config(page_title="Agência LP Generator Pro", page_icon="⚡", layout="wide")

st.title("⚡ Gerador de Landing Pages B2B (High Converting)")
st.caption(f"Engine: {MODELO} | Modo: Batch Processing")

with st.sidebar:
    st.header("Configurações")
    modo_deploy = st.checkbox("Ativar Deploy (Vercel)", value=False)
    if modo_deploy:
        st.warning("⚠️ Deploy ativo. Cada site levará ~3 min.")
    
    st.divider()
    st.info("💡 Dica: Use o arquivo clientes.csv para processar em massa.")

# --- INTERFACE ---

tab_lote, tab_unico = st.tabs(["🚀 Processamento em Lote", "🎯 Teste Único"])

with tab_lote:
    uploaded = st.file_uploader("Upload clientes.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        st.dataframe(df.head())
        
        if st.button("Iniciar Fila de Produção", type="primary"):
            progress = st.progress(0)
            log_box = st.empty()
            results = []
            
            for i, row in df.iterrows():
                nome = row.get('Nome', f"Cliente {i}")
                url = row.get('Site Atual', '')
                obj = row.get('Objetivo', 'Vender serviços')
                
                log_box.info(f"🔄 Processando {i+1}/{len(df)}: {nome}")
                
                # CHAMA O AGENTE PRO
                res = run_agent(nome, url, obj, modo_deploy)
                
                status_icon = "✅" if res['status'] == 'success' else "❌"
                results.append({
                    "Cliente": nome,
                    "Status": status_icon,
                    "Nova LP": res.get('url', '-'),
                    "Msg WhatsApp": res.get('whatsapp', '-')
                })
                
                progress.progress((i + 1) / len(df))
            
            st.success("Fila Finalizada!")
            st.dataframe(pd.DataFrame(results))
            
            # Botão Download
            csv = pd.DataFrame(results).to_csv(index=False).encode('utf-8')
            st.download_button("Baixar Relatório", csv, "relatorio_lps.csv", "text/csv")

with tab_unico:
    c1, c2 = st.columns(2)
    nome = c1.text_input("Nome Cliente")
    url = c2.text_input("Site Atual")
    obj = st.text_area("Objetivo", "Autoridade e Vendas")
    
    if st.button("Gerar LP Teste"):
        with st.status("Trabalhando...") as s:
            res = run_agent(nome, url, obj, modo_deploy)
            if res['status'] == 'success':
                s.update(label="Sucesso!", state="complete")
                st.success(f"Link: {res['url']}")
                st.code(res['whatsapp'])
            else:
                s.update(label="Erro", state="error")
                st.error(res['msg'])