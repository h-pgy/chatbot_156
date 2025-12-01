from pandas import DataFrame
from core.scraper import ScrapePipeline
from core.chunks import ChunkExtractor
from core.embeddings import EmbeddingsPipeline


class InitialLoadPipeline:

    def __init__(self) -> None:
        self.scrape = ScrapePipeline()
        self.extract_chunks = ChunkExtractor()
        self.build_and_load_embeddings = EmbeddingsPipeline()

    def run(self):

        print('Iniciando pipeline de carga inicial...')

        scraped_data: DataFrame = self.scrape()

        print('Dados raspados com sucesso.')

        parsed_chunks: dict[str, list] = self.extract_chunks.extract_chunks(scraped_data)

        print('Chunks extraídos com sucesso.')

        self.build_and_load_embeddings(parsed_chunks['chunks'], parsed_chunks['metadata'])

        print('Embeddings construídos e carregados com sucesso.')

    def __call__(self) -> None: 
        return self.run()
    
if __name__ == '__main__':
    pipeline = InitialLoadPipeline()
    pipeline()