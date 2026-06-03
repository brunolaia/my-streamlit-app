import streamlit as st
from pathlib import Path
from urllib.parse import quote

st.set_page_config(
    page_title="Localizador de Arquivos",
    layout="wide"
)

st.title("🔍 Pesquisa de Arquivos ACEDOC")

arquivo_txt = st.file_uploader(
    "Selecione o banco de dados (.txt) - Rev.1 - Desenvolvido por Bruno Laia",
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

        st.success(f"Encontrados: {len(resultados)} arquivo(s)")

        for caminho in resultados:
            path_obj = Path(caminho)

            # Nome do arquivo (última parte do caminho)
            nome_arquivo = path_obj.name

            # Pasta onde o arquivo está localizado
            pasta = str(path_obj.parent)

            # Link para abrir a pasta da rede
            pasta_url = "file:///" + quote(
                pasta.replace("\\", "/"),
                safe="/:"
            )

            st.markdown(
                f"""
                <div style="
                    display:flex;
                    align-items:center;
                    justify-content:space-between;
                    padding:8px;
                    border-bottom:1px solid #ddd;
                ">
                    <span>{nome_arquivo}</span>

                    <a href="{pasta_url}" target="_blank">
                        📂 Abrir Pasta
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )
