from typing import Any, Generator
import streamlit as st
import requests
from config import API_URL

BACKEND_URL = f"{API_URL}/ask"

st.set_page_config(page_title="Chatbot 156 - RAG", page_icon="💬", layout="centered")

st.title("💬 Chatbot 156 - Assistente de Serviços da Prefeitura de SP")
st.write("Este chatbot usa RAG + Qwen + embeddings do 156 para responder dúvidas.")


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
    st.session_state.history.append({"role": "user", "content": question})

    st.write("### Resposta:")
    placeholder = st.empty()
    full_answer = ""

    # Consome token a token do backend
    for token in stream_from_backend(question):
        full_answer += token
        placeholder.write(full_answer)

    # Armazena no histórico
    st.session_state.history.append({"role": "assistant", "content": full_answer})


# ---------------------------
# Mostrar histórico
# ---------------------------
if st.session_state.history:
    st.write("---")
    st.write("### Histórico")

    for msg in st.session_state.history:
        if msg["role"] == "user":
            st.markdown(f"**Usuário:** {msg['content']}")
        else:
            st.markdown(f"**Chatbot:** {msg['content']}")
