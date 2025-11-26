from .request_maker import RequestMaker

class Site156:

    domain = 'sp156.prefeitura.sp.gov.br'
    base_endpoint='portal'

    def __init__(self, secure=True) -> None:

        self.request_maker = RequestMaker(domain=self.domain, base_endpoint=self.base_endpoint,
                                          secure=secure)
        
    def service_list_page(self)->str:

        endpoint = 'servicos-online'

        return self.request_maker.get_html_request(endpoint=endpoint)
    
    def subtheme_list_page_by_theme(self, theme_name:str)->str:

        endpoint = 'servicos-online'
        query_params ={'id':theme_name}

        return self.request_maker.get_html_request(endpoint=endpoint, query_params=query_params)
    
    def service_data_by_subtheme(self, subtheme_id:str)->dict:

        endpoint=f"cube/secoes/{subtheme_id}/itens-secao"
        query_params = {'discardInformacoes' : 'true'}

        return self.request_maker.get_json_request(endpoint, query_params)

    
    def service_detail_page(self, service_id=int)->str:

        endpoint = 'informacao'
        query_params={'servico':service_id} 

        return self.request_maker.get_html_request(endpoint=endpoint, query_params=query_params)
    
    