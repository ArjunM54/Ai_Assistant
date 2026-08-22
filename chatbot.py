import os
import datetime
import streamlit as st

from core.gemini_chat import (ask_gemini, ask_gemini_stream, ask_pdf, ask_image, text_to_speech)
from reader.pdf_reader import read_pdf
from test_items.text_splitter import split_text
from core.embeddings import create_embedding
from core.vectorsearch import search
from test_items.faiss_index import build_index
from reader.pdftoimg import read_scanned_pdf
from reader.read_image import read_image
from core.document_processor import process_documents
from core.voice import(record_voice, speech_to_text, text_to_speech)
# ---------------------------------------------------
# App
# ---------------------------------------------------

st.set_page_config(page_title="Gima AI", page_icon="🤖")
st.title("🤖 Gima AI")

# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_pdf" not in st.session_state:
    st.session_state.current_pdf = None

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "index" not in st.session_state:
    st.session_state.index = None
    
if "loaded_files" not in st.session_state:
    st.session_state.loaded_files = []
    
if "file_type" not in st.session_state:
    st.session_state.file_type = None
    
if "current_file" not in st.session_state:
    st.session_state.current_file = None

# ---------------------------------------------------
# Chat History
# ---------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

uploaded_file = None

with st.sidebar:

    st.title("⚙️ Settings")

    # Process only NEW PDF
    uploaded_file = st.file_uploader(
        "📄 Upload PDF/Image",
        type=[
            "pdf",
            "png",
            "jpg",
            "jpeg"
        ],
        accept_multiple_files=True
    )


    if uploaded_file:

        current_files=[
            f.name for f in uploaded_file
        ]


        if current_files != st.session_state.loaded_files:


            chunks,index=process_documents(
                uploaded_file
            )


            st.session_state.loaded_files=current_files


            if st.session_state.file_type=="image":

                st.success(
                    "🖼 Image Loaded"
                )


            elif index:

                st.session_state.chunks=chunks
                st.session_state.index=index

                st.success(
                    f"📄 PDF Loaded : {len(chunks)} chunks"
                )

            else:

                st.error(
                    "No readable data found"
                )
                
                
    if st.button("🗑 Clear PDF"):

        st.session_state.chunks = []
        st.session_state.index = None
        st.session_state.loaded_files = []
        st.session_state.file_type = None
        st.session_state.current_file = None

        st.success("PDF Cleared")

    if st.session_state.index is not None:
        st.success(
            f"📄 PDF Mode ({st.session_state.index.ntotal} chunks)"
        )

    else:
        st.info("💬 Normal Chat")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []
        st.rerun()

    if st.button("👋 Say Hello"):

        st.success("Hello Arjun 😎")

    if st.button("📆 Show Date"):

        now = datetime.datetime.now()
        st.success(now.strftime("%d-%m-%Y %I:%M:%S %p"))
        
# ---------------------------------------------------
# Voice Input
# ---------------------------------------------------

audio = record_voice()

voice_prompt = None

if audio:

    with st.spinner("🧠 Converting speech to text..."):

        voice_prompt = speech_to_text(
            audio["bytes"]
        )

    if voice_prompt:

        st.success(
            f"🎤 You said: {voice_prompt}"
        )

# ---------------------------------------------------
# Chat input
# ---------------------------------------------------

prompt = st.chat_input("Type your message...")

if voice_prompt:
    prompt = voice_prompt
    

if prompt:

    st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

    with st.chat_message("user"):
        st.markdown(prompt)

    # ----------------------------
    # PDF Mode
    # ----------------------------

    if(
        st.session_state.file_type == "pdf"
        and st.session_state.index is not None
        and st.session_state.index.ntotal > 0
    ):
        history = ""

        for message in st.session_state.messages[-6:]:

            history += f"{message['role']}: {message['content']}\n"

        search_query = history + "\nUser: " + prompt

        query_embedding = create_embedding(search_query)

        results = search(
            query_embedding,
            st.session_state.index,
            st.session_state.chunks
        )
        
        for r in results:
            print("="*50)
            print("Source :", r["source"])
            print("Distance :", r["distance"])
            print(r["chunk"][:200])

        context = "\n\n".join(
            result["chunk"]
            for result in results
        )
        #build the source list.
        sources = []

        for result in results:
            sources.append(
                f"Chunk {result['index'] + 1}"
            )

        sources = list(dict.fromkeys(sources))

        response = ask_pdf(
            prompt,
            context
        )

    # -----------------------------------
    # IMAGE MODE
    # -----------------------------------

    elif st.session_state.file_type == "image":
        print("Before ask_image")
        print("prompt =", prompt)
        print("current_file =", st.session_state.current_file)

        response = ask_image(
            st.session_state.current_file,
            prompt
        )

    # -----------------------------------
    # NORMAL CHAT
    # -----------------------------------

    else:

        response = ask_gemini(
            st.session_state.messages
        )
        
    # used to take the chunk small to think and give response not after 5sec as full response.
    with st.chat_message("assistant"):

        placeholder = st.empty()

        full_response = ""

        if st.session_state.file_type is None:

            stream = ask_gemini_stream(
                st.session_state.messages
            )

            for chunk in stream:

                if chunk.text:

                    full_response += chunk.text

                    placeholder.markdown(full_response + "▌")

            placeholder.markdown(full_response)

            response = full_response

        else:

            placeholder.markdown(response)
            
            # Show sources only for PDF mode
            if (
                st.session_state.file_type == "pdf"
                and len(results) > 0
            ):

                st.markdown("---")
                st.markdown("### 📄 Sources")

                for source in sources:
                    st.markdown(f"- {source}")
                    
        try:

            audio_file = text_to_speech(
                response
            )

            if audio_file:

                st.audio(
                    audio_file,
                    format="audio/wav"
                )

        except Exception as e:

            st.warning(
                f"🔊 Voice output unavailable: {e}"
            )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )