import streamlit as st
import pandas as pd
import os
import sys

# --- CORREÇÃO DE PATH ---
# Garante que o python encontre o arquivo no mesmo diretório
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # CORREÇÃO: Importamos APENAS a função. Removemos 'MODELO' que não existe mais.
    from agent_v1_robusto import processar_cliente as run_agent
    
    # Definimos o nome manualmente para a interface, já que agora é fixo no LM Studio
    MODELO = "LM Studio (Server Local)" 
    
except ImportError as e:
    st.error(f"Erro de Importação: {e}")
    st.info("Verifique se 'agent_v1_robusto.py' está na pasta 'agent'.")
    st.stop()

st.set_page_config(page_title="Agência LP Generator Pro", page_icon="⚡", layout="wide")

st.title("⚡ Gerador de Landing Pages B2B (High Converting)")
st.caption(f"Engine: {MODELO} | Modo: Batch Processing")

with st.sidebar:
    st.header("Configurações")
    modo_deploy = st.checkbox("Ativar Deploy (Vercel)", value=False)
    if modo_deploy:
        st.warning("⚠️ Deploy ativo. Processo mais lento.")
    st.divider()
    st.info("💡 Dica: Use o CSV para processar em massa.")

# --- TABS ---
tab_lote, tab_unico = st.tabs(["🚀 Lote (CSV)", "🎯 Teste Único"])

with tab_lote:
    uploaded = st.file_uploader("Upload clientes.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        st.dataframe(df.head())
        
        if st.button("Iniciar Fila", type="primary"):
            progress = st.progress(0)
            log_box = st.empty()
            results = []
            
            for i, row in df.iterrows():
                nome = row.get('Nome', f"Cliente {i}")
                url = row.get('Site Atual', '')
                obj = row.get('Objetivo', 'Vender serviços')
                
                log_box.info(f"🔄 Processando {i+1}/{len(df)}: {nome}")
                
                try:
                    # Executa o agente
                    res = run_agent(nome, url, obj, modo_deploy=modo_deploy)
                    
                    status = "✅" if res['status'] == 'success' else "❌"
                    results.append({
                        "Cliente": nome,
                        "Status": status,
                        "URL": res.get('url', '-'),
                        "WhatsApp": res.get('whatsapp', '-')
                    })
                except Exception as e:
                    results.append({"Cliente": nome, "Status": "❌ ERRO", "URL": str(e)})
                
                progress.progress((i + 1) / len(df))
            
            st.success("Concluído!")
            st.dataframe(pd.DataFrame(results))
            
            # Botão Download
            csv = pd.DataFrame(results).to_csv(index=False).encode('utf-8')
            st.download_button("Baixar Relatório", csv, "relatorio_lps.csv", "text/csv")

with tab_unico:
    c1, c2 = st.columns(2)
    nome = c1.text_input("Nome Cliente")
    url = c2.text_input("Site Atual (URL)")
    obj = st.text_area("Objetivo", "Autoridade e Vendas")
    
    if st.button("Gerar LP"):
        if not nome or not url:
            st.warning("Preencha os campos.")
        else:
            with st.status("Agente trabalhando...") as s:
                try:
                    # Executa o agente
                    res = run_agent(nome, url, obj, modo_deploy=modo_deploy)
                    
                    if res['status'] == 'success':
                        s.update(label="Sucesso!", state="complete")
                        st.success(f"Link: {res['url']}")
                        st.code(res['whatsapp'])
                        
                        # Mostra logs de forma organizada
                        with st.expander("Ver Logs Detalhados"):
                            for linha in res.get('log', []):
                                st.text(linha)
                    else:
                        s.update(label="Erro", state="error")
                        st.error(res.get('msg', 'Erro desconhecido'))
                        with st.expander("Ver Detalhes do Erro"):
                             for linha in res.get('log', []):
                                st.text(linha)
                                
                except Exception as e:
                    s.update(label="Erro Crítico", state="error")
                    st.error(str(e))