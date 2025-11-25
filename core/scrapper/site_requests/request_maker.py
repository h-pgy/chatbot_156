from requests.sessions import Session
from urllib.parse import urlencode

class RequestMaker:

    def __init__(self, domain:str, base_endpoint:str|None, secure:bool=True)->None:

        self.session = Session()
        self.domain=domain
        self.base_endpoint = base_endpoint or ''
        self.secure = secure
        self.method = self.solve_method()
        self.base_url = self.solve_base_url()

    def solve_method(self)->str:

        if self.secure:
            return 'https'
        return 'http'
    
    def solve_base_url(self)->str:

        return self.method + r'://' + self.domain + '/' + self.base_endpoint
    
    def solve_url(self, endpoint:str|None, query_params:dict|None=None)->str:

        url = self.base_url
        if endpoint:
            url = f"{self.base_url}/{endpoint}"

        if query_params:
            qs = urlencode(query_params, doseq=True)
            url = f"{url}?{qs}"

        return url
    
    def get_html_request(self, endpoint:str, query_params:dict|None=None)->str:

        url = self.solve_url(endpoint, query_params)
        print(f'Getting html for {url}')
        with self.session.get(url) as r:
            return r.text