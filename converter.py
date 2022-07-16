from datetime import date
from typing import List
import httpx
import json
from decouple import config

class Converter():
    def __init__(self) -> None:
        self.base_url = "https://api.apilayer.com/exchangerates_data"
        self.api_key = config('API_KEY')

    def get_exchanged_value(self , currency_to: str, currency_from: str, amount_from: float):
        """_summary_
        
        """        
        url = f"{self.base_url}/convert?to={currency_to}&from={currency_from}&amount={amount_from}"
        headers = {"apikey": self.api_key}
        response = httpx.get(url, headers=headers)
        result = response.text
        return result
    
    def get_currencies(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        url = f"{self.base_url}/symbols"
        headers = {
            "apikey": self.api_key
        }        
        response = httpx.get(url, headers=headers)
        result = json.loads(response.text)
        return result
    
    def get_historical_rate(self, url , date:str , base:str,  symbols:List[str]):
        """_summary_

        Args:
            url (_type_): _description_
            date (str): _description_
            symbols (List[str]): _description_
            base (str): _description_

        Returns:
            _type_: _description_
        """
        url = f"{self.base_url}/{date}?symbols={symbols}&base={base}"
        headers= {"apikey": self.api_key}
        response = httpx.get(url, headers=headers)
        status_code = response.status_code
        result = json.loads(response.text)
        return result