import streamlit as st
import pandas as pd
import plotly.express as px
import time
import requests
from datetime import datetime

# =========================
# CONFIGURAÇÃO
# =========================
st.set_page_config(page_title="Dashboard Engenharia - CEDOC", layout="wide")

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
        r = requests.get(api_url, headers=headers, timeout=15)
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
    tabela_txt = "📋 Detailed Data"
    loading_txt = "📥 Loading database..."
    todos_txt = "ALL"
    status_adp_txt = "✅ ADP Approval Status"
    total_adp_txt = "📊 Total ADPs"
    qtd_label = "Quantity"
    registros_label = "Records"
    sucesso_txt = "✅ Data loaded successfully"
    nenhum_status_txt = "No ADP approval status found."

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
st.markdown(f"<p style='color:white; font-size:14px;'>{dev}</p>", unsafe_allow_html=True)

# =========================
# LEITURA
# =========================
url = "https://raw.githubusercontent.com/brunolaia/my-streamlit-app/main/BD_ENG.xlsx"

progress_bar = st.progress(0)

with st.spinner(loading_txt):

    for i in range(40):
        time.sleep(0.01)
        progress_bar.progress(i + 1)

    df = pd.read_excel(url, sheet_name=sheet_excel, engine="openpyxl")

    for i in range(40, 100):
        time.sleep(0.005)
        progress_bar.progress(i + 1)

progress_bar.empty()

# =========================
# TRATAMENTO
# =========================
if area == "ADP":

    while df.shape[1] < 5:
        df[f"ColunaExtra{df.shape[1] + 1}"] = ""

    df = df.iloc[:, :5]
    df.columns = ["Data", "Disciplina", "Registro", "TipoDocumento", "StatusADP"]

else:
    df = df.iloc[:, :4]
    df.columns = ["Data", "Disciplina", "Registro", "TipoDocumento"]

df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
df = df.dropna(subset=["Data"])

df["Ano"] = df["Data"].dt.year
df["MesNum"] = df["Data"].dt.month
df["Dia"] = df["Data"].dt.day
df["Mês"] = df["MesNum"].map(meses)

