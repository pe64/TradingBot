import requests

class StockCharge:
    def __init__(self, cf):
        self.gconf = cf['stock']
    
    def get_stock_charge(self, code, market):
        url = self.gconf['url'] + market + code
        headers = {
            "Referer": self.gconf['referer']
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.text.split('"')[1]
                stock_info = data.split(',')

                return stock_info
                
            else:
                return None
        except:
            return None