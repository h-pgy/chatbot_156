from .llm_service import LLMService
from .promp_builder import PromptBuilder


class RespGenerator:

    def __init__(self, llm_service:LLMService, prompt_builder: PromptBuilder) -> None:
        self.llm_service = llm_service
        self.prompt_builder = prompt_builder

    def generate_resp(self, query:str, retrieved_documents:list) -> str:

        prompt: str = self.prompt_builder(query, retrieved_documents)
        response: str = self.llm_service.generate(prompt)

        return response
    
    def __call__(self, query:str, retrieved_documents:list) -> str:
        return self.generate_resp(query, retrieved_documents)