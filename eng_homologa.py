import streamlit as st
import pandas as pd
import plotly.express as px
import time
import requests
from datetime import datetime

st.set_page_config(page_title="Dashboard Engenharia - CEDOC", layout="wide")

if "lang" not in st.session_state:
    st.session_state.lang = "PT"

def get_github_file_date():
    try:
        api_url = "https://api.github.com/repos/brunolaia/my-streamlit-app/commits?path=BD_ENG.xlsx&page=1&per_page=1"
        r = requests.get(api_url)

        if r.status_code == 200:
            data = r.json()
            if data:
                date_str = data[0]["commit"]["committer"]["date"]
                return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except:
        pass

    return None

st.sidebar.header("MENU")

col_pt, col_en = st.sidebar.columns(2)

with col_pt:
    if st.button("🇧🇷 Português", key="pt"):
        st.session_state.lang = "PT"

with col_en:
    if st.button("🇸🇬 English", key="en"):
        st.session_state.lang = "EN"

lang = st.session_state.lang

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

if area in ["ENGENHARIA", "ENGINEERING"]:
    sheet_excel = "Planilha1" if lang == "PT" else "Planilha2"
elif area == "ADP":
    sheet_excel = "ADP_PT" if lang == "PT" else "ADP_EN"
elif area == "MTO":
    sheet_excel = "MTO_PT" if lang == "PT" else "MTO_EN"
elif area == "TPS":
    sheet_excel = "TPS_PT" if lang == "PT" else "TPS_EN"

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

st.title(titulo)
st.markdown(f"<p style='color:white; font-size:14px;'>{dev}</p>", unsafe_allow_html=True)

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
df["MesAno"] = df["Mês"] + " " + df["Ano"].astype(str)

df["SemanaNum"] = ((df["Dia"] - 1) // 7 + 1)
df["Semana"] = ("SEMANA " if lang == "PT" else "WEEK ") + df["SemanaNum"].astype(str)

file_date = get_github_file_date()

if file_date:
    if lang == "PT":
        data_formatada = file_date.strftime("%d/%m/%Y")
        st.success(f"✅ Dados carregados com sucesso - Atualizado em {data_formatada}")
    else:
        data_formatada = file_date.strftime("%m/%d/%Y")
        st.success(f"✅ Data loaded successfully - Updated on {data_formatada}")
else:
    st.success("✅ Dados carregados com sucesso")

st.sidebar.subheader(filtros_txt)

lista_disciplina = [todos_txt] + sorted(df["Disciplina"].dropna().unique())
lista_tipo = [todos_txt] + sorted(df["TipoDocumento"].dropna().unique())
lista_ano = [todos_txt] + sorted(df["Ano"].dropna().unique())

disciplina = st.sidebar.selectbox(f"📂 {disciplina_txt}", lista_disciplina)
tipo_doc = st.sidebar.selectbox(f"📄 {tipo_txt}", lista_tipo)
ano = st.sidebar.selectbox(f"📅 {ano_txt}", lista_ano)

df_filtro = df.copy()

if disciplina != todos_txt:
    df_filtro = df_filtro[df_filtro["Disciplina"] == disciplina]

if tipo_doc != todos_txt:
    df_filtro = df_filtro[df_filtro["TipoDocumento"] == tipo_doc]

if ano != todos_txt:
    df_filtro = df_filtro[df_filtro["Ano"] == ano]

st.subheader(resumo_txt)

col1, col2, col3, col4 = st.columns(4)

col1.metric(total_txt, len(df_filtro))
col2.metric(disciplinas_txt, disciplina)
col3.metric(tipos_txt, tipo_doc)
col4.metric(ano_txt, ano)

# =========================
# STATUS DE APROVAÇÃO DA ADP
# =========================
if area == "ADP" and "StatusADP" in df_filtro.columns:

    st.subheader(status_adp_txt)

    df_status = df_filtro.dropna(subset=["StatusADP"]).copy()

    if not df_status.empty:

        df_status["StatusADP"] = df_status["StatusADP"].astype(str).str.strip().str.upper()

        ordem_status = [
            "APROVADO",
            "NÃO APROVADO",
            "APR. C/ RNC"
        ]

        df_status["StatusADP"] = pd.Categorical(
            df_status["StatusADP"],
            categories=ordem_status,
            ordered=True
        )

        status_df = df_status.groupby(
            ["Ano", "MesNum", "MesAno", "StatusADP"],
            observed=False
        ).agg(
            Quantidade=("Registro", "count"),
            Registros=("Registro", lambda x: "<br>".join(map(str, x)))
        ).reset_index()

        status_df = status_df[status_df["Quantidade"] > 0]
        status_df = status_df.sort_values(["Ano", "MesNum", "StatusADP"])

        fig_status = px.bar(
            status_df,
            x="MesAno",
            y="Quantidade",
            color="StatusADP",
            text="Quantidade",
            custom_data=["Registros"],
            barmode="group",
            category_orders={
                "StatusADP": ordem_status,
                "MesAno": status_df.sort_values(["Ano", "MesNum"])["MesAno"].unique()
            }
        )

        fig_status.update_traces(
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Status: %{legendgroup}<br>"
                "Quantidade: %{y}<br><br>"
                "<b>Registros:</b><br>"
                "%{customdata[0]}"
                "<extra></extra>"
            ),
            hoverlabel=dict(align="left")
        )

        fig_status.update_layout(
            height=420,
            showlegend=True,
            hovermode="x unified",
            xaxis_title="Mês e Ano" if lang == "PT" else "Month and Year",
            yaxis_title="Quantidade" if lang == "PT" else "Quantity",
            legend_title_text="Status"
        )

        st.plotly_chart(fig_status, use_container_width=True)

    else:
        st.info("Nenhum status encontrado para ADP.")

# =========================
# GRÁFICOS POR MÊS E SEMANA
# =========================
st.subheader(grafico_txt)

cores = px.colors.qualitative.Set2
ordem_meses = list(meses.values())
meses_com_dados = [m for m in ordem_meses if not df_filtro[df_filtro["Mês"] == m].empty]

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
                "Semana": ["Total"],
                "Quantidade": [total_quantidade],
                "Registros": [total_registros],
                "SemanaNum": [999]
            })

            semana_df = pd.concat([total_df, semana_df], ignore_index=True)

            semana_df["Cor"] = semana_df["Semana"].apply(
                lambda x: "TOTAL" if x == "Total" else "SEMANA"
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
                    "Quantidade: %{y}<br><br>"
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

            st.plotly_chart(fig, use_container_width=True)

st.subheader(tabela_txt)
st.dataframe(df_filtro.sort_values("Data"), use_container_width=True)
