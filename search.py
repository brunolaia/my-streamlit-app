import streamlit as st
from datetime import datetime
import os
import platform
import subprocess
import html

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
# UPLOAD TXT
# =========================

arquivo_txt = st.file_uploader(
    "Selecione o arquivo .txt",
    type=["txt"]
)

caminhos = []

if arquivo_txt:

    with st.spinner("🔄 Carregando base de dados..."):

        try:

            conteudo = arquivo_txt.read().decode(
                "utf-8",
                errors="ignore"
            )

            caminhos = [
                linha.strip()
                for linha in conteudo.splitlines()
                if linha.strip()
            ]

            # Data/hora em que o TXT foi carregado
            data_atualizacao = datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            )

            st.markdown(
                f"📅 Atualizado em: **{data_atualizacao}**"
            )

        except Exception:
            st.error(
                "Erro ao carregar arquivo TXT"
            )

            st.stop()

# =========================
# FUNÇÃO PARA ABRIR PASTA
# =========================

def abrir_pasta_explorer(caminho):

    try:

        # Remove aspas extras
        caminho = caminho.strip().strip('"')

        # Normaliza barras
        caminho = caminho.replace("/", "\\")

        # Se o caminho aponta para um arquivo existente
        if os.path.isfile(caminho):

            pasta = os.path.dirname(caminho)

        else:

            # Para caminhos que não podem ser validados
            # localmente, considera tudo antes do último "\"
            if "\\" in caminho:

                pasta = caminho.rsplit("\\", 1)[0]

            else:

                pasta = caminho

        # Verifica se está no Windows
        if platform.system() != "Windows":

            return False

        # Abre o Windows Explorer
        subprocess.Popen(
            ["explorer.exe", pasta],
            shell=False
        )

        return True

    except Exception:

        return False


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

    pesquisar = st.button(
        "🔎 Pesquisar",
        use_container_width=True
    )

with col3:

    limpar = st.button(
        "🧹 Limpar",
        use_container_width=True
    )

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

        st.session_state.historico.append(
            busca
        )

# =========================
# RESULTADOS
# =========================

if st.session_state.busca:

    busca_atual = st.session_state.busca

    resultados = [
        c
        for c in caminhos
        if busca_atual.lower() in c.lower()
    ]

    st.success(
        f"{len(resultados)} resultado(s) encontrado(s)"
    )

    if not resultados:

        st.warning(
            "Nenhum arquivo encontrado."
        )

    # =========================
    # RESULTADOS
    # =========================

    for indice, caminho in enumerate(resultados):

        # Nome do arquivo
        caminho_normalizado = caminho.replace(
            "/",
            "\\"
        )

        nome_arquivo = (
            caminho_normalizado
            .rstrip("\\")
            .rsplit("\\", 1)[-1]
        )

        caminho_html = html.escape(
            caminho,
            quote=True
        )

        nome_html = html.escape(
            nome_arquivo,
            quote=True
        )

        # =========================
        # CARD
        # =========================

        st.markdown(
            f"""
            <div class="card"
                 title="📁 {caminho_html}">
                <div class="file-text">
                    📄 {nome_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # =========================
        # BOTÃO ABRIR PASTA
        # =========================

        if st.button(
            "📂 Abrir pasta",
            key=f"abrir_pasta_{indice}",
            use_container_width=False
        ):

            sucesso = abrir_pasta_explorer(
                caminho
            )

            if sucesso:

                st.success(
                    "📂 Pasta aberta no Windows Explorer."
                )

            else:

                st.warning(
                    "⚠️ O Windows Explorer só pode ser "
                    "aberto diretamente quando o Streamlit "
                    "está sendo executado no Windows."
                )

# =========================
# HISTÓRICO
# =========================

if st.session_state.historico:

    st.markdown(
        "### 🕘 Histórico de buscas"
    )

    colh1, colh2 = st.columns([6, 1])

    with colh2:

        if st.button(
            "🗑️ Limpar histórico"
        ):

            st.session_state.historico = []

            st.rerun()

    st.markdown(
        "".join(
            f"<span class='tag'>{html.escape(h)}</span>"
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
