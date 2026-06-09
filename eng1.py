import streamlit as st
import pandas as pd
import plotly.express as px
import time

# =========================
# CONFIGURAÇÃO
# =========================
st.set_page_config(page_title="Dashboard Engenharia - CEDOC", layout="wide")

# =========================
# CONTROLE DE IDIOMA
# =========================
if "lang" not in st.session_state:
    st.session_state.lang = "PT"

# =========================
# MENU LATERAL
# =========================
st.sidebar.header("MENU")

col_pt, col_en = st.sidebar.columns(2)

with col_pt:
    if st.sidebar.button("🇧🇷 Português"):
        st.session_state.lang = "PT"

with col_en:
    if st.sidebar.button("🇸🇬 English"):
        st.session_state.lang = "EN"

lang = st.session_state.lang

# =========================
# DEFINIR PLANILHA
# =========================
sheet_excel = "Planilha1" if lang == "PT" else "Planilha2"

# =========================
# TEXTOS DINÂMICOS
# =========================
if lang == "PT":
    titulo = "📊 Dashboard - Engenharia NPO - CEDOC"
    dev = "Desenvolvido por Bruno Laia"
    filtros_txt = "Filtros"
    disciplina_txt = "Disciplina"
    ano_txt = "Ano"
    tipo_txt = "Tipo de Documento"
    resumo_txt = "📈 Resumo"
    total_txt = "Total"
    disciplinas_txt = "Disciplina"
    tipos_txt = "Tipo"
    grafico_txt = "📊 Registros por Mês e Semana"
    tabela_txt = "📋 Dados detalhados"
    loading_txt = "📥 Carregando base de dados..."
    todos_txt = "TODOS"
    meses = {
        1: "JANEIRO", 2: "FEVEREIRO", 3: "MARÇO", 4: "ABRIL",
        5: "MAIO", 6: "JUNHO", 7: "JULHO", 8: "AGOSTO",
        9: "SETEMBRO", 10: "OUTUBRO", 11: "NOVEMBRO", 12: "DEZEMBRO"
    }
else:
    titulo = "📊 Dashboard - Engineering NPO - CEDOC"
    dev = "Developed by Bruno Laia"
    filtros_txt = "Filters"
    disciplina_txt = "Discipline"
    ano_txt = "Year"
    tipo_txt = "Document Type"
    resumo_txt = "📈 Summary"
    total_txt = "Total"
    disciplinas_txt = "Disciplines"
    tipos_txt = "Type"
    grafico_txt = "📊 Records by Month and Week"
    tabela_txt = "📋 Detailed Data"
    loading_txt = "📥 Loading database..."
    todos_txt = "ALL"
    meses = {
        1: "JANUARY", 2: "FEBRUARY", 3: "MARCH", 4: "APRIL",
        5: "MAY", 6: "JUNE", 7: "JULY", 8: "AUGUST",
        9: "SEPTEMBER", 10: "OCTOBER", 11: "NOVEMBER", 12: "DECEMBER"
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
df = df.iloc[:, :4]
df.columns = ["Data", "Disciplina", "Registro", "TipoDocumento"]

df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
df = df.dropna(subset=["Data"])

df["Ano"] = df["Data"].dt.year
df["MesNum"] = df["Data"].dt.month
df["Dia"] = df["Data"].dt.day
df["Mês"] = df["MesNum"].map(meses)

df["SemanaNum"] = ((df["Dia"] - 1) // 7 + 1)
df["Semana"] = ("SEMANA " if lang=="PT" else "WEEK ") + df["SemanaNum"].astype(str)

st.success("✅ Dados carregados com sucesso - Atualizado em 09/06/2026" if lang == "PT" else "✅ Data loaded successfully - Updated on 06/09/2026")

# =========================
# FILTROS
# =========================
st.sidebar.subheader(filtros_txt)

lista_disciplina = [todos_txt] + sorted(df["Disciplina"].dropna().unique())
lista_tipo = [todos_txt] + sorted(df["TipoDocumento"].dropna().unique())
lista_ano = [todos_txt] + sorted(df["Ano"].unique())

disciplina = st.sidebar.selectbox(f"📂 {disciplina_txt}", lista_disciplina)
tipo_doc = st.sidebar.selectbox(f"📄 {tipo_txt}", lista_tipo)
ano = st.sidebar.selectbox(f"📅 {ano_txt}", lista_ano)

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
# GRÁFICOS
# =========================
st.subheader(grafico_txt)

st.markdown("""
<style>
.js-plotly-plot .hoverlayer {
    z-index: 999999 !important;
}
</style>
""", unsafe_allow_html=True)

cores = px.colors.qualitative.Set2
ordem_meses = list(meses.values())
meses_com_dados = [m for m in ordem_meses if not df_filtro[df_filtro["Mês"] == m].empty]

for linha in range(0, len(meses_com_dados), 3):
    cols = st.columns(3)

    for idx, mes in enumerate(meses_com_dados[linha:linha+3]):
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

            fig = px.bar(
                semana_df,
                x="Semana",
                y="Quantidade",
                text="Quantidade",
                custom_data=["Registros"],
                color_discrete_sequence=[cores[(linha + idx) % len(cores)]]
            )

            fig.update_traces(
                hovertemplate="<b>%{x}</b><br>Quantidade: %{y}<br><br>%{customdata[0]}<extra></extra>",
                hoverlabel=dict(align="left")
            )

            fig.update_layout(
                title={"text": f"📅 {mes}", "x": 0.5},
                height=320,
                showlegend=False,
                hovermode="x unified"
            )

            st.plotly_chart(fig, use_container_width=True)

# =========================
# TABELA
# =========================
st.subheader(tabela_txt)
st.dataframe(df_filtro.sort_values("Data"), use_container_width=True)
