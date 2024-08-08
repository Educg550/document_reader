import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

def get_llm_model():
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model

def handle_company_name(raw_text, conversation):
    response = conversation.generate_content("Based on the following text excerpt from an electricity bill, answer whether the energy company used is ENEL or CEMIG, answer JUST 'ENEL' OR 'CEMIG'. The text is in Portuguese:\n\n" + raw_text)
    st.write(response.text)


def main():
    load_dotenv()
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

                    conversation = get_llm_model()

                    handle_company_name(raw_text, conversation)
                else:
                    st.error("Nenhum arquivo foi enviado")

if __name__ == '__main__':
    main()