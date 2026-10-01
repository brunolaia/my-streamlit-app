import streamlit as st
import pandas as pd
import plotly.express as px
import time
import requests
from datetime import datetime

# =========================
# CONFIGURAÇÃO
# =========================
st.set_page_config(
    page_title="Dashboard Engenharia - CEDOC",
    layout="wide"
)

# =========================
# AJUSTE MENU LATERAL
# =========================
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    overflow-y: auto;
}

section[data-testid="stSidebar"] label {
    font-size: 13px !important;
}

section[data-testid="stSidebar"] .stSelectbox {
    margin-bottom: -8px;
}

section[data-testid="stSidebar"] .stRadio {
    margin-bottom: -8px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# CONTROLE DE IDIOMA
# =========================
if "lang" not in st.session_state:
    st.session_state.lang = "PT"


# =========================
# FUNÇÃO DATA GITHUB
# =========================
def get_github_file_date():

    api_url = (
        "https://api.github.com/repos/"
        "brunolaia/my-streamlit-app/commits"
        "?path=BD_ENG.xlsx&per_page=1"
    )

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Streamlit-Dashboard"
    }

    try:
        r = requests.get(
            api_url,
            headers=headers,
            timeout=15
        )

        r.raise_for_status()

        data = r.json()

        if len(data) > 0:

            data_commit = (
                data[0]["commit"]["committer"]["date"]
            )

            return datetime.fromisoformat(
                data_commit.replace(
                    "Z",
                    "+00:00"
                )
            )

    except Exception as erro:
        print("Erro GitHub:", erro)

    return None


# =========================
# MENU LATERAL
# =========================
st.sidebar.header("MENU")

col_pt, col_en = st.sidebar.columns(2)

with col_pt:
    if st.button("🇧🇷 PT", key="pt"):
        st.session_state.lang = "PT"

with col_en:
    if st.button("🇸🇬 EN", key="en"):
        st.session_state.lang = "EN"

lang = st.session_state.lang


# =========================
# MENU ÁREA
# =========================
if lang == "PT":

    area = st.sidebar.selectbox(
        "📁 TIPO DOCUMENTO",
        [
            "ENGENHARIA",
            "ADP",
            "MTO",
            "TPS"
        ]
    )

else:

    area = st.sidebar.selectbox(
        "📁 DOCUMENT TYPE",
        [
            "ENGINEERING",
            "ADP",
            "MTO",
            "TPS"
        ]
    )


# =========================
# DEFINIR PLANILHA
# =========================
if lang == "PT":

    if area == "ENGENHARIA":
        sheet_excel = "Planilha1"

    elif area == "ADP":
        sheet_excel = "ADP_PT"

    elif area == "MTO":
        sheet_excel = "MTO_PT"

    elif area == "TPS":
        sheet_excel = "TPS_PT"

else:

    if area == "ENGINEERING":
        sheet_excel = "Planilha2"

    elif area == "ADP":
        sheet_excel = "ADP_EN"

    elif area == "MTO":
        sheet_excel = "MTO_EN"

    elif area == "TPS":
        sheet_excel = "TPS_EN"


# =========================
# TEXTOS DINÂMICOS
# =========================
if lang == "PT":

    if area == "ENGENHARIA":
        titulo = "📊 Dashboard - Engenharia NPO"

    elif area == "ADP":
        titulo = "📊 Dashboard - ADP"

    elif area == "MTO":
        titulo = "📊 Dashboard - MTO"

    elif area == "TPS":
        titulo = "📊 Dashboard - TPS"

    dev = "Desenvolvido por Bruno Laia"
    filtros_txt = "Filtros"
    disciplina_txt = "Disciplina"
    ano_txt = "Ano"
    tipo_txt = "Tipo de Documento"
    resumo_txt = "📈 Resumo"
    total_txt = "Total"
    disciplinas_txt = "Disciplinas"
    tipos_txt = "Tipos"
    grafico_txt = "📊 Registros por Mês e Semana"
    tabela_txt = "📋 Dados detalhados"
    loading_txt = "📥 Carregando base de dados..."
    todos_txt = "TODOS"
    status_adp_txt = "✅ Status de aprovação da ADP"
    total_adp_txt = "📊 Total de ADPs"
    qtd_label = "Quantidade"
    registros_label = "Registros"
    sucesso_txt = "✅ Dados carregados com sucesso"
    nenhum_status_txt = "Nenhum status encontrado para ADP."

    meses = {
        1: "JANEIRO",
        2: "FEVEREIRO",
        3: "MARÇO",
        4: "ABRIL",
        5: "MAIO",
        6: "JUNHO",
        7: "JULHO",
        8: "AGOSTO",
        9: "SETEMBRO",
        10: "OUTUBRO",
        11: "NOVEMBRO",
        12: "DEZEMBRO"
    }

else:

    if area == "ENGINEERING":
        titulo = "📊 Engineering Dashboard"

    elif area == "ADP":
        titulo = "📊 ADP Dashboard"

    elif area == "MTO":
        titulo = "📊 MTO Dashboard"

    elif area == "TPS":
        titulo = "📊 TPS Dashboard"

    dev = "Developed by Bruno Laia"
    filtros_txt = "Filters"
    disciplina_txt = "Discipline"
    ano_txt = "Year"
    tipo_txt = "Document Type"
    resumo_txt = "📈 Summary"
    total_txt = "Total"
    disciplinas_txt = "Disciplines"
    tipos_txt = "Types"
    grafico_txt = "📊 Records by Month and Week"
    tabela_txt 
