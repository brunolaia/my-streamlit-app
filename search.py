import streamlit as st
from datetime import datetime
import requests
import pandas as pd
from io import BytesIO

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

    .stApp {
        background-color: #0e0f13;
        color: #e6e6e6;
    }

    input {
        background-color: #151821 !important;
        color: #e6e6e6 !important;
        border-radius: 8px !important;
        border: 1px solid #2a2f3a !important;
    }

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

    .card {
        background: #151821;
        border: 1px solid #2a2f3a;
        padding: 14px 16px;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.35);
        transition: 0.2s;
        cursor: pointer;
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
# GITHUB EXCEL
# =========================
GITHUB_XLSX_URL = "https://raw.githubusercontent.com/brunolaia/my-streamlit-app/main/A-CEDOC_BD.xlsx"

caminhos = []

with st.spinner("🔄 Carregando base de dados..."):
    try:
        response = requests.get(GITHUB_XLSX_URL)
        response.raise_for_status()

        df = pd.read_excel(BytesIO(response.content), engine="openpyxl")

        # 👉 CONVERTE TODAS AS COLUNAS EM LISTA (ignora vazios)
        caminhos = df.astype(str).stack().tolist()
        caminhos = [c.strip() for c in caminhos if c.strip() and c != "nan"]

        data_atualizacao = datetime.now().strftime("%d/%m/%Y %H:%M")
        st.markdown(f"**📅 Atualizado em: {data_atualizacao}**")

    except Exception as e:
        st.error("Erro ao carregar arquivo do GitHub")
        st.stop()

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
    # RESULTADOS
    # =========================
    for caminho in resultados:
        nome_arquivo = caminho.split("\\")[-1]

        st.markdown(
            f"""
            <div class="card"
                title="📁 {caminho}"
                onclick="navigator.clipboard.writeText('{caminho}')">

                <div class="file-text">📄 {nome_arquivo}</div>

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
