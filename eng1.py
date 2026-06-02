import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Engenharia", layout="wide")

st.title("📊 Dashboard - Engenharia NPO")

# =========================
# UPLOAD
# =========================
arquivo = st.file_uploader("📁 Envie sua planilha Excel - Rev.1 - Desenvolvido por Bruno Laia", type=["xlsx"])

if arquivo is None:
    st.warning("Envie um arquivo Excel para começar.")
    st.stop()

# =========================
# LEITURA
# =========================
df = pd.read_excel(arquivo)

# garante colunas A, B, C
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
    1: "JANEIRO", 2: "FEVEREIRO", 3: "MARÇO",
    4: "ABRIL", 5: "MAIO", 6: "JUNHO",
    7: "JULHO", 8: "AGOSTO", 9: "SETEMBRO",
    10: "OUTUBRO", 11: "NOVEMBRO", 12: "DEZEMBRO"
}

df["Mês"] = df["MesNum"].map(meses)

# =========================
# SEMANA
# =========================
df["SemanaNum"] = ((df["Dia"] - 1) // 7 + 1)
df["Semana"] = "SEMANA " + df["SemanaNum"].astype(str)

st.success("✔ Dados carregados com sucesso")

# =========================
# FILTRO
# =========================
categoria = st.selectbox("📌 Categoria", df["Categoria"].dropna().unique())
df_filtro = df[df["Categoria"] == categoria]

# =========================
# 📊 GRÁFICOS POR MÊS (COM HOVER DETALHADO)
# =========================
st.subheader("🗓️ Registros por Mês e Semana")

ordem_meses = list(meses.values())
cores = px.colors.qualitative.Set2

for i, mes in enumerate(ordem_meses):

    df_mes = df_filtro[df_filtro["Mês"] == mes]

    if df_mes.empty:
        continue

    # 🔥 AGRUPAMENTO COM LISTA DE REGISTROS
    semana_df = df_mes.groupby("Semana").agg(
        Quantidade=("Registro", "count"),
        Registros=("Registro", lambda x: "<br>".join(map(str, x)))
    ).reset_index()

    # ordenar semanas
    semana_df["SemanaNum"] = semana_df["Semana"].str.extract(r"(\d+)").astype(int)
    semana_df = semana_df.sort_values("SemanaNum")

    fig = px.bar(
        semana_df,
        x="Semana",
        y="Quantidade",
        text="Quantidade",
        title=f"📅 {mes}",
        color_discrete_sequence=[cores[i % len(cores)]],
        hover_data={"Registros": True, "Quantidade": True}
    )

    # melhora hover (HTML)
    fig.update_traces(
        hovertemplate=
        "<b>%{x}</b><br>" +
        "Quantidade: %{y}<br><br>" +
        "Registros:<br>%{customdata[0]}<extra></extra>"
    )

    # passa dados extras para hover
    fig.update_traces(customdata=semana_df[["Registros"]])

    fig.update_layout(
        xaxis_title="Semanas",
        yaxis_title="Quantidade",
        xaxis_tickangle=-45,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# 📦 DETALHES
# =========================
st.subheader("📦 Dados detalhados")

st.dataframe(
    df_filtro.sort_values(["Ano", "MesNum", "Dia"]),
    use_container_width=True
)
