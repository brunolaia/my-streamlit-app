import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(
    page_title="Dashboard Engenharia",
    layout="wide"
)

st.title("📊 Dashboard - Engenharia NPO - CEDOC")

st.markdown(
    "<p style='color:white; font-size:14px;'>Desenvolvido por Bruno Laia</p>",
    unsafe_allow_html=True
)

# =========================
# LEITURA DIRETA DO GITHUB
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

st.success("✅ Dados carregados automaticamente do GitHub")

# =========================
# FILTROS
# =========================
st.sidebar.header("Filtros")

categoria = st.sidebar.selectbox("📂 Categoria", ["TODAS"] + sorted(df["Categoria"].dropna().unique()))
ano = st.sidebar.selectbox("📅 Ano", ["TODOS"] + sorted(df["Ano"].unique()))
tipo_doc = st.sidebar.selectbox("📄 Tipo de Documento", ["TODOS"] + sorted(df["TipoDocumento"].dropna().unique()))

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

col1.metric("Total de Registros", len(df_filtro))
col2.metric("Categorias", df_filtro["Categoria"].nunique())
col3.metric("Tipos de Documento", df_filtro["TipoDocumento"].nunique())

# =========================
# GRÁFICOS
# =========================
st.subheader("📊 Registros por Mês e Semana")

cores = px.colors.qualitative.Set2
ordem_meses = list(meses.values())

meses_com_dados = [
    mes for mes in ordem_meses
    if not df_filtro[df_filtro["Mês"] == mes].empty
]

for linha in range(0, len(meses_com_dados), 3):

    cols = st.columns(3)

    for idx, mes in enumerate(meses_com_dados[linha:linha+3]):

        with cols[idx]:

            df_mes = df_filtro[df_filtro["Mês"] == mes]

            semana_df = (
                df_mes.groupby("Semana")
                .agg(
                    Quantidade=("Registro", "count"),
                    Registros=("Registro", lambda x: "<br>".join(map(str, x)))
                )
                .reset_index()
            )

            semana_df["SemanaNum"] = pd.to_numeric(
                semana_df["Semana"].str.extract(r"(\d+)")[0],
                errors="coerce"
            ).fillna(0).astype(int)

            semana_df = semana_df.sort_values("SemanaNum")

            # SOMA MÊS
            total_mes = semana_df["Quantidade"].sum()

            linha_total = pd.DataFrame({
                "Semana": ["SOMA MÊS"],
                "Quantidade": [total_mes],
                "Registros": ["TOTAL DO MÊS"],
                "SemanaNum": [0]
            })

            semana_df = pd.concat([linha_total, semana_df], ignore_index=True)

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
                showlegend=False
            )

            st.plotly_chart(fig, use_container_width=True)

# =========================
# DADOS DETALHADOS
# =========================
st.subheader("📋 Dados detalhados")

st.dataframe(
    df_filtro.sort_values("Data"),
    use_container_width=True
)
