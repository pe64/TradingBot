import requests
import hashlib
import hmac
import time

class BinanceOpt:
    def __init__(self, cf):
        self.gconf = cf["binance"]
        self.proxies = {
            "http": self.gconf['http_proxy'],
            "https": self.gconf['https_proxy']
        }
        pass

    def get_kline_data(self, symbol, interval, start_time, end_time, limit=1):
        ret = {}
        
        params_kline = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
    
        try:
            response = requests.get(self.gconf['url'] + self.gconf['kline'], params=params_kline, proxies=self.proxies)
    
            kline_data = response.json()
            if len(kline_data) > 0:
                ret["symbol"] = symbol
                ret["name"] = symbol
                ret["open"] = kline_data[0][1]
                ret["close"]= kline_data[0][4]
                ret["cur"]= kline_data[0][4]
                ret["high"] = kline_data[0][2]
                ret["low"] = kline_data[0][3]
                ret["volume"]= kline_data[0][5]
                
            params_price = {
                "symbol": symbol
            }
            response = requests.get(self.gconf['url'] + self.gconf['price'], params=params_price, proxies=self.proxies)
            price_data = response.json()
            if len(price_data) > 0:
                ret["cur"] = price_data["price"]
        except :
            return None
        return ret

    def get_signature(self, query_params, api_secret):

        query_string = '&'.join([f"{k}={v}" for k, v in query_params.items()])
        sig = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        query_params['signature'] = sig
        return query_params

    def get_user_asset(self, api_key, api_secret):
        url = self.gconf['url'] + \
            self.gconf['asset']
        query_params = {
            'timestamp': int(time.time() * 1000),
            'recvWindow': 30000
        }
        query_params = self.get_signature(query_params, api_secret)
        headers = {
            'X-MBX-APIKEY': api_key
        }
        response = requests.post(url, headers=headers, data=query_params, proxies=self.proxies)
        if response.status_code == 200:
            data = response.json()
        else:
            return print(response.json())

        return data
    
    def get_earn_asset(self, api_key, api_secret):
        url = self.gconf['url'] + self.gconf['earn_asset']
        query_params = {
            'timestamp': int(time.time() * 1000),
            'recvWindow': 30000,
            'size': 100,  # 每页结果数量，默认为10
        }
        query_params = self.get_signature(query_params, api_secret)
        headers = {
            'X-MBX-APIKEY': api_key
        }

        response = requests.get(
            url, headers=headers, 
            params=query_params, 
            proxies=self.proxies
        )

        if response.status_code == 200:
            data = response.json()
        else:
            return print(response.json())
        
        return data

    def sell_sopt_market(self, symbol, quantity, 
            api_key, api_secret):
        order_payload = {
            "symbol": symbol,
            "side": "SELL",
            "type": "MARKET",
            "quantity": quantity,
            "timestamp": int(time.time() * 1000)
        }
        order_payload = self.get_signature(order_payload,api_secret)
        url = self.gconf['url'] + self.gconf['order']
        headers = {
            'X-MBX-APIKEY': api_key
        }

        response = requests.post(url, headers=headers, data= order_payload, proxies=self.proxies)
        if response.status_code == 200:
            data = response.json()
        else:
            print(data)
            return None
        
        return data
        pass

    def sell_sopt_limit(self, symbol, auantity, account_id):
        pass