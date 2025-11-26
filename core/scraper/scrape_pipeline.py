from .service_theme_list import ServiceThemeListParser
from .subtheme_list import SubthemesByThemeParser
from .service_links_by_subtheme import ServiceLinksBySubthemeParser
from bs4 import BeautifulSoup
import pandas as pd

class ScrapePipeline:

    def __init__(self)->None:

        self.theme_parser = ServiceThemeListParser()
        self.subtheme_parser = SubthemesByThemeParser()
        self.service_links_parser = ServiceLinksBySubthemeParser()

    def __call__(self)->pd.DataFrame:
        
        theme_df = self.theme_parser()
        subtheme_df = self.subtheme_parser(theme_df)
        service_links_df = self.service_links_parser(subtheme_df)

        
        return service_links_df