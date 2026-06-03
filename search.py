import os
import streamlit as st

st.set_page_config(
    page_title="Localizador de Arquivos",
    layout="wide"
)

st.title("🔍 Pesquisa de Arquivos")

arquivo_txt = st.file_uploader(
    "Selecione o banco de dados (.txt)",
    type=["txt"]
)

if arquivo_txt:

    conteudo = arquivo_txt.read().decode(
        "utf-8",
        errors="ignore"
    )

    caminhos = [
        linha.strip()
        for linha in conteudo.splitlines()
        if linha.strip()
    ]

    busca = st.text_input(
        "Digite o nome do arquivo"
    )

    if busca:

        resultados = []

        for caminho in caminhos:

            nome_arquivo = caminho.split("\\")[-1]

            if busca.lower() in nome_arquivo.lower():
                resultados.append(caminho)

        st.success(
            f"Encontrados: {len(resultados)} arquivo(s)"
        )

        if not resultados:
            st.warning("Nenhum arquivo encontrado.")

        for i, caminho in enumerate(resultados):

            caminho = caminho.strip()

            # Nome do arquivo
            nome_arquivo = caminho.split("\\")[-1]

            # Pasta onde está o arquivo
            pasta = caminho.rsplit("\\", 1)[0]

            col1, col2 = st.columns([12, 1])

            with col1:
                st.markdown(
                    f"<div style='padding:0;margin:0'>{nome_arquivo}</div>",
                    unsafe_allow_html=True
                )

            with col2:
                if st.button(
                    "📂",
                    key=f"abrir_pasta_{i}",
                    help="Abrir pasta"
                ):
                    try:
                        os.startfile(pasta)
                    except Exception as e:
                        st.error(f"Erro ao abrir pasta: {e}")
