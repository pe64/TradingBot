import requests

class BinanceOpt:
    def __init__(self, cf):
        self.gconf = cf["binance"]
        pass

    def get_kline_data(self, symbol, interval, start_time, end_time, limit=1):
        ret = {}
        
        params_kline = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
         # 设置代理
        proxies = {
            "http": self.gconf['http_proxy'],
            "https": self.gconf['https_proxy']
        }
    
        response = requests.get(self.gconf['url'] + self.gconf['kline'], params=params_kline, proxies=proxies)
    
        kline_data = response.json()
        if len(kline_data) > 0:
            ret["code:"] = symbol
            ret["name:"] = symbol
            ret["open"] = kline_data[0][1]
            ret["close"]= kline_data[0][4]
            ret["cur"]= kline_data[0][4]
            ret["high"] = kline_data[0][2]
            ret["low"] = kline_data[0][3]
            ret["volume"]= kline_data[0][5]
            
        params_price = {
            "symbol": symbol
        }

        response = requests.get(self.gconf['url'] + self.gconf['price'], params=params_price, proxies=proxies)
        price_data = response.json()
        if len(price_data) > 0:
            ret["cur"] = price_data["price"]

        return ret
