import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter

# Prompt: Based on the following text excerpt from an electricity bill, answer whether the energy company used is ENEL or CEMIG, answer just one or the other. The text is in Portuguese.

# # Textos iniciais estão em /texts
# def get_existing_text_database():
#     with open('texts/initial_text.txt', 'r') as file:
#         data = file.read()
#     return data

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        text=raw_text,
        max_chunk_size=500,
        min_chunk_size=300
    )

def main():
    st.set_page_config(page_title="Detector de Contas de Luz", page_icon="📷")

    st.header("Detector de Contas de Luz :bulb:")
    st.text("Faça o upload de uma imagem, texto puro ou PDF de uma conta de luz para detectar a companhia de energia.")

    with st.sidebar:
        st.subheader("Seus documentos")
        uploaded_file = st.file_uploader("Faça o upload de uma imagem, PDF ou texto puro", type=["jpg", "jpeg", "png", "pdf", "txt"], accept_multiple_files=False)
        st.button("Detectar companhia de energia")

if __name__ == '__main__':
    main()