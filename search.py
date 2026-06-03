import streamlit as st

st.set_page_config(
    page_title="Pesquisa de Arquivos A-CEDOC - Rev. 5",
    layout="wide"
)

st.title("🔍 Pesquisa de Arquivos A-CEDOC")

# -------------------------
# HISTÓRICO DE BUSCAS
# -------------------------
if "historico" not in st.session_state:
    st.session_state.historico = []

if "busca" not in st.session_state:
    st.session_state.busca = ""

# -------------------------
# UPLOAD
# -------------------------
arquivo_txt = st.file_uploader(
    "Selecione o banco de dados (.txt)",
    type=["txt"]
)

# -------------------------
# PROCESSA ARQUIVO
# -------------------------
caminhos = []

if arquivo_txt:
    conteudo = arquivo_txt.read().decode("utf-8", errors="ignore")

    caminhos = [
        linha.strip()
        for linha in conteudo.splitlines()
        if linha.strip()
    ]

    # -------------------------
    # BUSCA
    # -------------------------
    col1, col2 = st.columns([3, 1])

    with col1:
        busca = st.text_input(
            "Digite qualquer termo (caminho, pasta, arquivo, etc.)",
            value=st.session_state.busca,
            placeholder="Ex: relatorio, 2024, financeiro..."
        )

    with col2:
        pesquisar = st.button("🔎 Pesquisar", use_container_width=True)
        limpar = st.button("🧹 Limpar", use_container_width=True)

    # -------------------------
    # LIMPAR
    # -------------------------
    if limpar:
        st.session_state.busca = ""
        st.rerun()

    # -------------------------
    # PESQUISAR
    # -------------------------
    if pesquisar and busca:
        st.session_state.busca = busca

        st.session_state.historico.append(busca)

        resultados = [
            caminho for caminho in caminhos
            if busca.lower() in caminho.lower()
        ]

        st.success(f"{len(resultados)} resultado(s) encontrado(s)")

        if not resultados:
            st.warning("Nenhum arquivo encontrado.")

        # -------------------------
        # RESULTADOS (CARDS)
        # -------------------------
        for caminho in resultados:

            partes = caminho.split("\\")
            nome_arquivo = partes[-1]
            pasta = "\\".join(partes[:-1])

            with st.container():

                st.markdown(
                    f"""
                    <div style="
                        background-color:#f9f9f9;
                        padding:12px;
                        border-radius:10px;
                        border:1px solid #e6e6e6;
                        margin-bottom:10px;
                    ">
                        <div style="
                            font-size:15px;
                            font-weight:700;
                            margin-bottom:6px;
                        ">
                            📄 {nome_arquivo}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                colA, colB = st.columns([4, 1])

                with colA:
                    st.text_input(
                        "Caminho completo",
                        value=caminho,
                        key=f"full_{hash(caminho)}"
                    )

                with colB:
                    st.text_input(
                        "Pasta",
                        value=pasta,
                        key=f"pasta_{hash(caminho)}"
                    )

        # -------------------------
        # HISTÓRICO
        # -------------------------
        if st.session_state.historico:
            st.markdown("### 🕘 Histórico de buscas")

            st.write(
                " • ".join(
                    list(dict.fromkeys(st.session_state.historico[::-1]))[:10]
                )
            )

# -------------------------
# RODAPÉ
# -------------------------
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
