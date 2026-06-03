import streamlit as st

st.set_page_config(
    page_title="Pesquisa de Arquivos A-CEDOC",
    layout="wide"
)

# =========================
# ESTILO GLOBAL (DARK UI)
# =========================
st.markdown(
    """
    <style>

    /* Fundo geral */
    .stApp {
        background-color: #0e0f13;
        color: #e6e6e6;
    }

    /* Inputs */
    input {
        background-color: #151821 !important;
        color: #e6e6e6 !important;
        border-radius: 8px !important;
        border: 1px solid #2a2f3a !important;
    }

    /* Botões */
    .stButton>button {
        background-color: #1c2230;
        color: #e6e6e6;
        border-radius: 8px;
        border: 1px solid #2a2f3a;
        height: 40px;
    }

    .stButton>button:hover {
        background-color: #2a3244;
        border: 1px solid #3a435a;
    }

    /* Cards de resultado */
    .card {
        background: #151821;
        border: 1px solid #2a2f3a;
        padding: 14px 16px;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.35);
        transition: 0.2s;
    }

    .card:hover {
        border: 1px solid #3a435a;
        transform: translateY(-1px);
    }

    .file-text {
        color: #e6e6e6;
        font-size: 14px;
        word-break: break-all;
        line-height: 1.4;
    }

    /* Histórico tags */
    .tag {
        display: inline-block;
        background: #1c2230;
        border: 1px solid #2a2f3a;
        padding: 4px 10px;
        border-radius: 20px;
        margin: 3px;
        font-size: 12px;
        color: #cfd6e6;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# TÍTULO
# =========================
st.title("🔍 Pesquisa de Arquivos A-CEDOC")

# =========================
# SESSION STATE
# =========================
if "historico" not in st.session_state:
    st.session_state.historico = []

if "busca" not in st.session_state:
    st.session_state.busca = ""

# =========================
# UPLOAD
# =========================
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

    # =========================
    # BUSCA
    # =========================
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        busca = st.text_input(
            "Buscar arquivos",
            value=st.session_state.busca,
            placeholder="Digite qualquer termo..."
        )

    with col2:
        pesquisar = st.button("🔎 Pesquisar", use_container_width=True)

    with col3:
        limpar = st.button("🧹 Limpar", use_container_width=True)

    # =========================
    # LIMPAR
    # =========================
    if limpar:
        st.session_state.busca = ""
        st.rerun()

    # =========================
    # PESQUISA
    # =========================
    if pesquisar and busca:
        st.session_state.busca = busca

        if busca not in st.session_state.historico:
            st.session_state.historico.append(busca)

        resultados = [
            c for c in caminhos
            if busca.lower() in c.lower()
        ]

        st.success(f"{len(resultados)} resultado(s) encontrado(s)")

        if not resultados:
            st.warning("Nenhum arquivo encontrado.")

        # =========================
        # RESULTADOS (CARDS DARK)
        # =========================
        for caminho in resultados:
            st.markdown(
                f"""
                <div class="card">
                    <div class="file-text">📄 {caminho}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # =========================
    # HISTÓRICO
    # =========================
    if st.session_state.historico:
        st.markdown("### 🕘 Histórico de buscas")

        colh1, colh2 = st.columns([6, 1])

        with colh2:
            if st.button("🗑️ Limpar histórico"):
                st.session_state.historico = []
                st.rerun()

        st.markdown(
            "".join(
                f"<span class='tag'>{h}</span>"
                for h in st.session_state.historico[::-1][:12]
            ),
            unsafe_allow_html=True
        )

# =========================
# FOOTER
# =========================
st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#6b7280;
        font-size:12px;
        padding-top:10px;
    ">
        Desenvolvido por Bruno Laia
    </div>
    """,
    unsafe_allow_html=True
)
