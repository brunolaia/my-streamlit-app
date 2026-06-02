import streamlit as st
import pandas as pd

st.set_page_config(page_title="Visualizador de Excel", layout="wide")

st.title("📊 Importador de Excel")

st.write("Envie uma planilha Excel para visualizar seus dados abaixo.")

# Upload do arquivo
arquivo = st.file_uploader("📁 Importar arquivo Excel", type=["xlsx"])

# Botão para carregar
if st.button("📥 Carregar dados"):

    if arquivo is None:
        st.warning("Por favor, selecione um arquivo Excel primeiro.")
    else:
        try:
            # Ler Excel
            df = pd.read_excel(arquivo)

            st.success("Arquivo carregado com sucesso!")

            # Mostrar dados completos
            st.subheader("📄 Conteúdo da planilha")
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")