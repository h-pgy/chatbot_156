import subprocess
import requests
from config import GEN_MODEL_NAME, OLLAMA_URL

class GenModelLoader:

    def __init__(self, model_name:str=GEN_MODEL_NAME, use_api:bool=True) -> None:

        self.model_name = model_name
        self.ollama_url = OLLAMA_URL
        self.use_api = use_api
        if not self.is_ollama_ready():
            raise EnvironmentError("Ollama server is not running. Please start the Ollama server to proceed.")
        self.solve_methods()

    def is_ollama_ready(self)->bool:
        try:
            r = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            return r.status_code == 200
        except Exception:
            return False
        
    def download_model_via_process(self):
        print(f"Downloading model {self.model_name} using Ollama...")
        try:
            subprocess.run(["ollama", "pull", self.model_name], check=True)
            print(f"Model {self.model_name} downloaded successfully.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to download model {self.model_name}") from e
        
    def download_model_via_api(self):
        print(f'Downloading model {self.model_name} using Ollama API...')
        with requests.post(f"{self.ollama_url}/api/pull", 
                           json={"model": self.model_name},
                           stream=True, 
                           timeout=300) as response:
            
            if response.status_code != 200:
                raise RuntimeError(f"Failed to pull model. Status: {response.status_code}")
            response_txt = []
            for line in response.iter_lines():
                if not line:
                    continue
                
            else:
                print(f"Model {self.model_name} downloaded successfully via API.")
    
    def check_if_model_downloaded_via_process(self) -> bool:
        try:
            result = subprocess.run(["ollama", "list"], check=True, capture_output=True, text=True)
            return self.model_name in result.stdout
        except subprocess.CalledProcessError as e:
            raise RuntimeError("Failed to list Ollama models") from e
        
    def check_if_model_downloaded_via_api(self) -> bool:
        
        try:
            with requests.get(f"{self.ollama_url}/api/tags", timeout=5) as response:

                response.raise_for_status()
                data = response.json()
                installed_models = [m["name"] for m in data.get("models", [])]

                return self.model_name in installed_models

        except Exception as e:
            raise RuntimeError("Failed to list Ollama models via API") from e
        
    def solve_methods(self):
        if not self.use_api:
            self.check_if_model_downloaded = self.check_if_model_downloaded_via_process
            self.download_model = self.download_model_via_process
        else:
            self.check_if_model_downloaded = self.check_if_model_downloaded_via_api
            self.download_model = self.download_model_via_api

    def download_model_pipeline(self) -> str:

        if not self.check_if_model_downloaded():
            self.download_model()
        else:
            print(f"Model {self.model_name} is already downloaded.")
        return self.model_name

    def __call__(self) -> str:
        return self.download_model_pipeline()
        
