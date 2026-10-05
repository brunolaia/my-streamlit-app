import streamlit as st
from datetime import datetime
import html
import json

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

    .copy-folder {
        display: inline-block;
        margin-top: 10px;
        padding: 7px 12px;
        background: #1c2230;
        border: 1px solid #2a2f3a;
        border-radius: 8px;
        color: #cfd6e6;
        font-size: 12px;
        cursor: pointer;
        transition: 0.2s;
    }

    .copy-folder:hover {
        background: #2a3244;
        border: 1px solid #3a435a;
        color: #ffffff;
    }

    .copy-success {
        display: none;
        color: #86efac;
        font-size: 12px;
        margin-left: 8px;
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

        # Normaliza o caminho
        caminho_normalizado = caminho.replace(
            "/",
            "\\"
        )

        # Remove barra final
        caminho_normalizado = caminho_normalizado.rstrip("\\")

        # Nome do arquivo
        nome_arquivo = caminho_normalizado.rsplit(
            "\\",
            1
        )[-1]

        # Pasta onde o arquivo está
        if "\\" in caminho_normalizado:

            pasta = caminho_normalizado.rsplit(
                "\\",
                1
            )[0]

        else:

            pasta = caminho_normalizado

        # Escapa para HTML
        caminho_html = html.escape(
            caminho_normalizado,
            quote=True
        )

        nome_html = html.escape(
            nome_arquivo,
            quote=True
        )

        # Converte o caminho para uma string JavaScript segura
        pasta_js = json.dumps(pasta)

        # ID único
        botao_id = f"copiar_pasta_{indice}"

        sucesso_id = f"sucesso_{indice}"

        # =========================
        # CARD DO ARQUIVO
        # =========================

        st.markdown(
            f"""
            <div class="card"
                 title="📁 {caminho_html}">

                <div class="file-text">
                    📄 {nome_html}
                </div>

                <div
                    class="copy-folder"
                    id="{botao_id}"
                    onclick='copiarPasta({pasta_js}, "{sucesso_id}")'>
                    📂 Copiar pasta
                </div>

                <span
                    class="copy-success"
                    id="{sucesso_id}">
                    ✓ Caminho copiado
                </span>

            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# JAVASCRIPT - COPIAR PASTA
# =========================

st.markdown(
    """
    <script>

    function copiarPasta(caminho, sucessoId) {

        navigator.clipboard.writeText(caminho).then(
            function() {

                var mensagem =
                    document.getElementById(sucessoId);

                if (mensagem) {

                    mensagem.style.display = "inline";

                    setTimeout(function() {

                        mensagem.style.display = "none";

                    }, 2500);
                }

            }
        ).catch(
            function() {

                // Método alternativo para navegadores
                // que não permitem Clipboard API

                var campo =
                    document.createElement("textarea");

                campo.value = caminho;

                campo.style.position = "fixed";
                campo.style.left = "-9999px";

                document.body.appendChild(campo);

                campo.focus();
                campo.select();

                document.execCommand("copy");

                document.body.removeChild(campo);

                var mensagem =
                    document.getElementById(sucessoId);

                if (mensagem) {

                    mensagem.style.display = "inline";

                    setTimeout(function() {

                        mensagem.style.display = "none";

                    }, 2500);
                }
            }
        );
    }

    </script>
    """,
    unsafe_allow_html=True
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
