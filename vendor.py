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
# FUNÇÃO GRD
# =========================
def extrair_revisao(grd):
    if pd.isna(grd):
        return ""
    grd = str(grd).strip()
    if "_" in grd:
        return grd.split("_")[-1].strip()
    return grd


# =========================
# APP
# =========================
if arquivo:

    try:

        # =========================
        # LER ARQUIVO PRINCIPAL
        # =========================
        df_mdls = pd.read_excel(arquivo, sheet_name="TODAS MDLS")
        df_docs = pd.read_excel(arquivo, sheet_name="DOCUMENTOS ENVIADOS")

        df_mdls = df_mdls.loc[:, ~df_mdls.columns.astype(str).str.contains("^Unnamed")]
        df_docs = df_docs.loc[:, ~df_docs.columns.astype(str).str.contains("^Unnamed")]

        df_mdls.columns = df_mdls.columns.str.strip()
        df_docs.columns = df_docs.columns.str.strip()

        st.success("Arquivo carregado com sucesso!")

        # =========================
        # COLUNAS
        # =========================
        adf_col = next(c for c in df_mdls.columns if "ADF" in c.upper())
        adf_docs_col = next(c for c in df_docs.columns if "ADF" in c.upper())
        grd_col = next(c for c in df_docs.columns if "GRD" in c.upper())
        package_col = next(c for c in df_mdls.columns if "PACK" in c.upper() or "PACKAGE" in c.upper())

        # =========================
        # NORMALIZAÇÃO
        # =========================
        df_docs[grd_col] = df_docs[grd_col].fillna("").astype(str).str.strip()

        # =========================
        # HISTÓRICO GRD
        # =========================
        df_docs["REV_GRD"] = df_docs[grd_col].apply(extrair_revisao)

        df_historico = (
            df_docs.groupby(adf_docs_col)["REV_GRD"]
            .apply(lambda x: "\n".join(sorted(set(x))))
            .reset_index()
            .rename(columns={
                adf_docs_col: adf_col,
                "REV_GRD": "HISTORICO_GRD"
            })
        )

        # =========================
        # MERGE FINAL
        # =========================
        df_final = df_mdls.merge(df_historico, on=adf_col, how="left")

        # =========================
        # ALERTAS
        # =========================
        df_sem_adf = df_final[df_final[adf_col].astype(str).str.strip() == ""]
        df_sem_grd = df_final[df_final["HISTORICO_GRD"].astype(str).str.strip() == ""]

        # =========================
        # ESTILO
        # =========================
        def estilizar(row):
            if str(row[adf_col]).strip() == "":
                return ["color:red"] * len(row)
            return [""] * len(row)

        # =========================
        # MENU
        # =========================
        opcao = st.sidebar.radio(
            "Menu:",
            [
                "Visualizar Tabela",
                "Buscar",
                "📊 Dashboard Packages",
                "📜 Histórico GRD",
                "📦 Juntar MDL"
            ]
        )

        st.sidebar.download_button(
            "📥 Baixar Excel",
            data=to_excel(df_final),
            file_name="mdl_vendor_tabela.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # =========================
        # ALERTAS SIDEBAR
        # =========================
        st.sidebar.title("🔎 ALERTAS")

        with st.sidebar.expander(f"🔴 ADF vazia ({len(df_sem_adf)})"):
            st.dataframe(df_sem_adf, use_container_width=True)

        with st.sidebar.expander(f"📛 Sem GRD ({len(df_sem_grd)})"):
            st.dataframe(df_sem_grd, use_container_width=True)

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
                st.dataframe(
                    df_final[df_final[adf_col].astype(str).str.contains(termo, na=False, case=False)],
                    use_container_width=True,
                    height=700
                )

        # =========================
        # DASHBOARD
        # =========================
        elif opcao == "📊 Dashboard Packages":

            resumo = df_final.groupby(package_col).size().reset_index(name="TOTAL")

            st.subheader("📊 Resumo por Package")

            fig = px.bar(resumo, x=package_col, y="TOTAL", text_auto=True)

            st.plotly_chart(fig, use_container_width=True)

        # =========================
        # HISTÓRICO GRD
        # =========================
        elif opcao == "📜 Histórico GRD":

            st.subheader("📜 Histórico de Revisões")

            adf_sel = st.text_input("Digite o ADF:")

            if adf_sel:

                resultado = df_final[
                    df_final[adf_col].astype(str).str.contains(adf_sel, na=False, case=False)
                ]

                if resultado.empty:
                    st.warning("ADF não encontrado")
                else:
                    for _, row in resultado.iterrows():
                        st.markdown(f"### 📌 {row[adf_col]}")
                        st.text(row.get("HISTORICO_GRD", ""))

        # =========================
        # 📦 JUNTAR MDL (NOVO COMPLETO)
        # =========================
        elif opcao == "📦 Juntar MDL":

            st.subheader("📦 Juntar múltiplos arquivos MDL")

            arquivos = st.file_uploader(
                "Envie múltiplos arquivos Excel",
                type=["xlsx"],
                accept_multiple_files=True
            )

            progresso = st.progress(0)
            status = st.empty()

            if arquivos:

                lista_df = []
                total = len(arquivos)

                for i, file in enumerate(arquivos):

                    status.write(f"Processando: {file.name}")

                    try:
                        df_temp = pd.read_excel(file, skiprows=11)
                        df_temp["ARQUIVO_ORIGEM"] = file.name
                        lista_df.append(df_temp)

                    except Exception as e:
                        st.error(f"Erro em {file.name}: {e}")

                    progresso.progress((i + 1) / total)

                if lista_df:

                    df_junto = pd.concat(lista_df, ignore_index=True)

                    st.success("Arquivos unidos com sucesso!")
                    st.dataframe(df_junto.head(50), use_container_width=True)

                    output = BytesIO()
                    with pd.ExcelWriter(output, engine="openpyxl") as writer:
                        df_junto.to_excel(writer, index=False, sheet_name="MDL_JUNTO")

                    st.download_button(
                        "📥 Baixar MDL Unido",
                        data=output.getvalue(),
                        file_name="mdl_unido.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

            else:
                st.info("Envie múltiplos arquivos para iniciar.")

    except Exception as e:
        st.error("Erro ao processar arquivo")
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
        Desenvolvido por Bruno Laia - Rev. 9.3
    </div>
    """,
    unsafe_allow_html=True
)
