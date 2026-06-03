import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import re

st.set_page_config(page_title="Sistema MDL Vendor", layout="wide")

st.title("📊 Sistema MDL Vendor - CEDOC")

arquivo = st.file_uploader("Envie seu arquivo Excel", type=["xlsx"])

# =========================
# LIMPAR ADF
# =========================
def limpar_adf(adf):
    if pd.isna(adf):
        return ""
    adf = str(adf).strip()
    adf = re.sub(r"[_-][A-Z0-9]+$", "", adf)
    return adf.strip()

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
        # DETECTAR COLUNAS
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
        # ALERTA ADF VAZIA
        # =========================
        df_adf_vazios = df_mdls[df_mdls[adf_col].astype(str).str.strip() == ""]

        if not df_adf_vazios.empty:
            st.warning(f"⚠ Existem {len(df_adf_vazios)} ADFs sem preenchimento!")
            with st.expander("Ver ADFs vazias"):
                st.dataframe(df_adf_vazios, use_container_width=True)

        # =========================
        # HISTÓRICO GRD (1 POR LINHA)
        # =========================
        df_historico = (
            df_docs.groupby("ADF_CLEAN")[grd_col]
            .apply(lambda x: "\n".join(sorted(set(x.dropna().astype(str)))))
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
            label="📥 Baixar Excel",
            data=to_excel(df_final),
            file_name="mdl_vendor_tabela_completa.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # =========================
        # VISUALIZAR
        # =========================
        if opcao == "Visualizar Tabela":

            st.subheader("📋 Tabela Completa")
            st.dataframe(df_final, use_container_width=True, height=700)

        # =========================
        # BUSCAR
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

            resumo = df_final.groupby(package_col).agg(
                TOTAL_ADF=("ADF_CLEAN", "count"),
                GRD_TOTAL=("HISTORICO_GRD", lambda x: x.notna().sum())
            ).reset_index()

            st.dataframe(resumo, use_container_width=True)

            st.plotly_chart(px.bar(resumo, x=package_col, y="TOTAL_ADF", title="Total ADF"), use_container_width=True)
            st.plotly_chart(px.bar(resumo, x=package_col, y="GRD_TOTAL", title="ADF com GRD"), use_container_width=True)

        # =========================
        # HISTÓRICO GRD
        # =========================
        elif opcao == "📜 Histórico GRD":

            st.subheader("📜 Histórico de GRD por ADF")

            adf_sel = st.text_input("Digite ADF (parcial ou completo):")

            if adf_sel:

                adf_sel = limpar_adf(adf_sel)

                resultados = df_final[
                    df_final["ADF_CLEAN"].astype(str).str.contains(adf_sel, na=False)
                ]

                if not resultados.empty:

                    for _, row in resultados.iterrows():

                        st.markdown(f"### 📌 ADF: {row[adf_col]}")

                        historico = str(row.get("HISTORICO_GRD", ""))

                        if historico.strip() == "":
                            st.warning("Sem GRDs registradas")
                        else:
                            grds = [g for g in historico.split("\n") if g.strip()]

                            for g in grds:
                                st.markdown(f"- {g}")

                        st.divider()

                else:
                    st.warning("ADF não encontrada")

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
        Desenvolvido por Bruno Laia - Rev. 7
    </div>
    """,
    unsafe_allow_html=True
)
