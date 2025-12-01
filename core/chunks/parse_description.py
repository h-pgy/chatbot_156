import pandas as pd
import unicodedata

class DescriptionParser:
    
    def remover_acentos(self, texto: str) -> str:

        nfkd = unicodedata.normalize("NFD", texto)
        texto_sem_acentos = "".join(
            c for c in nfkd if unicodedata.category(c) != "Mn"
        )
        
        return texto_sem_acentos

    def clean_chave(self, chave:str) -> str:

        chave = chave.lower().replace(' ', '_').replace('-', '_').replace(',', '_').replace('__', '_').strip()
        chave = self.remover_acentos(chave)

        return chave
    
    def clean_pedaco(self, pedaco:str)->str:

        pedaco = pedaco.strip().replace('\xa0', '').replace('clique aqui', '')
        return pedaco

    def split_description(self, description:str)->list[str]:

        return description.split('\n')


    def parse_data_atualizacao(self, pedacos:list[str])->str:

        atualizacao = pedacos.pop(-1).replace('Atualizado em:', '').strip()
        return atualizacao

    def parse_data_criacao(self, pedacos:list[str])->str:
        #precisa rodar depois de parse_data_atualizacao

        criacao  = pedacos.pop(-1).replace('Criado em:', '').strip()
        return criacao

    def build_keys_values(self, pedacos:list[str])->dict[str, str]:

        parsed = {}
        chave = None
        for pedaco in pedacos:
            if pedaco.isupper():
                chave = self.clean_chave(pedaco)
            else:
                if chave:
                    if chave not in parsed:
                        parsed[chave] = self.clean_pedaco(pedaco)
                    else:
                        parsed[chave] =  parsed[chave] + '***|||***' + self.clean_pedaco(pedaco)
        
        return parsed

    def parse_description(self, description:str)->dict[str, str]:

        pedacos = self.split_description(description)

        parsed = {}
        parsed['data_atualizacao'] = self.parse_data_atualizacao(pedacos)
        parsed['data_criacao'] = self.parse_data_criacao(pedacos)

        key_values = self.build_keys_values(pedacos)
        parsed.update(key_values)
        
        return parsed
    
    def pipeline(self, service_description:str) -> dict[str, str]:

        return self.parse_description(service_description)
    
    def __call__(self, service_description:str) -> dict[str, str]:

        return self.pipeline(service_description)