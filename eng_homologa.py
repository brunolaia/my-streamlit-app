# =========================
# STATUS DE APROVAÇÃO DA ADP
# =========================
if area == "ADP" and "StatusADP" in df_filtro.columns:

    st.subheader(status_adp_txt)

    df_status = df_filtro.dropna(subset=["StatusADP"]).copy()

    if not df_status.empty:

        if lang == "PT":
            status_map = {
                "APROVADO": "APROVADO",
                "NÃO APROVADO": "NÃO APROVADO",
                "NAO APROVADO": "NÃO APROVADO",
                "APR. C/ RNC": "APR. C/ RNC",
                "APROVADO C/ RNC": "APR. C/ RNC"
            }

            ordem_status = [
                "APROVADO",
                "NÃO APROVADO",
                "APR. C/ RNC"
            ]

            total_label = "Total"
            status_prefix = "Status: "
            qtd_label = "Quantidade"
            registros_label = "Registros"

        else:
            status_map = {
                "APPROVED": "APPROVED",
                "NOT APPROVED": "NOT APPROVED",
                "APPROVED W/ RNC": "APPROVED W/ RNC",
                "APR. C/ RNC": "APPROVED W/ RNC",
                "APROVADO": "APPROVED",
                "NÃO APROVADO": "NOT APPROVED",
                "NAO APROVADO": "NOT APPROVED",
                "APROVADO C/ RNC": "APPROVED W/ RNC"
            }

            ordem_status = [
                "APPROVED",
                "NOT APPROVED",
                "APPROVED W/ RNC"
            ]

            total_label = "Total"
            status_prefix = "Status: "
            qtd_label = "Quantity"
            registros_label = "Records"

        df_status["StatusADP"] = (
            df_status["StatusADP"]
            .astype(str)
            .str.strip()
            .str.upper()
            .map(status_map)
        )

        df_status = df_status.dropna(subset=["StatusADP"])

        meses_com_status = [
            m for m in ordem_meses
            if not df_status[df_status["Mês"] == m].empty
        ]

        for linha in range(0, len(meses_com_status), 3):
            cols_status = st.columns(3)

            for idx, mes in enumerate(meses_com_status[linha:linha + 3]):
                with cols_status[idx]:

                    df_mes_status = df_status[df_status["Mês"] == mes]

                    status_mes_df = df_mes_status.groupby("StatusADP").agg(
                        Quantidade=("Registro", "count"),
                        Registros=("Registro", lambda x: "<br>".join(map(str, x)))
                    ).reset_index()

                    status_mes_df["StatusADP"] = pd.Categorical(
                        status_mes_df["StatusADP"],
                        categories=ordem_status,
                        ordered=True
                    )

                    status_mes_df = status_mes_df.sort_values("StatusADP")

                    total_registros_status = "<br>".join(map(str, df_mes_status["Registro"]))
                    total_quantidade_status = status_mes_df["Quantidade"].sum()

                    total_status_df = pd.DataFrame({
                        "StatusADP": [total_label],
                        "Quantidade": [total_quantidade_status],
                        "Registros": [total_registros_status]
                    })

                    status_mes_df = pd.concat(
                        [total_status_df, status_mes_df],
                        ignore_index=True
                    )

                    status_mes_df["Cor"] = status_mes_df["StatusADP"].apply(
                        lambda x: "TOTAL" if x == total_label else "STATUS"
                    )

                    fig_status = px.bar(
                        status_mes_df,
                        x="StatusADP",
                        y="Quantidade",
                        text="Quantidade",
                        custom_data=["Registros"],
                        color="Cor",
                        color_discrete_map={
                            "STATUS": cores[(linha + idx) % len(cores)],
                            "TOTAL": "#002F6C"
                        }
                    )

                    fig_status.update_traces(
                        textposition="outside",
                        hovertemplate=(
                            "<b>%{x}</b><br>"
                            f"{qtd_label}: " + "%{y}<br><br>"
                            f"<b>{registros_label}:</b><br>"
                            "%{customdata[0]}"
                            "<extra></extra>"
                        ),
                        hoverlabel=dict(align="left")
                    )

                    fig_status.update_layout(
                        title={"text": f"📅 {mes}", "x": 0.5},
                        height=320,
                        showlegend=False,
                        hovermode="x unified",
                        xaxis_title="",
                        yaxis_title=qtd_label
                    )

                    st.plotly_chart(fig_status, use_container_width=True)

    else:
        if lang == "PT":
            st.info("Nenhum status encontrado para ADP.")
        else:
            st.info("No ADP approval status found.")
