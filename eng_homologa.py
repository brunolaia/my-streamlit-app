import streamlit as st
import pandas as pd
import plotly.express as px
import time
import requests
from datetime import datetime

# =========================
# CONFIGURACAO
# =========================
st.set_page_config(
    page_title="Dashboard Engenharia - CEDOC",
    layout="wide"
)

# =========================
# AJUSTE MENU LATERAL
# =========================
st.markdown(
    """
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
    """,
    unsafe_allow_html=True
)

# =========================
# CONTROLE DE IDIOMA
# =========================
if "lang" not in st.session_state:
    st.session_state.lang = "PT"

# =========================
# FUNCAO DATA GITHUB
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
        resposta = requests.get(
            api_url,
            headers=headers,
            timeout=15
        )

        resposta.raise_for_status()
        dados = resposta.json()

        if dados:
            data_commit = dados[0]["commit"]["committer"]["date"]

            return datetime.fromisoformat(
                data_commit.replace("Z", "+00:00")
            )

    except Exception as erro:
        print("Erro ao consultar o GitHub:", erro)

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
# MENU AREA
# =========================
if lang == "PT":
    area = st.sidebar.selectbox(
        "📁 TIPO DOCUMENTO",
        ["ENGENHARIA", "ADP", "MTO", "TPS"]
    )
else:
    area = st.sidebar.selectbox(
        "📁 DOCUMENT TYPE",
        ["ENGINEERING", "ADP", "MTO", "TPS"]
    )

# =========================
# DEFINIR PLANILHA
# =========================
if lang == "PT":
    mapa_planilhas = {
        "ENGENHARIA": "Planilha1",
        "ADP": "ADP_PT",
        "MTO": "MTO_PT",
        "TPS": "TPS_PT"
    }
else:
    mapa_planilhas = {
        "ENGINEERING": "Planilha2",
        "ADP": "ADP_EN",
        "MTO": "MTO_EN",
        "TPS": "TPS_EN"
    }

sheet_excel = mapa_planilhas[area]

# =========================
# TEXTOS DINAMICOS
# =========================
if lang == "PT":
    titulos = {
        "ENGENHARIA": "📊 Dashboard - Engenharia NPO",
        "ADP": "📊 Dashboard - ADP",
        "MTO": "📊 Dashboard - MTO",
        "TPS": "📊 Dashboard - TPS"
    }

    titulo = titulos[area]
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
    percentual_txt = "Percentual"

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
    titulos = {
        "ENGINEERING": "📊 Engineering Dashboard",
        "ADP": "📊 ADP Dashboard",
        "MTO": "📊 MTO Dashboard",
        "TPS": "📊 TPS Dashboard"
    }

    titulo = titulos[area]
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
    percentual_txt = "Percentage"

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
# TITULO
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

try:
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

except Exception as erro:
    progress_bar.empty()
    st.error(
        f"Erro ao carregar a planilha '{sheet_excel}': {erro}"
    )
    st.stop()

progress_bar.empty()

# =========================
# TRATAMENTO
# =========================

# Garante que existam pelo menos seis colunas, de A ate F
while df.shape[1] < 6:
    df[f"ColunaExtra{df.shape[1] + 1}"] = ""

if area == "ADP":
    # Coluna A = Data
    # Coluna B = Disciplina
    # Coluna C = Registro
    # Coluna D = Tipo de documento
    # Coluna E = Status da ADP
    # Coluna F = Nome do documento
    df = df.iloc[:, [0, 1, 2, 3, 4, 5]].copy()

    df.columns = [
        "Data",
        "Disciplina",
        "Registro",
        "TipoDocumento",
        "StatusADP",
        "NomeDocumento"
    ]

else:
    # Coluna A = Data
    # Coluna B = Disciplina
    # Coluna C = Registro
    # Coluna D = Tipo de documento
    # Coluna E = Ignorada
    # Coluna F = Nome do documento
    df = df.iloc[:, [0, 1, 2, 3, 5]].copy()

    df.columns = [
        "Data",
        "Disciplina",
        "Registro",
        "TipoDocumento",
        "NomeDocumento"
    ]

# Remove espacos dos nomes das colunas
df.columns = df.columns.astype(str).str.strip()

# Limpa as colunas de texto
colunas_texto = [
    "Disciplina",
    "Registro",
    "TipoDocumento",
    "NomeDocumento"
]

if "StatusADP" in df.columns:
    colunas_texto.append("StatusADP")

for coluna in colunas_texto:
    df[coluna] = (
        df[coluna]
        .fillna("")
        .astype(str)
        .str.strip()
    )

# Converte a coluna de data
df["Data"] = pd.to_datetime(
    df["Data"],
    errors="coerce",
    dayfirst=True
)

# Remove linhas sem data valida
df = df.dropna(subset=["Data"]).copy()

