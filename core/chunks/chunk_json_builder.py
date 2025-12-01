from .parse_description import DescriptionParser
from .build_chunk_header import ChunkHeaderBuilder


class ChunkJsonParser:

    def __init__(self)->None:

        self.parse_description = DescriptionParser()
        self.build_chunk_header = ChunkHeaderBuilder()

    def flaten_chunks(self, parsed_json:dict)->list[str]:

        flatened = []
        for pedacos in parsed_json.values():
            if isinstance(pedacos, list):
                for pedaco in pedacos:
                    flatened.append(pedaco)
            else:
                flatened.append(pedacos)
        
        return flatened

    def pipeline(self, description:str, service_name:str, flatten:bool=True)->dict[str, str]|list[str]:

        parsed_chunks = self.parse_description(description)
        parsed_with_headers = self.build_chunk_header(parsed_chunks, service_name)

        if flatten:
            return self.flaten_chunks(parsed_with_headers)
        
        return parsed_with_headers
    

    def __call__(self, description:str, service_name:str)->list[str]:

        #default is flatten true
        return self.pipeline(description, service_name, flatten=True)
    

    