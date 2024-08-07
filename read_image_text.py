import streamlit as st
import os
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import HuggingFaceHub
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from huggingface_hub import InferenceApi

# Prompt: Based on the following text excerpt from an electricity bill, answer whether the energy company used is ENEL or CEMIG, answer just one or the other. The text is in Portuguese.

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name='hkunlp/instructor-xl')
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vector_store

def get_conversation_chain(vector_store):
    llm = HuggingFaceHub(repo_id='google/flan-t5-xxl', model_kwargs={'temperature': 0.5, 'max_length': 512})
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_company_name(uploaded_file, conversation):
    response = conversation({'question': "Based on the following text excerpt from an electricity bill, answer whether the energy company used is ENEL or CEMIG, answer just one or the other. The text is in Portuguese."})
    st.write(response['answer'])


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

                    text_chunks = get_text_chunks(raw_text)
                    
                    vector_store = get_vectorstore(text_chunks)

                    conversation = get_conversation_chain(vector_store)

                    handle_company_name(uploaded_file, conversation)
                else:
                    st.error("Nenhum arquivo foi enviado")

if __name__ == '__main__':
    main()