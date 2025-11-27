from .service_theme_list import ServiceThemeListParser
from .subtheme_list import SubthemesByThemeParser
from .service_links_by_subtheme import ServiceLinksBySubthemeParser
from .service_detail import ServiceDetailParser
from config import DATA_DIR
import os
import pandas as pd

class ScrapePipeline:

    def __init__(self, data_dir:str=DATA_DIR)->None:

        self.theme_parser = ServiceThemeListParser()
        self.subtheme_parser = SubthemesByThemeParser()
        self.service_links_parser = ServiceLinksBySubthemeParser()
        self.service_detail_parser = ServiceDetailParser()

        self.__solve_data_dir(data_dir)
        self.data_dir = data_dir

        self.data_path = os.path.join(self.data_dir, '156_service_data.csv')

    def __solve_data_dir(self, data_dir:str)->None:

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def save_service_data(self, service_data:pd.DataFrame)->None:

        service_data.to_csv(self.data_path, index=False)

    def load_service_data(self)->pd.DataFrame:

        service_data = pd.read_csv(self.data_path)
        return service_data

    def __call__(self)->pd.DataFrame:

        if os.path.exists(self.data_path):
            print('Loading cached service data...')
            service_data = self.load_service_data()
            return service_data
        
        else:
            print('Scraping service data...')
            theme_df = self.theme_parser()
            subtheme_df = self.subtheme_parser(theme_df)
            service_links_df = self.service_links_parser(subtheme_df)
            service_links_df['description'] = service_links_df['service_id'].apply(self.service_detail_parser)
            self.save_service_data(service_links_df)
            return service_links_df