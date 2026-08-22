import sys
import os

# Add project root to Python path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import streamlit as st

from core.voice import record_voice, speech_to_text


st.set_page_config(
    page_title="Voice Test",
    page_icon="🎤"
)

st.title("🎤 Gima AI - Voice Test")

audio = record_voice()

if audio:

    st.success("✅ Recording completed!")

    st.audio(
        audio["bytes"],
        format="audio/wav"
    )

    with st.spinner("🧠 Converting speech to text..."):

        text = speech_to_text(
            audio["bytes"]
        )


    st.subheader("📝 Transcribed Text")

    st.write(text)