import os
import streamlit as st

from reader.pdf_reader import read_pdf
from reader.pdftoimg import read_scanned_pdf
from test_items.text_splitter import split_text
from core.embeddings import create_embedding
from test_items.faiss_index import build_index


def process_documents(uploaded_files):

    print("Processing Documents")

    chunks=[]
    embeddings=[]

    os.makedirs(
        "uploads",
        exist_ok=True
    )


    st.session_state.file_type=None
    st.session_state.current_file=None


    for file in uploaded_files:

        path=os.path.join(
            "uploads",
            file.name
        )


        with open(path,"wb") as f:
            f.write(file.getbuffer())


        ext=file.name.split(".")[-1].lower()



        # PDF
        if ext=="pdf":

            st.session_state.file_type="pdf"


            text=read_pdf(path)


            if not text.strip():

                text=read_scanned_pdf(path)



            if not text.strip():
                continue



            split_chunks=split_text(text)



            for chunk in split_chunks:

                chunks.append(
                    {
                        "text":chunk,
                        "source":file.name
                    }
                )


                embeddings.append(
                    create_embedding(chunk)
                )



        # IMAGE

        elif ext in ["png","jpg","jpeg"]:


            st.session_state.file_type="image"

            st.session_state.current_file=path



    if embeddings:

        index=build_index(
            embeddings
        )

        return chunks,index


    return [],None