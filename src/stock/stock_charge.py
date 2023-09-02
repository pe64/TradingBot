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

                return {
                    "code": code,
                    "name": stock_info[0],
                    "open": float(stock_info[1]),
                    "close": float(stock_info[2]),
                    "cur": float(stock_info[3]),
                    "high": float(stock_info[4]),
                    "low": float(stock_info[5]),
                    "percent": round((float(stock_info[3]) - float(stock_info[2])) / float(stock_info[2]) * 100, 2),
                    "volume": int(stock_info[8]),
                    "timestamp": stock_info[30] + " " + stock_info[31]
                }
            else:
                return None
        except:
            return None