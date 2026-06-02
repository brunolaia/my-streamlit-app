import streamlit as st

st.title("Calculadora Simples")

a = st.number_input("Primeiro número")
b = st.number_input("Segundo número")

if st.button("Somar"):
    st.success(f"Resultado: {a + b}")