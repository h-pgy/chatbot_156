from bs4 import BeautifulSoup
from bs4.element import Tag
import pandas as pd
from .site_requests import Site156

class ServiceThemeListParser:

    def __init__(self)->None:

        self.site = Site156()

    def get_page_soup(self)->BeautifulSoup:

        page_html = self.site.service_list_page()

        return BeautifulSoup(page_html, 'html.parser')
    
    def service_list_section(self, page_soup:BeautifulSoup)->Tag:

        service_list_section = page_soup.find('ol', attrs={'id' : 'lista_servicos_online_pmsp'})

        if service_list_section is None:
            raise RuntimeError('Não foi possível encontrar a tag da lista de serviços.')

        return service_list_section
    

    def service_li_list(self, service_list_section:Tag)->list[Tag]:

        service_list = service_list_section.find_all('li', attrs={'class' : 'collection-item'})

        return service_list
    
    def parse_service_list_item(self, service_list_item:Tag)->dict[str, str]:

        link = service_list_item.find('a')

        if link is None:
            raise RuntimeError(f'Link not found on service list item: {service_list_item}')

        href = link.get('href')
        if href is None:
            raise RuntimeError(f'Href not found on link: {link}')
        name = link.text.strip()

        return {'theme_name' : name, 'href' : str(href)}
    
    def parse_all_service_list_itens(self, service_li_list:list[Tag])->list[dict[str, str]]:

        parsed_data = []
        for li in service_li_list:
            parsed_item = self.parse_service_list_item(li)
            parsed_data.append(parsed_item)
        
        return parsed_data
    
    def service_theme_list_dataframe(self, parsed_list_itens:list[dict[str, str]])->pd.DataFrame:

        df = pd.DataFrame(parsed_list_itens)

        df['theme_id'] = df['href'].str.extract(r"id=([^&]+)")

        return df
    
    def parse_pipeline(self)->pd.DataFrame:

        page_soup = self.get_page_soup()
        service_list_section = self.service_list_section(page_soup)
        service_li_list = self.service_li_list(service_list_section)
        parsed_list_itens = self.parse_all_service_list_itens(service_li_list)
        df = self.service_theme_list_dataframe(parsed_list_itens)

        return df
    
    def __call__(self) -> pd.DataFrame:

        return self.parse_pipeline()