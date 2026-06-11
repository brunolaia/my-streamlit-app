import streamlit as st
import re

st.set_page_config(page_title="YouTube no Streamlit", layout="wide")

st.title("YouTube no Streamlit")

url = st.text_input("Cole o link do YouTube:")

def pegar_id_youtube(url):
    padroes = [
        r"(?:v=)([^&]+)",
        r"youtu\.be/([^?&]+)",
        r"youtube\.com/embed/([^?&]+)",
        r"youtube\.com/shorts/([^?&]+)"
    ]

    for padrao in padroes:
        resultado = re.search(padrao, url)
        if resultado:
            return resultado.group(1)

    return None

if url:
    video_id = pegar_id_youtube(url)

    if video_id:
        embed_url = f"https://www.youtube-nocookie.com/embed/{video_id}?rel=0"

        st.components.v1.html(
            f"""
            <iframe
                width="100%"
                height="600"
                src="{embed_url}"
                title="YouTube video player"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowfullscreen>
            </iframe>
            """,
            height=620
        )

        st.markdown("### Caso o vídeo não carregue:")
        st.video(f"https://www.youtube.com/watch?v={video_id}")

    else:
        st.error("Link do YouTube inválido.")
else:
    st.info("Cole um link do YouTube para assistir dentro do Streamlit.")
