# =========================
# TOTAL
# =========================

total_df = pd.DataFrame({
    "Semana": ["Total"],
    "Quantidade": [total_quantidade],
    "Registros": [total_registros],
    "SemanaNum": [999]
})

semana_df = pd.concat([total_df, semana_df], ignore_index=True)

semana_df["Cor"] = semana_df["Semana"].apply(
    lambda x: "TOTAL" if x == "Total" else "SEMANA"
)

# =========================
# GRÁFICO
# =========================

fig = px.bar(
    semana_df,
    x="Semana",
    y="Quantidade",
    text="Quantidade",
    custom_data=["Registros"],
    color="Cor",
    color_discrete_map={
        "SEMANA": cores[(linha + idx) % len(cores)],
        "TOTAL": "#002F6C"
    }
)

fig.update_traces(
    textposition="outside",
    hovertemplate=(
        "<b>%{x}</b><br>"
        "Quantidade: %{y}<br>"
        "Registros: %{customdata[0]}"
        "<extra></extra>"
    ),
    hoverlabel=dict(align="left")
)

fig.update_layout(
    title={
        "text": f"📅 {mes}",
        "x": 0.5,
        "xanchor": "center"
    },
    height=320,
    showlegend=False,
    hovermode="closest",
    xaxis_title="Semana",
    yaxis_title="Quantidade"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# TABELA
# =========================

st.subheader(tabela_txt)

st.dataframe(
    df_filtro.sort_values("Data"),
    use_container_width=True
)
