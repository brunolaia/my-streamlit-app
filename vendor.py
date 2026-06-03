import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="Sistema MDL Vendor", layout="wide")

st.title("📊 Sistema MDL Vendor - CEDOC")

arquivo = st.file_uploader("Envie seu arquivo Excel", type=["xlsx"])

# =========================
# EXPORT EXCEL
# =========================
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Tabela Completa")
    return output.getvalue()

# =========================
# APP
# =========================
if arquivo:

    try:
        # =========================
        # LER ABAS
        # =========================
        df_mdls = pd.read_excel(arquivo, sheet_name="TODAS MDLS")
        df_docs = pd.read_excel(arquivo, sheet_name="DOCUMENTOS ENVIADOS")

        # =========================
        # LIMPAR COLUNAS
        # =========================
        df_mdls = df_mdls.loc[:, ~df_mdls.columns.astype(str).str.contains("^Unnamed")]
        df_docs = df_docs.loc[:, ~df_docs.columns.astype(str).str.contains("^Unnamed")]

        df_mdls.columns = df_mdls.columns.str.strip()
        df_docs.columns = df_docs.columns.str.strip()

        st.success("Arquivo carregado com sucesso!")

        # =========================
        # COLUNAS
        # =========================
        adf_col = [c for c in df_mdls.columns if "ADF" in c][0]
        adf_docs_col = [c for c in df_docs.columns if "ADF" in c][0]
        grd_col = [c for c in df_docs.columns if "GRD" in c][0]
        package_col = [c for c in df_mdls.columns if "PACK" in c or "PACKAGE" in c][0]

        # =========================
        # NORMALIZAÇÃO (SEM ADF_CLEAN)
        # =========================
        df_docs[grd_col] = df_docs[grd_col].fillna("").astype(str).str.strip()

        # =========================
        # HISTÓRICO GRD
        # =========================
        df_historico = (
            df_docs.groupby(adf_docs_col)[grd_col]
            .apply(lambda x: "\n".join(sorted(set(x.dropna().astype(str)))))
            .reset_index()
            .rename(columns={adf_docs_col: adf_col, grd_col: "HISTORICO_GRD"})
        )

        # =========================
        # MERGE FINAL
        # =========================
        df_final = df_mdls.merge(df_historico, on=adf_col, how="left")

        # =========================
        # ALERTAS
        # =========================
        df_sem_adf = df_final[df_final[adf_col].isna() | (df_final[adf_col].astype(str).str.strip() == "")]
        df_sem_grd = df_final[df_final["HISTORICO_GRD"].isna() | (df_final["HISTORICO_GRD"].astype(str).str.strip() == "")]

        # =========================
        # STYLE (LINHA VERMELHA SEM ADF)
        # =========================
        def estilizar(row):
            if pd.isna(row[adf_col]) or str(row[adf_col]).strip() == "":
                return ["color: red"] * len(row)
            return [""] * len(row)

        # =========================
        # SIDEBAR ALERTAS
        # =========================
        st.sidebar.title("🔎 ALERTAS")

        with st.sidebar.expander(f"🔴 ADF NO. vazia ({len(df_sem_adf)})"):
            st.dataframe(df_sem_adf, use_container_width=True)

        with st.sidebar.expander(f"📛 Sem GRD ({len(df_sem_grd)})"):
            st.dataframe(df_sem_grd, use_container_width=True)

        opcao = st.sidebar.radio(
            "Menu:",
            ["Visualizar Tabela", "Buscar", "📊 Dashboard Packages", "📜 Histórico GRD"]
        )

        st.sidebar.download_button(
            label="📥 Baixar Excel",
            data=to_excel(df_final),
            file_name="mdl_vendor_tabela.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # =========================
        # VISUALIZAR
        # =========================
        if opcao == "Visualizar Tabela":

            st.subheader("📋 Tabela Completa")

            st.dataframe(
                df_final.style.apply(estilizar, axis=1),
                use_container_width=True,
                height=700
            )

        # =========================
        # BUSCAR
        # =========================
        elif opcao == "Buscar":

            termo = st.text_input("Buscar ADF:")

            if termo:

                df_filtrado = df_final[
                    df_final[adf_col].astype(str).str.contains(termo, na=False)
                ]

                st.dataframe(df_filtrado, use_container_width=True, height=700)

        # =========================
        # DASHBOARD PACKAGES (REFEITO)
        # =========================
        elif opcao == "📊 Dashboard Packages":

            resumo = df_final.groupby(package_col).agg(
                TOTAL=("ADF NO." if "ADF NO." in df_final.columns else adf_col, "count"),
                COM_ADF=(adf_col, lambda x: x.notna().sum()),
                SEM_ADF=(adf_col, lambda x: x.isna().sum())
            ).reset_index()

            resumo["PENDENTE"] = resumo["SEM_ADF"]

            st.subheader("📊 Resumo por Package")
            st.dataframe(resumo, use_container_width=True)

            # =========================
            # GRÁFICOS
            # =========================

            fig1 = px.bar(resumo, x=package_col, y="TOTAL", text_auto=True, title="Total de Registros por Package")

            fig2 = px.bar(
                resumo,
                x=package_col,
                y=["COM_ADF", "SEM_ADF"],
                title="Entregues vs Pendentes",
                barmode="stack"
            )

            fig3 = px.pie(
                resumo,
                names=package_col,
                values="TOTAL",
                title="Distribuição de Packages"
            )

            st.plotly_chart(fig1, use_container_width=True)
            st.plotly_chart(fig2, use_container_width=True)
            st.plotly_chart(fig3, use_container_width=True)

        # =========================
# HISTÓRICO GRD
# =========================

def extrair_revisao(grd):
    """
    Exemplos:
    GRD-P2-505-2025_A -> A
    GRD-P2-505-2025_B -> B
    GRD-P2-505-2025_C -> C
    GRD-P2-505-2025-D -> D
    """

    if pd.isna(grd):
        return ""

    grd = str(grd).strip()

    # prioridade para padrão com "_"
    if "_" in grd:
        return grd.split("_")[-1].strip()

    # se não existir "_", pega o que vem após o último "-"
    if "-" in grd:
        return grd.split("-")[-1].strip()

    return grd

df_docs["REV_GRD"] = df_docs[grd_col].apply(extrair_revisao)

df_historico = (
    df_docs.groupby(adf_docs_col)["REV_GRD"]
    .apply(
        lambda x: "\n".join(
            sorted(
                set(
                    str(v).strip()
                    for v in x
                    if str(v).strip()
                )
            )
        )
    )
    .reset_index()
    .rename(
        columns={
            adf_docs_col: adf_col,
            "REV_GRD": "HISTORICO_GRD"
        }
    )
)

# =========================
# RODAPÉ
# =========================
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0e1117;
        color: #ffffff;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #333;
        z-index: 999;
    }
    </style>

    <div class="footer">
        Desenvolvido por Sistema MDL Vendor - Rev. 9.0
    </div>
    """,
    unsafe_allow_html=True
)
