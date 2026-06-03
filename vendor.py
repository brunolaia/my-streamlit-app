import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="Sistema MDL Vendor", layout="wide")

st.title("📊 Sistema MDL Vendor - CEDOC")

arquivo = st.file_uploader("Envie seu arquivo Excel", type=["xlsx"])

if arquivo:

    try:
        # =========================
        # LER ABAS
        # =========================
        df_mdls = pd.read_excel(arquivo, sheet_name="TODAS MDLS")
        df_docs = pd.read_excel(arquivo, sheet_name="DOCUMENTOS ENVIADOS")

        # =========================
        # LIMPAR UNNAMED
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
        # LIMPAR VALORES
        # =========================
        df_mdls[adf_col] = df_mdls[adf_col].fillna("").astype(str).str.strip()
        df_docs[adf_docs_col] = df_docs[adf_docs_col].fillna("").astype(str).str.strip()

        # =========================
        # MERGE
        # =========================
        df_lookup = df_docs[[adf_docs_col, grd_col]].drop_duplicates()

        df_lookup = df_lookup.rename(columns={
            adf_docs_col: adf_col
        })

        df_lookup = df_lookup[[adf_col, grd_col]]

        df_final = df_mdls.merge(
            df_lookup,
            on=adf_col,
            how="left"
        )

        # =========================
        # FUNÇÃO EXPORT EXCEL
        # =========================
        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Tabela Completa")
            return output.getvalue()

        # =========================
        # MENU
        # =========================
        st.sidebar.title("🔎 MENU")

        opcao = st.sidebar.radio(
            "Selecione:",
            ["Visualizar Tabela", "Buscar", "📊 Dashboard Packages"]
        )

        # =========================
        # BOTÃO DOWNLOAD EXCEL
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

            adf_vazio = str(row[adf_col]).strip() == ""
            tem_grd = pd.notna(row[grd_col]) and str(row[grd_col]).strip() != ""

            if adf_vazio:
                return ["color: red"] * len(row)

            if tem_grd:
                return ["color: #2ecc71"] * len(row)

            return [""] * len(row)

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

            termo = st.text_input("Buscar:")

            if termo:

                df_filtrado = df_final[
                    df_final.astype(str).apply(
                        lambda row: row.str.contains(termo, case=False, na=False).any(),
                        axis=1
                    )
                ]

                st.dataframe(
                    df_filtrado.style.apply(estilizar, axis=1),
                    use_container_width=True,
                    height=700
                )

            else:
                st.info("Digite algo para buscar")

        # =========================
        # DASHBOARD
        # =========================
        elif opcao == "📊 Dashboard Packages":

            st.subheader("📊 Dashboard por Package")

            package_col = [c for c in df_final.columns if "PACK" in c or "PACKAGE" in c][0]

            packages = ["Todos"] + sorted(df_final[package_col].dropna().unique().tolist())

            selected = st.selectbox("Filtrar Package:", packages)

            df_dash = df_final if selected == "Todos" else df_final[df_final[package_col] == selected]

            resumo = df_dash.groupby(package_col).agg(
                TOTAL_ADF=(adf_col, "count"),
                ADF_FALTANTES=(adf_col, lambda x: (x.astype(str).str.strip() == "").sum()),
                GRD_OK=(grd_col, lambda x: x.astype(str).str.strip().ne("").sum())
            ).reset_index()

            st.dataframe(resumo, use_container_width=True)

            fig1 = px.bar(resumo, x=package_col, y="TOTAL_ADF", text_auto=True, title="Total ADF")
            fig2 = px.bar(resumo, x=package_col, y="ADF_FALTANTES", text_auto=True, title="ADF Faltantes", color_discrete_sequence=["red"])
            fig3 = px.bar(resumo, x=package_col, y="GRD_OK", text_auto=True, title="GRD Recebidos", color_discrete_sequence=["green"])

            st.plotly_chart(fig1, use_container_width=True)
            st.plotly_chart(fig2, use_container_width=True)
            st.plotly_chart(fig3, use_container_width=True)

    except Exception as e:
        st.error("Erro ao processar o arquivo")
        st.exception(e)

else:
    st.info("Envie o arquivo Excel para iniciar")

# =========================
# RODAPÉ FIXO
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
        Desenvolvido por Bruno Laia - Rev. 5
    </div>
    """,
    unsafe_allow_html=True
)
