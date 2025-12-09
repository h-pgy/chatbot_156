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


# ---------------------------
# SIDEBAR
# ---------------------------
with st.sidebar:
    st.title("ℹ️ Sobre o projeto")

    # ---------------------------
    # Seção 1 — Como foi feito
    # ---------------------------
    with st.container():
        st.subheader("Como foi feito")
        st.markdown(
            """
            Este chatbot utiliza uma arquitetura **RAG** e modelos **open source** para responder dúvidas sobre o Portal 156.
            """
        )
        with st.expander("Clique para ver mais detalhes"):
            st.markdown(
                """
                O sistema foi desenvolvido utilizando uma arquitetura **RAG (Retrieval-Augmented Generation)**.  
                Nesse modelo, antes de gerar uma resposta, a IA busca informações relevantes em uma base de documentos — no caso, os textos da Carta de Serviços do Portal 156, que foram scrapeados do site e estruturados em um banco de dados vetorizado (QDRANT). Isso garante respostas mais precisas, atuais e alinhadas ao conteúdo oficial, reduzindo alucinações comuns em modelos puramente generativos.

                Para o processamento de dados, o projeto utiliza o **modelo open source Qwen**, responsável pela geração das respostas, em conjunto com o **modelo SBERT** para criação de *embeddings*, que permitem encontrar trechos relevantes nos documentos. Essa combinação garante rapidez na recuperação das informações e qualidade na geração do texto final.

                Este chatbot é um **MVP experimental**, desenvolvido como trabalho final da disciplina **“Fundamentos, Governança e Ferramentas de IA para Tomada de Decisões”** da **Universidade Complutense de Madrid**.

                Como todo LLM, o Chat-156 pode apresentar imprecisões ou erros. Recomenda-se sempre consultar os canais oficiais da Prefeitura de São Paulo para informações definitivas.
                """
            )

    st.write("---")

    # ---------------------------
    # Seção 2 — Código fonte
    # ---------------------------
    with st.container():
        st.subheader("Código no GitHub")

        github_logo_url = "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(github_logo_url, width=32)
        with col2:
            st.markdown("[Repositório no GitHub](https://github.com/h-pgy/chatbot_156)")

        st.write("---")

    # ---------------------------
    # Seção 3 — LinkedIn
    # ---------------------------
    with st.container():
        st.subheader("Contato profissional")
        st.markdown("**Desenvolvido por Henrique Pougy**")

        linkedin_logo_url = "https://cdn-icons-png.flaticon.com/512/174/174857.png"

        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(linkedin_logo_url, width=32)
        with col2:
            st.markdown("[Meu LinkedIn](https://www.linkedin.com/in/henrique-pougy/)")




if "history" not in st.session_state:
    st.session_state.history = []


with st.form("form"):
    question = st.text_input("Faça sua pergunta sobre os serviços do 156:")
    submitted = st.form_submit_button("Enviar")

if submitted and question.strip():
    resp_obj = {"question" : question}
    placeholder = st.empty()
    st.write("### Resposta:")
    answer_placeholder = st.empty()

    with st.spinner("Aguarde enquanto o Chat-156 elabora a resposta..."):
        resp_gen = stream_from_backend(question)
        full_answer = answer_placeholder.write_stream(resp_gen, cursor='...')

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
        for msg in st.session_state.history:
            with st.expander(msg['question'][:100]+'...', expanded=False):
                st.markdown(f"**Você:** {msg['question']}")
                st.markdown(f"**Chat-156:** {msg['answer']}")
    # Botão de limpar histórico
    if st.button("🗑️ Limpar histórico"):
        st.session_state.history = []
        st.rerun()

# ---------------------------
# Footer — Aviso de uso responsável
# ---------------------------
st.divider()
st.markdown(
    """
### 🛡️ Aviso de uso responsável da IA
As respostas são geradas por modelos de IA e **podem conter imprecisões**.  
Não substituem canais oficiais da Prefeitura de São Paulo.
    """
)




