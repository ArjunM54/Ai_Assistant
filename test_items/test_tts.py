import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import streamlit as st

from core.voice import text_to_speech


st.set_page_config(
    page_title="TTS Test",
    page_icon="🔊"
)

st.title("🔊 Gima AI - Text to Speech")


text = st.text_input(
    "Enter text",
    "Hello! I am Gima AI. Nice to meet you."
)


if st.button("🔊 Speak"):

    if text:

        with st.spinner("Generating voice..."):

            audio_file = text_to_speech(text)

        if audio_file:

            st.success("✅ Speech generated!")

            st.audio(
                audio_file,
                format="audio/wav"
            )