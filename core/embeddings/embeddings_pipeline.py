from .build_embeddings import EmbeddingBuilder
from .load_embeddings import EmbeddingLoader


class EmbeddingsPipeline:

    def __init__(self) -> None:
        self.builder = EmbeddingBuilder()
        self.loader = EmbeddingLoader()


    def pipeline(self, chunks:list[str], metadata:list[dict], collection_name:str|None=None) -> None:

        embeddings = self.builder(chunks)
        vector_dim_size = self.builder.dimensions
        self.loader(
            embedding_vectors=embeddings,
            vector_dim_size=vector_dim_size,
            metadata=metadata,
            collection_name=collection_name
        )
    
    def __call__(self, chunks:list[str], metadata:list[dict]) -> None:
        return self.pipeline(chunks, metadata)