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
    
    def service_list_page_by_tema(self, tema_nome:str)->str:

        endpoint = 'servicos-online'
        query_params ={'id':tema_nome}

        return self.request_maker.get_html_request(endpoint=endpoint, query_params=query_params)
    
    def service_detail_page(self, service_id=int)->str:

        endpoint = 'informacao'
        query_params={'servico':service_id} 

        return self.request_maker.get_html_request(endpoint=endpoint, query_params=query_params)