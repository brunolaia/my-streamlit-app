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

# =========================
# UPLOAD
# =========================
arquivo = st.file_uploader(
    "📁 Envie sua planilha Excel&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbspDesenvolvido por Bruno Laia",
    type=["xlsx"]
)

if arquivo is None:
    st.warning("Envie um arquivo Excel para começar.")
    st.stop()

# =========================
# LEITURA
# =========================
df = pd.read_excel(arquivo)

# Agora mantém 4 colunas
df = df.iloc[:, :4]
df.columns = ["Data", "Categoria", "Registro", "TipoDocumento"]

# =========================
# TRATAMENTO DE DATAS
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
    1: "JANEIRO", 2: "FEVEREIRO", 3: "MARÇO", 4: "ABRIL",
    5: "MAIO", 6: "JUNHO", 7: "JULHO", 8: "AGOSTO",
    9: "SETEMBRO", 10: "OUTUBRO", 11: "NOVEMBRO", 12: "DEZEMBRO"
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

categorias = ["TODAS"] + sorted(df["Categoria"].dropna().unique().tolist())
anos = ["TODOS"] + sorted(df["Ano"].unique().tolist())
tipos = ["TODOS"] + sorted(df["TipoDocumento"].dropna().unique().tolist())

categoria = st.sidebar.selectbox("📂 Categoria", categorias)
ano = st.sidebar.selectbox("📅 Ano", anos)
tipo_doc = st.sidebar.selectbox("📄 Tipo de Documento", tipos)

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

with col1:
    st.metric("Total de Registros", len(df_filtro))

with col2:
    st.metric("Categorias", df_filtro["Categoria"].nunique())

with col3:
    st.metric("Tipos de Documento", df_filtro["TipoDocumento"].nunique())

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

# =========================
# 3 GRÁFICOS POR LINHA
# =========================
for linha in range(0, len(meses_com_dados), 3):

    cols = st.columns(3)

    for idx, mes in enumerate(meses_com_dados[linha:linha+3]):

        with colsdf_mes = df_filtro[df_filtro["Mês"] == mes]

            semana_df = (
                df_mes.groupby("Semana")
                .agg(
                    Quantidade=("Registro", "count"),
                    Registros=("Registro", lambda x: "<br>".join(map(str, x)))
                )
                .reset_index()
            )

            # Ordena semanas
            semana_df["SemanaNum"] = (
                semana_df["Semana"].str.extract(r"(\d+)").astype(int)
            )
            semana_df = semana_df.sort_values("SemanaNum")

            # Calcula TOTAL do mês
            total_mes = semana_df["Quantidade"].sum()

            # Cria linha TOTAL
            linha_total = pd.DataFrame({
                "Semana": ["TOTAL"],
                "Quantidade": [total_mes],
                "Registros": ["TOTAL DO MÊS"],
                "SemanaNum": [0]  # força ficar em primeiro lugar
            })

            # Junta TOTAL + semanas
            semana_df_total = pd.concat([linha_total, semana_df], ignore_index=True)

            # Cor diferenciada
            semana_df_total["Cor"] = semana_df_total["Semana"].apply(
                lambda x: "TOTAL" if x == "TOTAL" else "SEMANA"
            )

            # Gráfico
            fig = px.bar(
                semana_df_total,
                x="Semana",
                y="Quantidade",
                text="Quantidade",
                color="Cor",
                color_discrete_map={
                    "SEMANA": cores[(linha + idx) % len(cores)],
                    "TOTAL": "#002F6C"  # azul escuro
                }
            )

            fig.update_traces(
                width=0.35,
                customdata=semana_df_total[["Registros"]],
                hovertemplate=
                "<b>%{x}</b><br>" +
                "Quantidade: %{y}<br><br>" +
                "Registros:<br>%{customdata[0]}" +
                "<extra></extra>"
            )

            fig.update_layout(
                title={"text": f"📅 {mes}", "x": 0.5},
                height=320,
                margin=dict(l=10, r=10, t=50, b=10),
                showlegend=False,
                xaxis_title="",
                yaxis_title="Quantidade",
                xaxis_tickangle=-45
            )

            st.plotly_chart(fig, use_container_width=True)
# =========================
# DADOS DETALHADOS
# =========================
st.subheader("📋 Dados detalhados")

st.dataframe(
    df_filtro.sort_values(["Data"]),
    use_container_width=True,
    height=500
)


# =========================
# TOPO FIXO (DIREITA - TEXTO BRANCO)
# =========================
st.markdown(
    """
    <style>
    .top-right {
        position: fixed;
        top: 10px;
        right: 200px;
        font-size: 12px;
        color: white;
        z-index: 9999;
    }
    </style>

    <div class="top-right">
        Desenvolvido por Bruno Laia
    </div>
    """,
    unsafe_allow_html=True
)
