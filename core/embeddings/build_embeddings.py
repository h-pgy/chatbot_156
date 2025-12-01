from config import EMBEDDER_MODEL_NAME, USE_GPU
from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingBuilder:

    def __init__(self, embedder_model_name=EMBEDDER_MODEL_NAME, use_gpu:bool=USE_GPU, batch_size:int=5):
        self.embedder_model_name = embedder_model_name
        self.use_gpu = bool(use_gpu)
        self.batch_size = batch_size

        self.embedder = self.load_embedder()
        self.embeddings = None
        self.dimensions = None
    
    def load_embedder(self) -> SentenceTransformer:
        device = 'cuda' if self.use_gpu else 'cpu'
        embedder = SentenceTransformer(self.embedder_model_name, device=device)
        return embedder
    
    def __check_embedding_dimension(self, embeddings: np.ndarray, chunks:list[str]) -> bool:
        return embeddings.shape[0] == len(chunks)
    
    def build_embeddings(self, chunks: list[str]) -> np.ndarray:
        embeddings = self.embedder.encode(chunks, 
                            normalize_embeddings=True,
                            show_progress_bar=True,
                            batch_size=self.batch_size)
        
        if not self.__check_embedding_dimension(embeddings, chunks):
            raise ValueError("Embedding dimension mismatch.")

        return embeddings
        
    def pipeline(self, chunk:list[str]) -> np.ndarray:
        embeddings = self.build_embeddings(chunk)

        self.embeddings = embeddings
        self.dimensions = self.embedder.get_sentence_embedding_dimension()

        return embeddings
    
    def __call__(self, chunk:list[str]) -> np.ndarray:
        return self.pipeline(chunk)
        