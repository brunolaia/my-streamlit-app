import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Excel", layout="wide")

st.title("📊 Dashboard de Disciplinas (BÁSICO x DETALHADO)")

file = st.file_uploader("Envie seu arquivo .xlsb", type=["xlsb"])

meses = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março",
    4: "Abril", 5: "Maio", 6: "Junho",
    7: "Julho", 8: "Agosto", 9: "Setembro",
    10: "Outubro", 11: "Novembro", 12: "Dezembro"
}


# 🔎 encontra aba automaticamente
def encontrar_aba(sheet_names, palavra):
    for s in sheet_names:
        if palavra.lower() in s.lower():
            return s
    return None


# 📊 processa dados
def processar(df):
    df = df.iloc[:, [5, 11]].copy()  # F e L
    df.columns = ["disciplina", "data"]

    df = df.dropna()
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df = df.dropna(subset=["data"])

    df["ano"] = df["data"].dt.year
    df["mes_num"] = df["data"].dt.month
    df["mes"] = df["mes_num"].map(meses)

    resumo = (
        df.groupby(["disciplina", "ano", "mes"])
        .size()
        .reset_index(name="quantidade")
    )

    return resumo


# 📈 gráfico
def grafico(df, titulo):
    for disc in df["disciplina"].unique():
        dados = df[df["disciplina"] == disc]

        fig = px.bar(
            dados,
            x="mes",
            y="quantidade",
            color="ano",
            barmode="group",
            text="quantidade",
            title=f"{titulo} - {disc}"
        )

        st.plotly_chart(fig, use_container_width=True)


if file:

    # lê Excel
    xls = pd.ExcelFile(file, engine="pyxlsb")

    st.write("📄 Abas encontradas:", xls.sheet_names)

    aba_basico = encontrar_aba(xls.sheet_names, "basico")
    aba_detalhado = encontrar_aba(xls.sheet_names, "detalhado")

    # 🔵 BÁSICO
    if aba_basico:
        st.header("📌 BÁSICO")

        df_b = pd.read_excel(file, sheet_name=aba_basico, engine="pyxlsb")
        df_b = processar(df_b)
        grafico(df_b, "BÁSICO")

    else:
        st.warning("Aba 'BÁSICO' não encontrada no arquivo.")

    # 🟢 DETALHADO
    if aba_detalhado:
        st.header("📌 DETALHADO")

        df_d = pd.read_excel(file, sheet_name=aba_detalhado, engine="pyxlsb")
        df_d = processar(df_d)
        grafico(df_d, "DETALHADO")

    else:
        st.warning("Aba 'DETALHADO' não encontrada no arquivo.")