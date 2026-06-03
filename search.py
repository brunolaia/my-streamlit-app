import streamlit as st
from pathlib import Path
from urllib.parse import quote

st.set_page_config(page_title="Localizador de Arquivos")

st.title("🔍 Pesquisa de Arquivos")

arquivo_txt = st.file_uploader(
    "Selecione o banco de dados (.txt)",
    type=["txt"]
)

if arquivo_txt:
    conteudo = arquivo_txt.read().decode("utf-8", errors="ignore")

    caminhos = [
        linha.strip()
        for linha in conteudo.splitlines()
        if linha.strip()
    ]

    busca = st.text_input("Digite o nome do arquivo")

    if busca:
        resultados = []

        for caminho in caminhos:
            nome_arquivo = Path(caminho).name

            if busca.lower() in nome_arquivo.lower():
                resultados.append(caminho)

        st.write(f"Encontrados: {len(resultados)} arquivo(s)")

        for caminho in resultados:
            pasta = str(Path(caminho).parent)
            nome = Path(caminho).name

            st.markdown(f"**Arquivo:** {nome}")
            st.code(caminho)

            pasta_url = "file:///" + quote(pasta.replace("\\", "/"))

            st.markdown(
                f'<a href="{pasta_url}" target="_blank">📂 Abrir pasta</a>',
                unsafe_allow_html=True
            )

            st.divider()