df["SemanaNum"] = ((df["Dia"] - 1) // 7 + 1)
df["Semana"] = ("SEMANA " if lang == "PT" else "WEEK ") + df["SemanaNum"].astype(str)

# =========================
# DATA DO EXCEL
# =========================
file_date = get_github_file_date()

if file_date:

    if lang == "PT":
        data_formatada = file_date.strftime("%d/%m/%Y")
    else:
        data_formatada = file_date.strftime("%m/%d/%Y")

    st.success(f"{sucesso_txt} - {data_formatada}")

else:
    st.success(sucesso_txt)

# =========================
# FILTROS
# =========================
st.sidebar.subheader(filtros_txt)

lista_disciplina = [todos_txt] + sorted(df["Disciplina"].dropna().unique())
lista_tipo = [todos_txt] + sorted(df["TipoDocumento"].dropna().unique())
lista_ano = [todos_txt] + sorted(df["Ano"].dropna().unique())

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
    df_filtro = df_filtro[df_filtro["Disciplina"] == disciplina]

if tipo_doc != todos_txt:
    df_filtro = df_filtro[df_filtro["TipoDocumento"] == tipo_doc]

if ano != todos_txt:
    df_filtro = df_filtro[df_filtro["Ano"] == ano]

# =========================
# RESUMO
# =========================
st.subheader(resumo_txt)

col1, col2, col3, col4 = st.columns(4)

col1.metric(total_txt, len(df_filtro))
col2.metric(disciplinas_txt, disciplina)
col3.metric(tipos_txt, tipo_doc)
col4.metric(ano_txt, ano)

# =========================
# TOTAL DE ADPs
# =========================
if area == "ADP" and "StatusADP" in df_filtro.columns:

    df_status_total = df_filtro.copy()

    if lang == "PT":
        status_map_total = {
            "APROVADO": "APROVADO",
            "NÃO APROVADO": "NÃO APROVADO",
            "NAO APROVADO": "NÃO APROVADO",
            "APR. C/ RNC": "APR. C/ RNC",
            "APROVADO C/ RNC": "APR. C/ RNC",
            "APROVADO COM RNC": "APR. C/ RNC"
        }

        aprovado_label = "APROVADO"
        nao_aprovado_label = "NÃO APROVADO"
        rnc_label = "APR. C/ RNC"

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

        aprovado_label = "APPROVED"
        nao_aprovado_label = "NOT APPROVED"
        rnc_label = "APPROVED W/ RNC"

    df_status_total["StatusADP"] = (
        df_status_total["StatusADP"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
        .map(status_map_total)
    )

    st.subheader(total_adp_txt)

    total_adps = len(df_status_total)

    registros_total = "<br>".join(
        map(str, df_status_total["Registro"].dropna())
    )

    df_aprovados = df_status_total[
        df_status_total["StatusADP"] == aprovado_label
    ]

    df_nao_aprovados = df_status_total[
        df_status_total["StatusADP"] == nao_aprovado_label
    ]

    df_rnc = df_status_total[
        df_status_total["StatusADP"] == rnc_label
    ]

    resumo_adp = [
        {
            "Titulo": total_txt,
            "Quantidade": total_adps,
            "Registros": registros_total,
            "Cor": "TOTAL"
        },
        {
            "Titulo": aprovado_label,
            "Quantidade": len(df_aprovados),
            "Registros": "<br>".join(map(str, df_aprovados["Registro"].dropna())),
            "Cor": "STATUS"
        },
        {
            "Titulo": nao_aprovado_label,
            "Quantidade": len(df_nao_aprovados),
            "Registros": "<br>".join(map(str, df_nao_aprovados["Registro"].dropna())),
            "Cor": "STATUS"
        },
        {
            "Titulo": rnc_label,
            "Quantidade": len(df_rnc),
            "Registros": "<br>".join(map(str, df_rnc["Registro"].dropna())),
            "Cor": "STATUS"
        }
    ]

    colunas_resumo_adp = st.columns(4)

    cores_resumo = px.colors.qualitative.Set2

    for idx, item in enumerate(resumo_adp):

        with colunas_resumo_adp[idx]:

            resumo_df = pd.DataFrame([item])

            fig_resumo = px.bar(
                resumo_df,
                x="Titulo",
                y="Quantidade",
                text="Quantidade",
                custom_data=["Registros"],
                color="Cor",
                color_discrete_map={
                    "TOTAL": "#002F6C",
                    "STATUS": cores_resumo[idx % len(cores_resumo)]
                }
            )

            fig_resumo.update_traces(
                textposition="outside",
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    f"{qtd_label}: "
                    "%{y}<br><br>"
                    f"<b>{registros_label}:</b><br>"
                    "%{customdata[0]}"
                    "<extra></extra>"
                ),
                hoverlabel=dict(align="left")
            )

            fig_resumo.update_layout(
                title={
                    "text": item["Titulo"],
                    "x": 0.5
                },
                height=300,
                showlegend=False,
                xaxis_title="",
                yaxis_title=qtd_label,
                hovermode="x unified"
            )

            st.plotly_chart(
                fig_resumo,
                use_container_width=True,
                key=f"resumo_adp_{lang}_{idx}"
            )

# =========================
# STATUS DE APROVAÇÃO DA ADP
# =========================
if area == "ADP" and "StatusADP" in df_filtro.columns:

    st.subheader(status_adp_txt)

    df_status = df_filtro.dropna(subset=["StatusADP"]).copy()

    if not df_status.empty:

        if lang == "PT":
            status_map = {
                "APROVADO": "APROVADO",
                "NÃO APROVADO": "NÃO APROVADO",
                "NAO APROVADO": "NÃO APROVADO",
                "APR. C/ RNC": "APR. C/ RNC",
                "APROVADO C/ RNC": "APR. C/ RNC",
                "APROVADO COM RNC": "APR. C/ RNC"
            }

            ordem_status = [
                "APROVADO",
                "NÃO APROVADO",
                "APR. C/ RNC"
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

        df_status["StatusADP"] = (
            df_status["StatusADP"]
            .astype(str)
            .str.strip()
            .str.upper()
            .map(status_map)
        )

        df_status = df_status.dropna(subset=["StatusADP"])

        ordem_meses = list(meses.values())

        meses_com_status = [
            m for m in ordem_meses
            if not df_status[df_status["Mês"] == m].empty
        ]

        cores = px.colors.qualitative.Set2

        for linha in range(0, len(meses_com_status), 3):
            cols_status = st.columns(3)

            for idx, mes in enumerate(meses_com_status[linha:linha + 3]):
                with cols_status[idx]:

                    df_mes_status = df_status[df_status["Mês"] == mes]

                    status_mes_df = df_mes_status.groupby("StatusADP").agg(
                        Quantidade=("Registro", "count"),
                        Registros=("Registro", lambda x: "<br>".join(map(str, x)))
                    ).reset_index()

                    status_mes_df["StatusADP"] = pd.Categorical(
                        status_mes_df["StatusADP"],
                        categories=ordem_status,
                        ordered=True
                    )

                    status_mes_df = status_mes_df.sort_values("StatusADP")

                    total_registros_status = "<br>".join(map(str, df_mes_status["Registro"]))
                    total_quantidade_status = status_mes_df["Quantidade"].sum()

                    total_status_df = pd.DataFrame({
                        "StatusADP": [total_txt],
                        "Quantidade": [total_quantidade_status],
                        "Registros": [total_registros_status]
                    })

                    status_mes_df = pd.concat(
                        [total_status_df, status_mes_df],
                        ignore_index=True
                    )

                    status_mes_df["Cor"] = status_mes_df["StatusADP"].apply(
                        lambda x: "TOTAL" if x == total_txt else "STATUS"
                    )

                    fig_status = px.bar(
                        status_mes_df,
                        x="StatusADP",
                        y="Quantidade",
                        text="Quantidade",
                        custom_data=["Registros"],
                        color="Cor",
                        color_discrete_map={
                            "STATUS": cores[(linha + idx) % len(cores)],
                            "TOTAL": "#002F6C"
                        }
                    )

                    fig_status.update_traces(
                        textposition="outside",
                        hovertemplate=(
                            "<b>%{x}</b><br>"
                            f"{qtd_label}: "
                            "%{y}<br><br>"
                            f"<b>{registros_label}:</b><br>"
                            "%{customdata[0]}"
                            "<extra></extra>"
                        ),
                        hoverlabel=dict(align="left")
                    )

                    fig_status.update_layout(
                        title={"text": f"📅 {mes}", "x": 0.5},
                        height=320,
                        showlegend=False,
                        hovermode="x unified",
                        xaxis_title="",
                        yaxis_title=qtd_label
                    )

                    st.plotly_chart(
                        fig_status,
                        use_container_width=True,
                        key=f"status_adp_{lang}_{linha}_{idx}_{mes}"
                    )

    else:
        st.info(nenhum_status_txt)

# =========================
# GRÁFICOS POR MÊS E SEMANA
# =========================
st.subheader(grafico_txt)

cores = px.colors.qualitative.Set2
ordem_meses = list(meses.values())

meses_com_dados = [
    m for m in ordem_meses
    if not df_filtro[df_filtro["Mês"] == m].empty
]

for linha in range(0, len(meses_com_dados), 3):
    cols = st.columns(3)

    for idx, mes in enumerate(meses_com_dados[linha:linha + 3]):
        with cols[idx]:

            df_mes = df_filtro[df_filtro["Mês"] == mes]

            semana_df = df_mes.groupby("Semana").agg(
                Quantidade=("Registro", "count"),
                Registros=("Registro", lambda x: "<br>".join(map(str, x)))
            ).reset_index()

            semana_df["SemanaNum"] = pd.to_numeric(
                semana_df["Semana"].str.extract(r"(\d+)")[0],
                errors="coerce"
            ).fillna(0).astype(int)

            semana_df = semana_df.sort_values("SemanaNum")

            total_registros = "<br>".join(map(str, df_mes["Registro"]))
            total_quantidade = semana_df["Quantidade"].sum()

            total_df = pd.DataFrame({
                "Semana": [total_txt],
                "Quantidade": [total_quantidade],
                "Registros": [total_registros],
                "SemanaNum": [999]
            })

            semana_df = pd.concat(
                [total_df, semana_df],
                ignore_index=True
            )

            semana_df["Cor"] = semana_df["Semana"].apply(
                lambda x: "TOTAL" if x == total_txt else "SEMANA"
            )

            fig = px.bar(
                semana_df,
                x="Semana",
                y="Quantidade",
                text="Quantidade",
                custom_data=["Registros"],
                color="Cor",
                color_discrete_map={
                    "SEMANA": cores[(linha + idx) % len(cores)],
                    "TOTAL": "#002F6C"
                }
            )

            fig.update_traces(
                textposition="outside",
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    f"{qtd_label}: "
                    "%{y}<br><br>"
                    f"<b>{registros_label}:</b><br>"
                    "%{customdata[0]}"
                    "<extra></extra>"
                ),
                hoverlabel=dict(align="left")
            )

            fig.update_layout(
                title={"text": f"📅 {mes}", "x": 0.5},
                height=320,
                showlegend=False,
                hovermode="x unified"
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key=f"semanal_{lang}_{linha}_{idx}_{mes}"
            )

# =========================
# TABELA
# =========================
st.subheader(tabela_txt)
st.dataframe(df_filtro.sort_values("Data"), use_container_width=True)
