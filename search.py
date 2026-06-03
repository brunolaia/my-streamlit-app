import streamlit as st

st.set_page_config(
    page_title="Pesquisa de Arquivos A-CEDOC - Rev. Final",
    layout="wide"
)

st.title("🔍 Pesquisa de Arquivos A-CEDOC")

# -------------------------
# SESSION STATE
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

caminhos = []

if arquivo_txt:
    conteudo = arquivo_txt.read().decode("utf-8", errors="ignore")

    caminhos = [
        linha.strip()
        for linha in conteudo.splitlines()
        if linha.strip()
    ]

    # -------------------------
    # BUSCA + BOTÕES
    # -------------------------
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        busca = st.text_input(
            "Digite qualquer termo (arquivo, pasta, caminho...)",
            value=st.session_state.busca,
            placeholder="Ex: contrato, 2024, financeiro..."
        )

    with col2:
        pesquisar = st.button("🔎 Pesquisar", use_container_width=True)

    with col3:
        limpar_busca = st.button("🧹 Limpar busca", use_container_width=True)

    col4, col5 = st.columns([1, 1])

    with col4:
        limpar_hist = st.button("🗑️ Limpar histórico", use_container_width=True)

    # -------------------------
    # LIMPAR BUSCA
    # -------------------------
    if limpar_busca:
        st.session_state.busca = ""
        st.rerun()

    # -------------------------
    # LIMPAR HISTÓRICO
    # -------------------------
    if limpar_hist:
        st.session_state.historico = []
        st.rerun()

    # -------------------------
    # PESQUISA
    # -------------------------
    if pesquisar and busca:
        st.session_state.busca = busca

        if busca not in st.session_state.historico:
            st.session_state.historico.append(busca)

        resultados = [
            caminho for caminho in caminhos
            if busca.lower() in caminho.lower()
        ]

        st.success(f"{len(resultados)} resultado(s) encontrado(s)")

        if not resultados:
            st.warning("Nenhum arquivo encontrado.")

        # -------------------------
        # RESULTADOS (CARDS DARK)
        # -------------------------
        for caminho in resultados:

            st.markdown(
                f"""
                <div style="
                    background: #111318;
                    border: 1px solid #2a2f3a;
                    border-radius: 10px;
                    padding: 14px 16px;
                    margin-bottom: 10px;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.25);
                ">
                    <div style="
                        color: #E6E6E6;
                        font-size: 14px;
                        font-family: 'Segoe UI', sans-serif;
                        word-break: break-all;
                        line-height: 1.4;
                    ">
                        📄 {caminho}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # -------------------------
        # HISTÓRICO
        # -------------------------
        if st.session_state.historico:
            st.markdown("### 🕘 Histórico de buscas")

            st.markdown(
                "<div style='color:#aaa; font-size:13px;'>"
                + " • ".join(st.session_state.historico[::-1][:10]) +
                "</div>",
                unsafe_allow_html=True
            )

# -------------------------
# FOOTER
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
