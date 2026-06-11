import streamlit as st
import re

st.set_page_config(page_title="YouTube no Streamlit", layout="wide")

st.title("xxx")

url = st.text_input("xxx:")

def pegar_id_youtube(url):
    padroes = [
        r"v=([^&]+)",
        r"youtu\.be/([^?&]+)",
        r"embed/([^?&]+)"
    ]

    for padrao in padroes:
        resultado = re.search(padrao, url)
        if resultado:
            return resultado.group(1)

    return None

if url:
    video_id = pegar_id_youtube(url)

    if video_id:
        embed_url = f"https://www.youtube.com/embed/{video_id}"

        st.components.v1.html(
            f"""
            <div style="display:flex; justify-content:center;">
                <iframe
                    width="100%"
                    height="600"
                    src="{embed_url}"
                    title="YouTube video player"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                    allowfullscreen>
                </iframe>
            </div>
            """,
            height=620
        )
    else:
        st.error("Link do YouTube inválido.")
else:
    st.info("Cole um link do YouTube para assistir dentro do Streamlit.")
