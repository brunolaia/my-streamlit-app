import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import re

st.set_page_config(page_title="Sistema MDL Vendor", layout="wide")

st.title("📊 Sistema MDL Vendor - CEDOC")

arquivo = st.file_uploader("Envie seu arquivo Excel", type=["xlsx"])

# =========================
# FUNÇÃO LIMPAR ADF
# =========================
def limpar_adf(adf):
    if pd.isna(adf):
        return ""

    adf = str(adf).strip()

    # remove sufixos tipo _A, _B, -A, -1 no final
    adf = re.sub(r"[_-][A-Z0-9]+$", "", adf)

    return adf.strip()

# =========================
# FUNÇÃO EXCEL EXPORT
# =========================
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Tabela Completa")
    return output.getvalue()

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

        # =========================
        # NORMALIZAR ADF
        # =========================
        df_mdls["ADF_CLEAN"] = df_mdls[adf_col].apply(limpar_adf)
        df_docs["ADF_CLEAN"] = df_docs[adf_docs_col].apply(limpar_adf)

        df_docs[grd_col] = df_docs[grd_col].fillna("").astype(str).str.strip()

        # =========================
        # HISTÓRICO GRD (AGRUPADO)
        # =========================
        df_historico = (
            df_docs.groupby("ADF_CLEAN")[grd_col]
            .apply(lambda x: "\n".join(sorted(set([i for i in x if i != ""]))))
            .reset_index()
            .rename(columns={grd_col: "HISTORICO_GRD"})
        )

        # =========================
        # MERGE FINAL
        # =========================
        df_final = df_mdls.merge(
            df_historico,
            on="ADF_CLEAN",
            how="left"
        )

        # =========================
        # MENU
        # =========================
        st.sidebar.title("🔎 MENU")

        opcao = st.sidebar.radio(
            "Selecione:",
            ["Visualizar Tabela", "Buscar", "📊 Dashboard Packages", "📜 Histórico GRD"]
        )

        # =========================
        # DOWNLOAD EXCEL
        # =========================
        st.sidebar.download_button(
            label="📥 Baixar Tabela em Excel",
            data=to_excel(df_final),
            file_name="mdl_vendor_tabela_completa.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # =========================
        # ESTILO
        # =========================
        def estilizar(row):
            if pd.isna(row.get("HISTORICO_GRD")):
                return [""] * len(row)

            return [""] * len(row)

        # =========================
        # VISUALIZAR
        # =========================
        if opcao == "Visualizar Tabela":

            st.subheader("📋 Tabela Completa")

            st.dataframe(df_final, use_container_width=True, height=700)

        # =========================
        # BUSCAR (AGORA USANDO ADF_CLEAN)
        # =========================
        elif opcao == "Buscar":

            termo = st.text_input("Buscar ADF:")

            if termo:

                termo = limpar_adf(termo)

                df_filtrado = df_final[
                    df_final["ADF_CLEAN"].astype(str).str.contains(termo, na=False)
                ]

                st.dataframe(df_filtrado, use_container_width=True, height=700)

            else:
                st.info("Digite uma ADF")

        # =========================
        # DASHBOARD
        # =========================
        elif opcao == "📊 Dashboard Packages":

            package_col = [c for c in df_final.columns if "PACK" in c or "PACKAGE" in c][0]

            df_dash = df_final

            resumo = df_dash.groupby(package_col).agg(
                TOTAL_ADF=("ADF_CLEAN", "count"),
                GRD_TOTAL=("HISTORICO_GRD", lambda x: x.notna().sum())
            ).reset_index()

            st.dataframe(resumo, use_container_width=True)

            st.plotly_chart(px.bar(resumo, x=package_col, y="TOTAL_ADF", title="Total ADF"), use_container_width=True)
            st.plotly_chart(px.bar(resumo, x=package_col, y="GRD_TOTAL", title="ADF com GRD"), use_container_width=True)

        # =========================
        # HISTÓRICO DETALHADO
        # =========================
        elif opcao == "📜 Histórico GRD":

            st.subheader("📜 Histórico de GRD por ADF")

            adf_sel = st.text_input("Digite ADF para ver histórico:")

            if adf_sel:

                adf_sel = limpar_adf(adf_sel)

                result = df_final[df_final["ADF_CLEAN"] == adf_sel]

                if not result.empty:

                    st.write("### ADF encontrada:")
                    st.write(result[[adf_col, "ADF_CLEAN"]])

                    st.write("### Histórico de GRD:")
                    st.text(result.iloc[0]["HISTORICO_GRD"])
                else:
                    st.warning("ADF não encontrada")

            else:
                st.info("Digite uma ADF para ver o histórico")

    except Exception as e:
        st.error("Erro ao processar o arquivo")
        st.exception(e)

else:
    st.info("Envie o arquivo Excel para iniciar")

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
        Desenvolvido por Bruno Laia - Rev. 6
    </div>
    """,
    unsafe_allow_html=True
)
