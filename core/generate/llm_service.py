from config import OLLAMA_URL, GEN_MODEL_NAME
from .load_model import GenModelLoader
from typing import Generator
import json
import requests

class LLMService:

    def __init__(self, model_name: str=GEN_MODEL_NAME) -> None:
        self.model_name = model_name
        self.url = OLLAMA_URL

        self.load_model = GenModelLoader(self.model_name)
        self.load_model()

    def generate(self, prompt: str) -> Generator[str, None, None]:
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream" : True
        }

        with requests.post(f"{self.url}/api/generate", json=payload, stream=True) as response:
            
            response.raise_for_status()

            for line in response.iter_lines():
                if not line:
                    continue
                try:
                    data = json.loads(line.decode("utf-8"))
                except:
                    continue

                token = data.get("response", "")
                if token:
                    yield token
