import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIGURAÇÃO
# =========================
st.set_page_config(page_title="Dashboard Engenharia", layout="wide")

st.title("📊 Dashboard - Engenharia NPO - CEDOC")

# =========================
# UPLOAD
# =========================
arquivo = st.file_uploader("📁 Envie sua planilha Excel&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Desenvolvido por Bruno Laia", type=["xlsx"])

if arquivo is None:
    st.warning("Envie um arquivo Excel para começar.")
    st.stop()

# =========================
# LEITURA
# =========================
df = pd.read_excel(arquivo)
df = df.iloc[:, :4]
df.columns = ["Data", "Categoria", "Registro", "TipoDocumento"]

# =========================
# DATA
# =========================
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

st.success("✅ Dados carregados com sucesso")

# =========================
# FILTROS
# =========================
st.sidebar.header("Filtros")

categoria = st.sidebar.selectbox("📂 Categoria", ["TODAS"] + sorted(df["Categoria"].dropna().unique()))
ano = st.sidebar.selectbox("📅 Ano", ["TODOS"] + sorted(df["Ano"].unique()))
tipo_doc = st.sidebar.selectbox("📄 Tipo Documento", ["TODOS"] + sorted(df["TipoDocumento"].dropna().unique()))

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
col1, col2, col3 = st.columns(3)

col1.metric("Total", len(df_filtro))
col2.metric("Categorias", df_filtro["Categoria"].nunique())
col3.metric("Tipos Doc", df_filtro["TipoDocumento"].nunique())

# =========================
# GRÁFICOS
# =========================
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

            semana_df["SemanaNum"] = semana_df["Semana"].str.extract(r"(\\d+)").astype(int)
            semana_df = semana_df.sort_values("SemanaNum")

            total = semana_df["Quantidade"].sum()

            total_row = pd.DataFrame({
                "Semana": ["TOTAL"],
                "Quantidade": [total],
                "Registros": ["TOTAL DO MÊS"],
                "SemanaNum": [0]
            })

            semana_df = pd.concat([total_row, semana_df])

            semana_df["Cor"] = semana_df["Semana"].apply(lambda x: "TOTAL" if x=="TOTAL" else "SEMANA")

            fig = px.bar(
                semana_df,
                x="Semana",
                y="Quantidade",
                text="Quantidade",
                color="Cor",
                color_discrete_map={
                    "SEMANA": cores[(linha+idx)%len(cores)],
                    "TOTAL": "#002F6C"
                }
            )

            fig.update_traces(
                customdata=semana_df[["Registros"]],
                hovertemplate="<b>%{x}</b><br>Qtd: %{y}<br><br>%{customdata[0]}"
            )

            fig.update_layout(height=320, showlegend=False)

            st.plotly_chart(fig, use_container_width=True)

            # REGISTROS
            for _, r in semana_df.iterrows():
                if r["Semana"] != "TOTAL":
                    with st.expander(f"{mes} - {r['Semana']} ({r['Quantidade']})"):
                        st.write(r["Registros"].split("<br>"))

# =========================
# TABELA
# =========================
st.dataframe(df_filtro.sort_values("Data"), use_container_width=True, height=500)

# =========================
# TEXTO FIXO
# =========================
st.markdown("""
<style>
.top-right {
    position: fixed;
    top: 10px;
    right: 200px;
    color: white;
    font-size: 12px;
    z-index: 9999;
    text-shadow:0 0 6px black;
}
</style>

<div class="top-right">
Desenvolvido por Bruno Laia
</div>
""", unsafe_allow_html=True)
