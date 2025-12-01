from config import QDRANT_HOST, QDRANT_PORT, QDRANT_DATA_FOLDER, QDRANT_COLLECTION_NAME
import requests
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
import numpy as np

class EmbeddingLoader:

    default_collection_name = QDRANT_COLLECTION_NAME

    def __init__(self, host:str=QDRANT_HOST, port:int=QDRANT_PORT) -> None:

        if not self.__check_qdrant_running():
            raise ConnectionError(f"Qdrant server is not running at {host}:{port}. Please start the server and try again.")

        self.client = QdrantClient(host=host, port=port)
    
    def __check_qdrant_running(self) -> bool:
        try:
            with requests.get(f'http://{QDRANT_HOST}:{QDRANT_PORT}/collections') as r:
                r_qdrant = r.json()
                return r_qdrant['status'] == 'ok'
        except requests.ConnectionError:
            return False
        
    def create_collection(self, collection_name:str, vector_size:int) -> None:

        self.client.recreate_collection(
            collection_name=collection_name,
            vectors_config=qmodels.VectorParams(
                size=vector_size,
                distance=qmodels.Distance.COSINE
            )
        )

        assert self.client.collection_exists(collection_name), f"Failed to create collection {collection_name}."

        print(f'Collection {collection_name} created successfully.')

    def load_to_collection(self, collection_name:str, embedding_vectors:np.ndarray, metadata:list[dict]) -> None:
        
        self.client.upload_collection(
            collection_name=collection_name,
            vectors=embedding_vectors,
            payload=metadata,
            ids=None,        # IDs automáticos
            batch_size=64
        )

        print("Embeddings enviados com sucesso!")

    def pipeline(self, collection_name:str, embedding_vectors:np.ndarray, vector_dim_size:int, metadata:list[dict]) -> None:

        self.create_collection(collection_name, vector_dim_size)
        self.load_to_collection(collection_name, embedding_vectors, metadata)

    def __call__(self, embedding_vectors:np.ndarray, vector_dim_size:int, metadata:list[dict], collection_name:str|None=None) -> None:
        if collection_name is None:
            collection_name = self.default_collection_name
        return self.pipeline(collection_name, embedding_vectors, vector_dim_size, metadata)


    

 