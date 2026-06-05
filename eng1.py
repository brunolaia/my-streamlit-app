import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(page_title="Dashboard Engenharia", layout="wide")

st.title("📊 Dashboard - Engenharia NPO - CEDOC")

st.markdown(
    "<p style='color:white; font-size:14px;'>Desenvolvido por Bruno Laia</p>",
    unsafe_allow_html=True
)

# =========================
# LEITURA DO GITHUB
# =========================
url = "https://raw.githubusercontent.com/brunolaia/my-streamlit-app/main/BD_ENG.xlsx"

df = pd.read_excel(url, engine="openpyxl")

# =========================
# TRATAMENTO
# =========================
df = df.iloc[:, :4]
df.columns = ["Data", "Categoria", "Registro", "TipoDocumento"]

df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
df = df.dropna(subset=["Data"])

df["Ano"] = df["Data"].dt.year
df["MesNum"] = df["Data"].dt.month
df["Dia"] = df["Data"].dt.day

meses = {
    1: "JANEIRO", 2: "FEVEREIRO", 3: "MARÇO", 4: "ABRIL",
    5: "MAIO", 6: "JUNHO", 7: "JULHO", 8: "AGOSTO",
    9: "SETEMBRO", 10: "OUTUBRO", 11: "NOVEMBRO", 12: "DEZEMBRO"
}

df["Mês"] = df["MesNum"].map(meses)

df["SemanaNum"] = ((df["Dia"] - 1) // 7 + 1)
df["Semana"] = "SEMANA " + df["SemanaNum"].astype(str)

st.success("✅ Dados carregados automaticamente - Atualização: 05/06/2026")

# =========================
# SESSION STATE (FILTROS)
# =========================
if "categoria" not in st.session_state:
    st.session_state.categoria = "TODAS"
if "ano" not in st.session_state:
    st.session_state.ano = "TODOS"
if "tipo_doc" not in st.session_state:
    st.session_state.tipo_doc = "TODOS"

# =========================
# FILTROS
# =========================
st.sidebar.header("Filtros")

lista_categoria = ["TODAS"] + sorted(df["Categoria"].dropna().unique())
lista_ano = ["TODOS"] + sorted(df["Ano"].unique())
lista_tipo = ["TODOS"] + sorted(df["TipoDocumento"].dropna().unique())

categoria = st.sidebar.selectbox(
    "📂 Categoria", lista_categoria,
    index=lista_categoria.index(st.session_state.categoria)
)

ano = st.sidebar.selectbox(
    "📅 Ano", lista_ano,
    index=lista_ano.index(st.session_state.ano)
)

tipo_doc = st.sidebar.selectbox(
    "📄 Tipo de Documento", lista_tipo,
    index=lista_tipo.index(st.session_state.tipo_doc)
)

st.session_state.categoria = categoria
st.session_state.ano = ano
st.session_state.tipo_doc = tipo_doc

# ✅ BOTÃO LIMPAR
if st.sidebar.button("🔄 Limpar Filtros"):
    st.session_state.categoria = "TODAS"
    st.session_state.ano = "TODOS"
    st.session_state.tipo_doc = "TODOS"
    st.rerun()

# =========================
# APLICA FILTROS
# =========================
df_filtro = df.copy()

if categoria != "TODAS":
    df_filtro = df_filtro[df_filtro["Categoria"] == categoria]

if ano != "TODOS":
    df_filtro = df_filtro[df_filtro["Ano"] == ano]

if tipo_doc != "TODOS":
    df_filtro = df_filtro[df_filtro["TipoDocumento"] == tipo_doc]

# =========================
# RESUMO
# =========================
st.subheader("📈 Resumo")

col1, col2, col3 = st.columns(3)
col1.metric("Total", len(df_filtro))
col2.metric("Categorias", df_filtro["Categoria"].nunique())
col3.metric("Tipos", df_filtro["TipoDocumento"].nunique())

# =========================
# GRÁFICOS
# =========================
st.subheader("📊 Registros por Mês e Semana")

cores = px.colors.qualitative.Set2
ordem_meses = list(meses.values())

meses_com_dados = [m for m in ordem_meses if not df_filtro[df_filtro["Mês"] == m].empty]

for linha in range(0, len(meses_com_dados), 3):

    cols = st.columns(3)

    for idx, mes in enumerate(meses_com_dados[linha:linha+3]):

        with cols[idx]:

            df_mes = df_filtro[df_filtro["Mês"] == mes]

            semana_df = df_mes.groupby("Semana").agg(
                Registros=("Registro", lambda x: "<br>".join(map(str, x)))
            ).reset_index()

            # ✅ Quantidade correta
            semana_df["Quantidade"] = semana_df["Registros"].apply(lambda x: len(x.split("<br>")))

            semana_df["SemanaNum"] = pd.to_numeric(
                semana_df["Semana"].str.extract(r"(\d+)")[0],
                errors="coerce"
            ).fillna(0).astype(int)

            semana_df = semana_df.sort_values("SemanaNum")

            # SOMA MÊS
            total = semana_df["Quantidade"].sum()

            total_row = pd.DataFrame({
                "Semana": ["SOMA MÊS"],
                "Quantidade": [total],
                "Registros": ["TOTAL DO MÊS"],
                "SemanaNum": [0]
            })

            semana_df = pd.concat([total_row, semana_df], ignore_index=True)

            semana_df["Cor"] = semana_df["Semana"].apply(
                lambda x: "TOTAL" if x == "SOMA MÊS" else "SEMANA"
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

            fig.update_traces(
                customdata=semana_df[["Registros"]],
                hovertemplate=
                "<b>%{x}</b><br>" +
                "Quantidade: %{y}<br><br>" +
                "%{customdata[0]}" +
                "<extra></extra>"
            )

            fig.update_layout(
                title={"text": f"📅 {mes}", "x": 0.5},
                height=320,
                showlegend=False,
                hovermode="closest"
            )

            st.plotly_chart(fig, use_container_width=True)

# =========================
# TABELA
# =========================
st.subheader("📋 Dados detalhados")

st.dataframe(df_filtro.sort_values("Data"), use_container_width=True)
