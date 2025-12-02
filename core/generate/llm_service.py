from config import OLLAMA_URL, GEN_MODEL_NAME
from .load_model import GenModelLoader
import requests

class LLMService:

    def __init__(self, model_name: str=GEN_MODEL_NAME) -> None:
        self.model_name = model_name
        self.url = OLLAMA_URL

        self.load_model = GenModelLoader(self.model_name)
        self.load_model()

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream" : False
        }

        response = requests.post(
            f"{self.url}/api/generate",
            json=payload,
            timeout=120
        )
        response.raise_for_status()

        return response.json().get("response", "").strip()
