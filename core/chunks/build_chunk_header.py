
class ChunkHeaderBuilder:

    def chunk_header(self, chunk:str, chunk_key: str, service_name:str, posit:int|None=None)->str:

        header = f"[{chunk_key.upper()} | {service_name}]"

        if posit is not None:
            header = f"[{chunk_key.upper()} | {posit} | {service_name}]"

        return header + '\n' + chunk


    def solve_list_chunks(self, parsed:dict, chave:str, service_name:str, splited:list[str])->None:

        parsed[chave] = []
        posit = 1
        for i, item in enumerate(splited):
            if item.replace('\n', '').strip().endswith(':'):
                next = i+1
                dropar = []
                while next < len(splited) and (splited[next].startswith('-') or splited[next][0].isdigit()):
                    dropar.append(next)
                    item = item + '\n ' + splited[next]
                    next+=1
                for index in sorted(dropar, reverse=True):
                    splited.pop(index)
                    
            parsed[chave].append(self.chunk_header(item, chave, service_name, posit))
            posit+=1

    def add_header_to_chunks(self, parsed_chunks:dict[str, str], service_name:str)->dict[str, str]:


        parsed = {}
        #reestruturando os chunks para formato de lista e colocando o header
        for chave, pedacos in parsed_chunks.items():

            splited = pedacos.split('***|||***')
            if len(splited)>1:
                self.solve_list_chunks(parsed, chave, service_name, splited)
            else:
                parsed[chave] = self.chunk_header(pedacos, chave, service_name)

        return parsed
    

    def __call__(self, parsed_chunks:dict[str, str], service_name:str)->dict[str, str]:

        return self.add_header_to_chunks(parsed_chunks, service_name)