from bs4 import BeautifulSoup
from bs4.element import Tag
import pandas as pd

from .site_requests import Site156


class SubthemesByThemeParser:

    def __init__(self)->None:
    
        self.site = Site156()

    def get_theme_page_soup(self, theme_name:str)->BeautifulSoup:

        page_html = self.site.subtheme_list_page_by_theme(theme_name=theme_name)
        page_soup = BeautifulSoup(page_html, 'html.parser')

        return page_soup
    
    def get_subthemes(self, theme_page_soup:BeautifulSoup)->list[Tag]:

        subtheme_divs = theme_page_soup.find_all('div', 
                                                 attrs={'class' : 'collapsible-header sp_red-text'})

        return subtheme_divs
    
    def parse_subtheme(self, subtheme_div:Tag)->dict[str, str]:



        id_subtema = subtheme_div.get('data-assunto')

        if id_subtema is None or len(str(id_subtema).strip())==0:
            raise RuntimeError('Subtheme div has no id attribute')
        
        id_subtema= str(id_subtema).strip()
        
        nome_subtema = subtheme_div.text.strip()

        return {'id_subtema' : id_subtema,
                'nome_subtema' : nome_subtema}
    
    def parse_all_subthemes_by_theme(self, theme_name:str, theme_id:str)->list[dict[str, str]]:

        theme_page_soup = self.get_theme_page_soup(theme_id)
        subtheme_divs = self.get_subthemes(theme_page_soup)

        subthemes_data = [self.parse_subtheme(div) for div in subtheme_divs]

        for subtheme in subthemes_data:
            subtheme['tema_id'] = theme_id
            subtheme['tema_nome'] = theme_name

        return subthemes_data
    
    def pipeline(self, service_theme_df:pd.DataFrame)->pd.DataFrame:

        all_subthemes = []

        for _, row in service_theme_df.iterrows():

            theme_id = row['theme_id']
            theme_name = row['theme_name']

            subthemes_data = self.parse_all_subthemes_by_theme(theme_name, theme_id)

            all_subthemes.extend(subthemes_data)
        
        subthemes_df = pd.DataFrame(all_subthemes)

        return subthemes_df
    

    def __call__(self, service_theme_df:pd.DataFrame)->pd.DataFrame:
        
        return self.pipeline(service_theme_df)
