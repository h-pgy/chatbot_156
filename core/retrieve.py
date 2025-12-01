from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from config import QDRANT_COLLECTION_NAME, QDRANT_HOST, QDRANT_PORT, EMBEDDER_MODEL_NAME, USE_GPU

from pydantic import BaseModel
from typing import Dict, Any

class RetrievedDocument(BaseModel):
    score: float
    metadata: Dict[str, Any]
    content: str

class Retriever:

    def __init__(self, top_k:int=5)->None:
        self.qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        device = 'cuda' if USE_GPU else 'cpu'
        self.embedder = SentenceTransformer(EMBEDDER_MODEL_NAME, device=device)

        self.collection_name = QDRANT_COLLECTION_NAME
        self.top_k = top_k

    def embed_query(self, query:str)->list[float]:
        query_embedding = self.embedder.encode(query, 
                                                normalize_embeddings=True,
                                                show_progress_bar=True,
                                                batch_size=5)
        return query_embedding.tolist()
    
    def retrieve(self, embedded_query:list[float])->list[RetrievedDocument]:

        results = self.qdrant_client.query_points(
                collection_name=self.collection_name,
                query=embedded_query,
                limit=self.top_k,
                with_vectors=False,
                with_payload=True
            )
        docs = [RetrievedDocument(
                score = p.score,
                metadata = p.payload,
                content = p.payload.get('content')
            ) for p in results.points]
        
        return docs
    
    def __call__(self, query:str)->list[RetrievedDocument]:
        embedded_query = self.embed_query(query)
        docs = self.retrieve(embedded_query)
        return docs
    

