import streamlit as st

st.set_page_config(
    page_title="Localizador de Arquivos",
    layout="wide"
)

st.title("🔍 Pesquisa de Arquivos A-CEDOC")

arquivo_txt = st.file_uploader(
    "Selecione o banco de dados (.txt) - Rev.2 - Desenvolvido por Bruno Laia",
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

        for caminho in resultados:

            caminho = caminho.strip()

            # Nome do arquivo
            nome_arquivo = caminho.split("\\")[-1]

            # Pasta (remove o arquivo do final)
            pasta = caminho.rsplit("\\", 1)[0]

            # Link para a pasta de rede
            pasta_url = "file:///" + pasta.replace("\\", "/")

            col1, col2 = st.columns([9, 1])

            with col1:
                st.write(nome_arquivo)

            with col2:
                st.markdown(
                    f'<a href="{pasta_url}" target="_blank">📂 Abrir Pasta</a>',
                    unsafe_allow_html=True
                )
