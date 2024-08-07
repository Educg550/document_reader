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
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks

def main():
    st.set_page_config(page_title="Detector de Contas de Luz", page_icon="📷")

    st.header("Detector de Contas de Luz :bulb:")
    st.text("Insira o TXT obtido da conta de luz")

    with st.sidebar:
        st.subheader("Seus documentos")
        uploaded_file = st.file_uploader("Faça o upload de uma imagem, PDF ou texto puro e clique em Detectar", type=["txt"], accept_multiple_files=False)
        if st.button("Detectar companhia de energia"):
            with st.spinner("Detectando companhia de energia..."):
                if uploaded_file is not None:
                    bytes_text = uploaded_file.read()
                    raw_text = bytes_text.decode("utf-8")

                    text_chunks = get_text_chunks(raw_text)
                    st.write(text_chunks)
                else:
                    st.error("Nenhum arquivo foi enviado")

if __name__ == '__main__':
    main()