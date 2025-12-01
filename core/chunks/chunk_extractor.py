import pandas as pd
from .chunk_json_builder import ChunkJsonParser
import os
import json
from config import DATA_DIR

class ChunkExtractor:

    fname = 'chunks_metadata.json'

    def __init__(self)->None:

        self.chunk_json_parser = ChunkJsonParser()

    def extract_service_chunks(self, row:pd.Series)->list[str]:

        description = row['description']
        service_name = row['service_desc']
        service_chunks = self.chunk_json_parser(description, service_name)

        return service_chunks


    def build_metadata(self, service_chunks:list[str], row:pd.Series)->list[dict]:

        metadata_list = []
        for chunk in service_chunks:
            parsed_metadata = {
                "service_name": row['service_desc'],
                "service_id" : row['service_id'],
                "theme" : row['theme_name'],
                "subtheme" : row['subtheme_name'],
                "content" : chunk
            }
        
            metadata_list.append(parsed_metadata)

        return metadata_list


    def extract_chunks(self, data: pd.DataFrame) -> dict[str, list]:

        all_chunks = []
        metadata_list = []
        for i, row in data.iterrows():

            chunks = self.extract_service_chunks(row)
            metada = self.build_metadata(chunks, row)
            all_chunks.extend(chunks)
            metadata_list.extend(metada)
            
        assert len(all_chunks) == len(metadata_list)

        parsed = {
            'chunks': all_chunks,
            'metadata': metadata_list
        }

        return parsed
    
    def save_chunks_json(self, parsed:dict[str, list]) -> None:

        json_path = os.path.join(DATA_DIR, self.fname)
        with open(json_path, 'w') as f:
            json.dump(parsed, f, indent=4, ensure_ascii=False)
    
    def pipeline(self, data: pd.DataFrame, save: bool=True) -> dict[str, list]:

        extracted = self.extract_chunks(data)
        if save:
            self.save_chunks_json(extracted)
        return extracted
    
    def __call__(self, data: pd.DataFrame|None=None, save: bool=True) -> dict[str, list]:

        if data is None:
            csv_path = os.path.join(DATA_DIR, '156_service_data.csv')
            data = pd.read_csv(csv_path)

        return self.pipeline(data, save)