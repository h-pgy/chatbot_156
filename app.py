from typing import Any, Generator
import streamlit as st
import requests
from config import API_URL

BACKEND_URL = f"{API_URL}/ask"

st.set_page_config(page_title="Chat-156", page_icon="💬", layout="centered")

st.title("💬 Chat-156 - Assistente de Serviços da Prefeitura de SP")
st.write("Este chatbot utiliza Inteligência Artificial para responder dúvidas sobre os serviços disponíveis no Portal 156 da Prefeitura de São Paulo.")


# ---------------------------
# Função que consome o streaming da API
# ---------------------------
def stream_from_backend(question:str) -> Generator[str, Any, None]:
    params = {"query": question}
    with requests.get(BACKEND_URL, params=params, stream=True) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=None):
            if chunk:
                yield chunk.decode("utf-8")


# ---------------------------
# UI
# ---------------------------
if "history" not in st.session_state:
    st.session_state.history = []


with st.form("form"):
    question = st.text_input("Faça sua pergunta sobre os serviços do 156:")
    submitted = st.form_submit_button("Enviar")

if submitted and question.strip():
    resp_obj = {"question" : question}

    st.write("### Resposta:")
    placeholder = st.empty()
    full_answer = ""

    # Consome token a token do backend
    for token in stream_from_backend(question):
        full_answer += token
        placeholder.write(full_answer)
    
    resp_obj["answer"] = full_answer

    # Armazena no histórico
    st.session_state.history.append(resp_obj)


# ---------------------------
# Mostrar histórico
# ---------------------------
if st.session_state.history:
    st.write("---")
    st.write("### Histórico de conversas")

    with st.container():
        st.markdown('### Histórico de conversas')

        for msg in st.session_state.history:
            with st.expander(msg['question'][:100]+'...', expanded=False):
                st.markdown(f"**Você:** {msg['question']}")
                st.markdown(f"**Chat-156:** {msg['answer']}")



