from core.scraper.site_requests import Site156
import pandas as pd

class ServiceLinksBySubthemeParser:

    def __init__(self)->None:

        self.site = Site156()

    def parse_service_link_item(self, service_link_item:dict)->dict:

        parsed = {
            'permite_pedido_anomimo' : service_link_item['permiteAnonimo'],
            'img_url' : service_link_item['urlImagem'],
            'service_desc' : service_link_item['descricao'],
            'service_id' : service_link_item['idAsNumber'],
            'ativo' : service_link_item['status']=='ATIVO'
        }

        return parsed

    def parse_service_links_by_subtheme(self, subtheme_id:str, subtheme_data:dict)->list[dict[str, str]]:

        data = self.site.service_data_by_subtheme(subtheme_id)

        parsed_services = []
        for service_item in data['solicitacao']:
            parsed = self.parse_service_link_item(service_item)
            parsed.update(subtheme_data)
            parsed_services.append(parsed)
            
        return parsed_services
    
    def parse_all_service_links(self, df_subthemes:pd.DataFrame)->pd.DataFrame:

        all_parsed_services = []

        for _, row in df_subthemes.iterrows():
            subtheme_id = row['id_subtema']
            subtheme_data = {
                'subtheme_name' : row['nome_subtema'],
                'theme_name' : row['tema_nome']
            }
            parsed_services = self.parse_service_links_by_subtheme(subtheme_id, subtheme_data)
            all_parsed_services.extend(parsed_services)

        df_services = pd.DataFrame(all_parsed_services)

        return df_services
    
    def __call__(self, df_subthemes:pd.DataFrame)->pd.DataFrame:
        return self.parse_all_service_links(df_subthemes)