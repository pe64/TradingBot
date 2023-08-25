import requests

class BinanceOpt:
    def __init__(self, cf):
        self.gconf = cf["binance"]
        pass

    def get_kline_data(self, symbol, interval, start_time, end_time, limit=1):
        endpoint = self.gconf['kline']
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
         # 设置代理
        proxies = {
            "http": self.gconf['http_proxy'],
            "https": self.gconf['https_proxy']
        }
    
        response = requests.get(self.gconf['url'] + endpoint, params=params, proxies=proxies)
    
        kline_data = response.json()
        if len(kline_data) > 0:
            ret = {
                "code:":symbol,
                "name:":symbol,
                "open": kline_data[0][1],
                "cur": kline_data[0][4],
                "high": kline_data[0][2],
                "low": kline_data[0][3],
                "volume": kline_data[0][5],
            }
    
        return ret
