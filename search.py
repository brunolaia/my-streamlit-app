import streamlit as st

st.set_page_config(
    page_title="Pesquisa de Arquivos A-CEDOC - Rev. 4",
    layout="wide"
)

st.title("🔍 Pesquisa de Arquivos A-CEDOC")

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
            f"{len(resultados)} arquivo(s) encontrado(s)"
        )

        if not resultados:
            st.warning(
                "Nenhum arquivo encontrado."
            )

        for caminho in resultados:

            nome_arquivo = caminho.split("\\")[-1]

            pasta = caminho.rsplit("\\", 1)[0]

            st.markdown(
                f"""
                <div style="
                    padding-top:6px;
                    padding-bottom:6px;
                ">
                    <div style="
                        font-size:14px;
                        font-weight:600;
                        margin-bottom:6px;
                    ">
                        📄 {nome_arquivo}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.text_input(
                "Caminho da pasta",
                value=pasta,
                key=f"pasta_{hash(caminho)}",
                disabled=False
            )

            st.markdown(
                """
                <hr style="
                    margin-top:10px;
                    margin-bottom:10px;
                    border:0;
                    border-top:1px solid #d9d9d9;
                ">
                """,
                unsafe_allow_html=True
            )

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#808080;
        font-size:12px;
        padding-top:10px;
    ">
        Desenvolvido por Bruno Laia
    </div>
    """,
    unsafe_allow_html=True
)
