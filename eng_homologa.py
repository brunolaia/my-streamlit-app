# -*- coding: utf-8 -*-

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

            data_commit = data[0]["commit"]["committer"]["date"]

            return datetime.fromisoformat(
                data_commit.replace("Z", "+00:00")
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

    if st.button(
        "🇧🇷 PT",
        key="pt"
    ):
        st.session_state.lang = "PT"


with col_en:

    if st.button(
        "🇸🇬 EN",
        key="en"
    ):
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
    nome_documento_txt = "Nome do Documento"

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
    tabela_txt = "📋 Detailed Data"
    loading_txt = "📥 Loading database..."
    todos_txt = "ALL"
    status_adp_txt = "✅ ADP Approval Status"
    total_adp_txt = "📊 Total ADPs"
    qtd_label = "Quantity"
    registros_label = "Records"
    sucesso_txt = "✅ Data loaded successfully"
    nenhum_status_txt = "No ADP approval status found."
    nome_documento_txt = "Document Name"

    meses = {
        1: "JANUARY",
        2: "FEBRUARY",
        3: "MARCH",
        4: "APRIL",
        5: "MAY",
        6: "JUNE",
        7: "JULY",
        8: "AUGUST",
        9: "SEPTEMBER",
        10: "OCTOBER",
        11: "NOVEMBER",
        12: "DECEMBER"
    }


# =========================
# TÍTULO
# =========================

st.title(titulo)

st.markdown(
    f"<p style='color:white; font-size:14px;'>{dev}</p>",
    unsafe_allow_html=True
)


# =========================
# LEITURA
# =========================

url = (
    "https://raw.githubusercontent.com/"
    "brunolaia/my-streamlit-app/main/BD_ENG.xlsx"
)

progress_bar = st.progress(0)

with st.spinner(loading_txt):

    for i in range(40):

        time.sleep(0.01)

        progress_bar.progress(i + 1)

    df = pd.read_excel(
        url,
        sheet_name=sheet_excel,
        engine="openpyxl"
    )

    for i in range(40, 100):

        time.sleep(0.005)

        progress_bar.progress(i + 1)

progress_bar.empty()


# =========================
# TRATAMENTO
# =========================

# Estrutura do Excel:
#
# A = Data
# B = Disciplina
# C = Registro
# D = TipoDocumento
# E = StatusADP (somente ADP)
# F = NomeDocumento


if area == "ADP":

    while df.shape[1] < 6:

        df[f"ColunaExtra{df.shape[1] + 1}"] = ""

    df = df.iloc[:, :6]

    df.columns = [
        "Data",
        "Disciplina",
        "Registro",
        "TipoDocumento",
        "StatusADP",
        "NomeDocumento"
    ]

else:

    while df.shape[1] < 6:

        df[f"ColunaExtra{df.shape[1] + 1}"] = ""

    df = df.iloc[:, [0, 1, 2, 3, 5]]

    df.columns = [
        "Data",
        "Disciplina",
        "Registro",
        "TipoDocumento",
        "NomeDocumento"
    ]


df["Data"] = pd.to_datetime(
    df["Data"],
    errors="coerce"
)

df = df.dropna(
    subset=["Data"]
)

df["Ano"] = df["Data"].dt.year

df["MesNum"] = df["Data"].dt.month

df["Dia"] = df["Data"].dt.day

df["Mês"] = df["MesNum"].map(meses)

df["SemanaNum"] = (
    (df["Dia"] - 1) // 7 + 1
)

df["Semana"] = (
    "SEMANA "
    if lang == "PT"
    else "WEEK "
) + df["SemanaNum"].astype(str)


# =========================
# DATA DO EXCEL
# =========================

file_date = get_github_file_date()

if file_date:

    if lang == "PT":

        data_formatada = file_date.strftime(
            "%d/%m/%Y"
        )

    else:

        data_formatada = file_date.strftime(
            "%m/%d/%Y"
        )

    st.success(
        f"{sucesso_txt} - {data_formatada}"
    )

else:

    st.success(
        sucesso_txt
    )


# =========================
# FILTROS
# =========================

st.sidebar.subheader(
    filtros_txt
)

lista_disciplina = [
    todos_txt
] + sorted(
    df["Disciplina"]
    .dropna()
    .unique()
)

lista_tipo = [
    todos_txt
] + sorted(
    df["TipoDocumento"]
    .dropna()
    .unique()
)

lista_ano = [
    todos_txt
] + sorted(
    df["Ano"]
    .dropna()
    .unique()
)

disciplina = st.sidebar.selectbox(
    f"📂 {disciplina_txt}",
    lista_disciplina
)

tipo_doc = st.sidebar.selectbox(
    f"📄 {tipo_txt}",
    lista_tipo
)

ano = st.sidebar.selectbox(
    f"📅 {ano_txt}",
    lista_ano
)


# =========================
# FILTRO
# =========================

df_filtro = df.copy()

if disciplina != todos_txt:

    df_filtro = df_filtro[
        df_filtro["Disciplina"] == disciplina
    ]

if tipo_doc != todos_txt:

    df_filtro = df_filtro[
        df_filtro["TipoDocumento"] == tipo_doc
    ]

if ano != todos_txt:

    df_filtro = df_filtro[
        df_filtro["Ano"] == ano
    ]


# =========================
# RESUMO
# =========================

st.subheader(
    resumo_txt
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    total_txt,
    len(df_filtro)
)

col2.metric(
    disciplinas_txt,
    disciplina
)

col3.metric(
    tipos_txt,
    tipo_doc
)

col4.metric(
    ano_txt,
    ano
)


# =========================
# GRÁFICO DE PIZZA - TOTAL DE ADPs
# =========================

if (
    area == "ADP"
    and "StatusADP" in df_filtro.columns
):

    st.subheader(
        total_adp_txt
    )

    df_status_total = df_filtro.copy()

    if lang == "PT":

        status_map_total = {
            "APROVADO": "APROVADO",
            "NÃO APROVADO": "NÃO APROVADO",
            "NAO APROVADO": "NÃO APROVADO",
            "APR. C/ RNC": "APROVADO COM RNC",
            "APROVADO C/ RNC": "APROVADO COM RNC",
            "APROVADO COM RNC": "APROVADO COM RNC"
        }

        ordem_status_total = [
            "APROVADO",
            "NÃO APROVADO",
            "APROVADO COM RNC"
        ]

    else:

        status_map_total = {
            "APPROVED": "APPROVED",
            "NOT APPROVED": "NOT APPROVED",
            "APPROVED W/ RNC": "APPROVED W/ RNC",
            "APPROVED WITH RNC": "APPROVED W/ RNC",
            "APPROVED C/ RNC": "APPROVED W/ RNC",
            "APR. C/ RNC": "APPROVED W/ RNC",
            "APROVADO": "APPROVED",
            "NÃO APROVADO": "NOT APPROVED",
            "NAO APROVADO": "NOT APPROVED",
            "APROVADO C/ RNC": "APPROVED W/ RNC",
            "APROVADO COM RNC": "APPROVED W/ RNC"
        }

        ordem_status_total = [
            "APPROVED",
            "NOT APPROVED",
            "APPROVED W/ RNC"
        ]

    df_status_total["StatusGrafico"] = (
        df_status_total["StatusADP"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
        .map(status_map_total)
    )

    df_status_total = df_status_total.dropna(
        subset=["StatusGrafico"]
    )

    if not df_status_total.empty:

        pizza_adp_df = (
            df_status_total
            .groupby("StatusGrafico")
            .agg(
                Quantidade=("Registro", "count"),
                Registros=(
                    "Registro",
                    lambda x: "<br>".join(
                        map(str, x.dropna())
                    )
                )
            )
            .reset_index()
        )

        pizza_adp_df["StatusGrafico"] = pd.Categorical(
            pizza_adp_df["StatusGrafico"],
            categories=ordem_status_total,
            ordered=True
        )

        pizza_adp_df = pizza_adp_df.sort_values(
            "StatusGrafico"
        )

        fig_pizza_adp = px.pie(
            pizza_adp_df,
            names="StatusGrafico",
            values="Quantidade",
            custom_data=["Registros"],
            hole=0
        )

        fig_pizza_adp.update_traces(
            textinfo="label+value+percent",
            textposition="inside",
            hovertemplate=(
                "<b>%{label}</b><br>"
                f"{qtd_label}: "
                "%{value}<br>"