# =========================
# COLUNAS AUXILIARES
# =========================
df["Ano"] = df["Data"].dt.year.astype("Int64")
df["MesNum"] = df["Data"].dt.month.astype("Int64")
df["Dia"] = df["Data"].dt.day.astype("Int64")
df["Mês"] = df["MesNum"].map(meses)

df["SemanaNum"] = (
    ((df["Dia"] - 1) // 7) + 1
).astype("Int64")

if lang == "PT":
    df["Semana"] = (
        "SEMANA " + df["SemanaNum"].astype(str)
    )
else:
    df["Semana"] = (
        "WEEK " + df["SemanaNum"].astype(str)
    )

# =========================
# DATA DO EXCEL
# =========================
file_date = get_github_file_date()

if file_date:
    if lang == "PT":
        data_formatada = file_date.strftime("%d/%m/%Y")
    else:
        data_formatada = file_date.strftime("%m/%d/%Y")

    st.success(
        f"{sucesso_txt} - {data_formatada}"
    )
else:
    st.success(sucesso_txt)

# =========================
# FILTROS
# =========================
st.sidebar.subheader(filtros_txt)

lista_disciplina = [todos_txt] + sorted(
    [
        valor
        for valor in df["Disciplina"].unique().tolist()
        if valor
    ]
)

lista_tipo = [todos_txt] + sorted(
    [
        valor
        for valor in df["TipoDocumento"].unique().tolist()
        if valor
    ]
)

lista_ano = [todos_txt] + sorted(
    df["Ano"]
    .dropna()
    .astype(int)
    .unique()
    .tolist()
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
# APLICACAO DOS FILTROS
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
        df_filtro["Ano"] == int(ano)
    ]

# =========================
# RESUMO
# =========================
st.subheader(resumo_txt)

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
# STATUS ADP
# =========================
if lang == "PT":
    status_map = {
        "APROVADO": "APROVADO",
        "NÃO APROVADO": "NÃO APROVADO",
        "NAO APROVADO": "NÃO APROVADO",
        "APR. C/ RNC": "APROVADO COM RNC",
        "APROVADO C/ RNC": "APROVADO COM RNC",
        "APROVADO COM RNC": "APROVADO COM RNC"
    }

    ordem_status = [
        "APROVADO",
        "NÃO APROVADO",
        "APROVADO COM RNC"
    ]

else:
    status_map = {
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

    ordem_status = [
        "APPROVED",
        "NOT APPROVED",
        "APPROVED W/ RNC"
    ]

# =========================
# GRAFICO DE PIZZA - TOTAL ADP
# =========================
if area == "ADP" and "StatusADP" in df_filtro.columns:
    st.subheader(total_adp_txt)

    df_status_total = df_filtro.copy()

    df_status_total["StatusGrafico"] = (
        df_status_total["StatusADP"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
        .map(status_map)
    )

    df_status_total = df_status_total.dropna(
        subset=["StatusGrafico"]
    )

    if not df_status_total.empty:
        pizza_adp_df = (
            df_status_total
            .groupby(
                "StatusGrafico",
                observed=True
            )
            .agg(
                Quantidade=("Registro", "count"),
                Registros=(
                    "Registro",
                    lambda valores: "<br>".join(
                        map(
                            str,
                            valores[
                                valores.astype(str).str.strip() != ""
                            ]
                        )
                    )
                )
            )
            .reset_index()
        )

        pizza_adp_df["StatusGrafico"] = pd.Categorical(
            pizza_adp_df["StatusGrafico"],
            categories=ordem_status,
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
                f"{qtd_label}: %{{value}}<br>"
                f"{percentual_txt}: %{{percent}}<br><br>"
                f"<b>{registros_label}:</b><br>"
                "%{customdata[0]}"
                "<extra></extra>"
            ),
            hoverlabel=dict(
                align="left"
            )
        )

        fig_pizza_adp.update_layout(
            height=450,
            showlegend=True,
            legend_title_text="Status",
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            )
        )

        st.plotly_chart(
            fig_pizza_adp,
            use_container_width=True,
            key=f"pizza_total_adp_{lang}"
        )

    else:
        st.info(nenhum_status_txt)

# =========================
# STATUS DE APROVACAO ADP
# =========================
if area == "ADP" and "StatusADP" in df_filtro.columns:
    st.subheader(status_adp_txt)

    df_status = df_filtro.copy()

    df_status["StatusADP"] = (
        df_status["StatusADP"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
        .map(status_map)
    )

    df_status = df_status.dropna(
        subset=["StatusADP"]
    )

    if not df_status.empty:
        ordem_meses = list(meses.values())

        meses_com_status = [
            mes
            for mes in ordem_meses
            if not df_status[
                df_status["Mês"] == mes
            ].empty
        ]

       
