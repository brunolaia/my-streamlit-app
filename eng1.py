import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Engenharia", layout="wide")

st.title("📊 Dashboard - Engenharia NPO")

# =========================
# UPLOAD
# =========================
arquivo = st.file_uploader(
    "📁 Envie sua planilha Excel - Rev.2 - Desenvolvido por Bruno Laia",
    type=["xlsx"]
)

if arquivo is None:
    st.warning("Envie um arquivo Excel para começar.")
    st.stop()

# =========================
# LEITURA
# =========================
df = pd.read_excel(arquivo)

# Mantém apenas as 3 primeiras colunas
df = df.iloc[:, :3]
df.columns = ["Data", "Categoria", "Registro"]

# =========================
# DATA
# =========================
df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
df = df.dropna(subset=["Data"])

df["Ano"] = df["Data"].dt.year
df["MesNum"] = df["Data"].dt.month
df["Dia"] = df["Data"].dt.day

# =========================
# MESES
# =========================
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

df["Mês"] = df["MesNum"].map(meses)

# =========================
# SEMANAS
# =========================
df["SemanaNum"] = ((df["Dia"] - 1) // 7 + 1)
df["Semana"] = "SEMANA " + df["SemanaNum"].astype(str)

st.success("✅ Dados carregados com sucesso")

# =========================
# FILTROS
# =========================
st.sidebar.header("Filtros")

categoria = st.sidebar.selectbox(
    "📂 Categoria",
    sorted(df["Categoria"].dropna().unique())
)

ano = st.sidebar.selectbox(
    "📅 Ano",
    sorted(df["Ano"].unique())
)

df_filtro = df[
    (df["Categoria"] == categoria) &
    (df["Ano"] == ano)
]

# =========================
# INFORMAÇÕES
# =========================
st.subheader("📈 Resumo")

col1, col2 = st.columns(2)

with col1:
    st.metric("Ano Selecionado", ano)

with col2:
    st.metric("Total de Registros", len(df_filtro))

# =========================
# GRÁFICOS
# =========================
st.subheader(f"📊 Registros por Mês e Semana - {ano}")

ordem_meses = list(meses.values())
cores = px.colors.qualitative.Set2

for i, mes in enumerate(ordem_meses):

    df_mes = df_filtro[df_filtro["Mês"] == mes]

    if df_mes.empty:
        continue

    semana_df = (
        df_mes.groupby("Semana")
        .agg(
            Quantidade=("Registro", "count"),
            Registros=("Registro", lambda x: "<br>".join(map(str, x)))
        )
        .reset_index()
    )

    semana_df["SemanaNum"] = (
        semana_df["Semana"]
        .str.extract(r"(\d+)")
        .astype(int)
    )

    semana_df = semana_df.sort_values("SemanaNum")

    fig = px.bar(
        semana_df,
        x="Semana",
        y="Quantidade",
        text="Quantidade",
        title=f"📅 {mes} - {ano}",
        color_discrete_sequence=[cores[i % len(cores)]],
        hover_data={"Registros": True}
    )

    fig.update_traces(
        customdata=semana_df[["Registros"]],
        hovertemplate=
        "<b>%{x}</b><br>" +
        "Quantidade: %{y}<br><br>" +
        "Registros:<br>%{customdata[0]}" +
        "<extra></extra>"
    )

    fig.update_layout(
        xaxis_title="Semanas",
        yaxis_title="Quantidade",
        showlegend=False,
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# TABELA DETALHADA
# =========================
st.subheader("📋 Dados detalhados")

st.dataframe(
    df_filtro.sort_values(["Data"]),
    use_container_width=True
)
