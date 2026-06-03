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
# FUNÇÃO: VERIFICAR VAZIO REAL
# =========================
def vazio(valor):
    return pd.isna(valor) or str(valor).strip() == ""


# =========================
# APP
# =========================
if arquivo:

    try:

        df_mdls = pd.read_excel(arquivo, sheet_name="TODAS MDLS")
        df_docs = pd.read_excel(arquivo, sheet_name="DOCUMENTOS ENVIADOS")

        df_mdls = df_mdls.loc[:, ~df_mdls.columns.astype(str).str.contains("^Unnamed")]
        df_docs = df_docs.loc[:, ~df_docs.columns.astype(str).str.contains("^Unnamed")]

        df_mdls.columns = df_mdls.columns.str.strip()
        df_docs.columns = df_docs.columns.str.strip()

        st.success("Arquivo carregado com sucesso!")

        adf_col = [c for c in df_mdls.columns if "ADF" in c.upper()][0]
        adf_docs_col = [c for c in df_docs.columns if "ADF" in c.upper()][0]
        grd_col = [c for c in df_docs.columns if "GRD" in c.upper()][0]
        package_col = [c for c in df_mdls.columns if "PACK" in c.upper() or "PACKAGE" in c.upper()][0]

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

        df_final = df_mdls.merge(df_historico, on=adf_col, how="left")

        # =========================
        # ALERTAS CORRIGIDOS
        # =========================
        df_sem_adf = df_final[df_final[adf_col].apply(vazio)]

        df_sem_grd = df_final[df_final["HISTORICO_GRD"].apply(vazio)]

        # =========================
        # ESTILO (LINHA VERMELHA CORRETA)
        # =========================
        def estilizar(row):
            if vazio(row[adf_col]):
                return ["color:red"] * len(row)
            return [""] * len(row)

        # =========================
        # SIDEBAR
        # =========================
        st.sidebar.title("🔎 ALERTAS")

        with st.sidebar.expander(f"🔴 ADF vazia ({len(df_sem_adf)})"):
            st.dataframe(df_sem_adf, use_container_width=True)

        with st.sidebar.expander(f"📛 Sem GRD ({len(df_sem_grd)})"):
            st.dataframe(df_sem_grd, use_container_width=True)

        opcao = st.sidebar.radio(
            "Menu:",
            ["Visualizar Tabela", "Buscar", "📊 Dashboard Packages", "📜 Histórico GRD"]
        )

        st.sidebar.download_button(
            "📥 Baixar Excel",
            data=to_excel(df_final),
            file_name="mdl_vendor_tabela.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        # =========================
        # VISUALIZAR
        # =========================
        if opcao == "Visualizar Tabela":
            st.subheader("📋 Tabela Completa")
            st.dataframe(df_final.style.apply(estilizar, axis=1), use_container_width=True, height=700)

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

        # =========================
        # HISTÓRICO
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

                        st.markdown(f"### 📌 ADF: {row[adf_col]}")

                        historico = row.get("HISTORICO_GRD", "")

                        if vazio(historico):
                            st.warning("Sem GRDs registradas")
                        else:
                            for r in str(historico).split("\n"):
                                if r.strip():
                                    st.markdown(f"- Revisão {r}")

                        st.divider()

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
        Desenvolvido por Bruno Laia - Rev. 9.4
    </div>
    """,
    unsafe_allow_html=True
)
