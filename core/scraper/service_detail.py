from .site_requests import Site156
from bs4 import BeautifulSoup
from bs4.element import PageElement

class ServiceDetailParser:

    def __init__(self)->None:
        self.site = Site156()


    def page_service_detail_soup(self, service_id:int)->BeautifulSoup:

        page_html = self.site.service_detail_page(service_id)
        sopa = BeautifulSoup(page_html, 'html.parser')
        return sopa
    
    def get_service_description_itens(self, page_soup:BeautifulSoup)->list[PageElement]:

        txt_servico_tag_list = page_soup.find('div', {'id' : 'servicos-texto-holder'})

        if txt_servico_tag_list is None:
            raise RuntimeError("Could not find service description tag list")

        return list(txt_servico_tag_list.children)
    
    def clean_service_description_itens(self, raw_itens:list[PageElement])->list[str]:

        cleaned_itens = [p.text.strip() for p in raw_itens if p.text.strip() != '']
        return cleaned_itens
    
    def build_text_description(self, description_itens:list[str])->str:

        full_description = "\n".join(description_itens)
        return full_description
    

    def pipeline(self, service_id:int)->str:

        sopa = self.page_service_detail_soup(service_id)
        raw_itens = self.get_service_description_itens(sopa)
        cleaned_itens = self.clean_service_description_itens(raw_itens)

        full_description = self.build_text_description(cleaned_itens)

        return full_description
    
    def __call__(self, service_id:int)->str:

        return self.pipeline(service_id)