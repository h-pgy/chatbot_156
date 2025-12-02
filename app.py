from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from core.generate import LLMService, PromptBuilder, RespGenerator
from core.retrieve import Retriever
from config import GEN_MODEL_NAME

app = FastAPI()

llm_service = LLMService(GEN_MODEL_NAME)
prompt_builder = PromptBuilder()
retrieve_docs = Retriever(top_k=5)

def get_resp_generator():
    return RespGenerator(llm_service, prompt_builder)


@app.get("/ask")
async def ask(query: str, resp_generator: RespGenerator = Depends(get_resp_generator)):
    
    docs = retrieve_docs(query)
    gen = resp_generator(query=query, retrieved_documents=docs)
    return StreamingResponse(gen, media_type="text/plain")
