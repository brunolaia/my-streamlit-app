import streamlit as st

st.set_page_config(page_title="Calculadora")

if "display" not in st.session_state:
    st.session_state.display = ""

def clicar(valor):
    if valor == "C":
        st.session_state.display = ""

    elif valor == "=":
        try:
            resultado = str(eval(st.session_state.display))
            st.session_state.display = resultado
        except:
            st.session_state.display = "Erro"

    elif valor == "⌫":
        st.session_state.display = st.session_state.display[:-1]

    else:
        if st.session_state.display == "Erro":
            st.session_state.display = ""
        st.session_state.display += valor

st.title("🧮 Calculadora")

st.text_input(
    "Display",
    value=st.session_state.display,
    disabled=True
)

botoes = [
    ["C", "(", ")", "⌫"],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"]
]

for linha in botoes:
    cols = st.columns(4)

    for i, botao in enumerate(linha):
        with cols[i]:
            if st.button(botao, use_container_width=True):
                clicar(botao)
                st.rerun()