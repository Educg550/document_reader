import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import easyocr
from pdf2image import convert_from_path

def get_llm_model():
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model

def get_llm_response(raw_text, conversation):
    response = conversation.generate_content("Based on the following text excerpt from an electricity bill, answer whether the energy company used is ENEL or CEMIG, answer JUST 'ENEL' OR 'CEMIG'. The text is in Portuguese:\n\n" + raw_text)
    return response.text

def which_company(text):
  company_matches = {
        'enel': {
            'enel', 'enei', 'eletropaulo', 'eietropaulo', 'eletropauio', 'eietropauio', 'eletropau', 'eietropau',
            'enl', 'eneel', 'ennel', 'enell', 'elletropaulo', 'eletropaullo', 'eletropaolo', 'eletrpaulo',
            'eletropaul', 'eletroplauo', 'elrtopaulo', 'eletropalu', 'eletrp', 'elettrp', 'eletorp', 'elettrop',
            'eneii', 'enniei', 'eneli', 'eneil'
        },
        'cemig': {
            'cemig', 'cemlg', 'cenig', 'cenlg',
            'cemg', 'cemiig', 'cemigg', 'semig', 'cemigs',
            'cemige', 'ceemig', 'cemeg', 'cemigee', 'semg',
            'seemig', 'cemlg', 'cmig', 'cmigg', 'cemmigg',
            'ceemlg', 'cenmg', 'cenmig', 'cenmigg'
        }
    }
  words = set(word.lower() for word in text.split())
  for company, matches in company_matches.items():
    if words & matches:
      return company

def get_text_from_text_file(file_path):
    with open(file_path, "r") as f:
        raw_text = f.read()
    return raw_text

def get_text_from_image(file_path):
    ocr_reader = easyocr.Reader(['en'])
    return ocr_reader.readtext(file_path)

def get_text_from_pdf(file_path):
    ocr_reader = easyocr.Reader(['en'])
    # Para cada página, salva em uma subpasta
    pages = convert_from_path(file_path, 500)
    result = ""
    for page in pages:
        file_name = "data/page" + str(pages.index(page)) + ".png"
        page.save(file_name, "PNG")
        result += get_text_from_image(file_name) + "\n"
    return result

# Retorna: [texto extraído da imagem, predição da companhia de energia por visão computacional]
def get_vision_response(file_path):
    image_type = ["jpg", "jpeg", "png"]
    pdf_type = ["pdf"]
    text_type = ["txt"]
    
    if file_path.endswith(tuple(image_type)):
        raw_text = get_text_from_image(file_path)
    if file_path.endswith(tuple(text_type)):
        raw_text = get_text_from_text_file(file_path)
    if file_path.endswith(tuple(pdf_type)):
        raw_text = get_text_from_pdf(file_path)

    vision_predict = which_company(raw_text)
        
    return [raw_text, vision_predict]

def main():
    load_dotenv()
    st.set_page_config(page_title="Detector de Contas de Luz", page_icon="📷")

    st.header("Detector de Contas de Luz :bulb:")
    st.text("Insira o TXT obtido da conta de luz")

    show_vision = st.checkbox("Solução por visão computacional", value=True)
    show_llm = st.checkbox("Solução por LLM", value=False)
    show_raw_text = st.checkbox("Mostrar texto extraído", value=False)

    with st.sidebar:
        st.subheader("Seus documentos")
        uploaded_file = st.file_uploader("Faça o upload de uma imagem, PDF ou texto puro e clique em Detectar", type=["txt", "pdf", "jpg", "jpeg", "png"], accept_multiple_files=False)
        if st.button("Detectar companhia de energia"):
            with st.spinner("Detectando companhia de energia..."):
                if uploaded_file is not None:
                    # Salvando em arquivo na pasta /images
                    # Criando images se não existir
                    if not os.path.exists("data"):
                        os.makedirs("data")

                    file_path = os.path.join("data", uploaded_file.name)
                    with open(os.path.join("data", uploaded_file.name), "wb") as f:
                        f.write(uploaded_file.read())

                    conversation = get_llm_model()

                    [raw_text, vision_predict] = get_vision_response(file_path)
                    llm_predict = get_llm_response(raw_text, conversation)
                    # Mostrar somente se a checkbox estiver marcada
                    if show_vision:
                        st.write("Predição da companhia de energia por visão computacional: ", vision_predict)
                    if show_llm:
                        st.write("Predição da companhia de energia pela LLM (Gemini): ", llm_predict)
                else:
                    st.error("Nenhum arquivo foi enviado")
    if show_raw_text:
        st.write("Texto extraído da imagem: ", raw_text)

if __name__ == '__main__':
    main()