from fastapi import FastAPI, Depends
from core.generate import load_model_instance, LLMService

app = FastAPI()

@app.get("/ask")
async def ask(query: str, model_name: str = Depends(load_model_instance)):
    llm = LLMService(model_name)
    answer = llm.generate(query)
    return {"answer": answer}
