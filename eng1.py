import streamlit as st
import pandas as pd
import plotly.express as px
import time

# =========================
# CONFIGURAÇÃO
# =========================
st.set_page_config(page_title="Dashboard Engenharia", layout="wide")

# =========================
# CONTROLE DE IDIOMA
# =========================
if "lang" not in st.session_state:
    st.session_state.lang = "PT"

# =========================
# MENU LATERAL
# =========================
st.sidebar.header("MENU")

# ✅ Captura idioma via URL (hack funcional)
query_lang = st.query_params.get("lang")

if query_lang:
    st.session_state.lang = query_lang

# ✅ Botões com imagem dentro (HTML)
st.sidebar.markdown("""
<div style="display: flex; gap: 10px;">
    
    <a href="?lang=PT" target="_self">
        <button style="padding:6px 10px; font-size:12px; cursor:pointer;">
            <img src="https://flagcdn.com/w20/br.png" 
                 style="vertical-align:middle; margin-right:6px;">
            Português
        </button>
    </a>

    <a href="?lang=EN" target="_self">
        <button style="padding:6px 10px; font-size:12px; cursor:pointer;">
            <img src="https://flagcdn.com/w20/sg.png" 
                 style="vertical-align:middle; margin-right:6px;">
            English
        </button>
    </a>

</div>
""", unsafe_allow_html=True)


# ✅ Define idioma
if "lang" not in st.session_state:
    st.session_state.lang = "PT"

lang = st.session_state.lang

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
    limpar_txt = "🔄 Limpar Filtros"
    resumo_txt = "📈 Resumo"
    total_txt = "Total"
    disciplinas_txt = "Disciplinas"
    tipos_txt = "Tipos"
    grafico_txt = "📊 Registros por Mês e Semana"
    tabela_txt = "📋 Dados detalhados"
    loading_txt = "📥 Carregando base de dados..."
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
    limpar_txt = "🔄 Clear Filters"
    resumo_txt = "📈 Summary"
    total_txt = "Total"
    disciplinas_txt = "Disciplines"
    tipos_txt = "Types"
    grafico_txt = "📊 Records by Month and Week"
    tabela_txt = "📋 Detailed Data"
    loading_txt = "📥 Loading database..."
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
# LEITURA COM LOADING
# =========================
url = "https://raw.githubusercontent.com/brunolaia/my-streamlit-app/main/BD_ENG.xlsx"

progress_bar = st.progress(0)

with st.spinner(loading_txt):

    for i in range(40):
        time.sleep(0.01)
        progress_bar.progress(i + 1)

    df = pd.read_excel(url, engine="openpyxl")

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
df["Semana"] = "WEEK " + df["SemanaNum"].astype(str) if lang == "EN" else "SEMANA " + df["SemanaNum"].astype(str)
st.success("✅ Dados carregados automaticamente - Atualização: 05/06/2026")

# =========================
# FILTROS
# =========================
st.sidebar.subheader(filtros_txt)

lista_disciplina = ["TODAS" if lang=="PT" else "ALL"] + sorted(df["Disciplina"].dropna().unique())
lista_ano = ["TODOS" if lang=="PT" else "ALL"] + sorted(df["Ano"].unique())
lista_tipo = ["TODOS" if lang=="PT" else "ALL"] + sorted(df["TipoDocumento"].dropna().unique())

disciplina = st.sidebar.selectbox(f"📂 {disciplina_txt}", lista_disciplina)
ano = st.sidebar.selectbox(f"📅 {ano_txt}", lista_ano)
tipo_doc = st.sidebar.selectbox(f"📄 {tipo_txt}", lista_tipo)

if st.sidebar.button(limpar_txt):
    st.rerun()

# =========================
# FILTRO
# =========================
df_filtro = df.copy()

if disciplina not in ["TODAS","ALL"]:
    df_filtro = df_filtro[df_filtro["Disciplina"] == disciplina]

if ano not in ["TODOS","ALL"]:
    df_filtro = df_filtro[df_filtro["Ano"] == ano]

if tipo_doc not in ["TODOS","ALL"]:
    df_filtro = df_filtro[df_filtro["TipoDocumento"] == tipo_doc]

# =========================
# RESUMO
# =========================
st.subheader(resumo_txt)

col1, col2, col3 = st.columns(3)

col1.metric(total_txt, len(df_filtro))

texto_disciplina = disciplina if disciplina not in ["TODAS","ALL"] else ("TODAS" if lang=="PT" else "ALL")
col2.metric(disciplinas_txt, texto_disciplina)

texto_tipo = tipo_doc if tipo_doc not in ["TODOS","ALL"] else ("TODOS" if lang=="PT" else "ALL")
col3.metric(tipos_txt, texto_tipo)

# =========================
# GRÁFICOS
# =========================
st.subheader(grafico_txt)

cores = px.colors.qualitative.Set2
ordem_meses = list(meses.values())

meses_com_dados = [m for m in ordem_meses if not df_filtro[df_filtro["Mês"] == m].empty]

for linha in range(0, len(meses_com_dados), 3):

    cols = st.columns(3)

    for idx, mes in enumerate(meses_com_dados[linha:linha+3]):

        with cols[idx]:

            df_mes = df_filtro[df_filtro["Mês"] == mes]

            semana_df = df_mes.groupby("Semana").agg(
                Quantidade=("Registro", "count")
            ).reset_index()

            semana_df["SemanaNum"] = pd.to_numeric(
                semana_df["Semana"].str.extract(r"(\d+)")[0],
                errors="coerce"
            ).fillna(0).astype(int)

            semana_df = semana_df.sort_values("SemanaNum")

            total = semana_df["Quantidade"].sum()

            total_row = pd.DataFrame({
                "Semana": ["TOTAL"],
                "Quantidade": [total],
                "SemanaNum": [0]
            })

            semana_df = pd.concat([total_row, semana_df], ignore_index=True)

            semana_df["Cor"] = semana_df["Semana"].apply(
                lambda x: "TOTAL" if x == "TOTAL" else "SEMANA"
            )

            fig = px.bar(
                semana_df,
                x="Semana",
                y="Quantidade",
                text="Quantidade",
                color="Cor",
                color_discrete_map={
                    "SEMANA": cores[(linha + idx) % len(cores)],
                    "TOTAL": "#002F6C"
                }
            )

            fig.update_layout(
                title={"text": f"📅 {mes}", "x": 0.5},
                height=320,
                showlegend=False,
                hovermode=False
            )

            st.plotly_chart(fig, use_container_width=True)

# =========================
# TABELA
# =========================
st.subheader(tabela_txt)
st.dataframe(df_filtro.sort_values("Data"), use_container_width=True)
