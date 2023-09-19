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

    def _make_request(self, method, url, headers=None, params=None, data=None):
        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                params=params,
                data=data,
                proxies=self.proxies
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Request failed with status code {response.status_code}")
                return None
        except Exception as e:
            print("Error:", e)
            return None

    def get_request(self, url, params=None):
        return self._make_request("GET", url, params=params)

    def post_request(self, url, headers, data=None):
        return self._make_request("POST", url, headers=headers, data=data)

    def get_kline_data(self, symbol, interval, start_time=None, limit=1):
        ret = {}
        params_kline = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        
        if start_time:
            params_kline["startTime"] = start_time
        
        kline_data = self.get_request(self.gconf['url'] + self.gconf['kline'], params=params_kline)
    
        if kline_data and len(kline_data) > 0:
            ret["symbol"] = symbol
            ret["name"] = symbol
            ret["open"] = float(kline_data[0][1])
            ret["close"]= float(kline_data[0][1])
            ret["cur"]= float(kline_data[0][4])
            ret["high"] = float(kline_data[0][2])
            ret["low"] = float(kline_data[0][3])
            ret["volume"]= kline_data[0][5]
        else:
            return None
                
        params_price = {
            "symbol": symbol
        }
        price_data = self.get_request(self.gconf['url'] + self.gconf['price'], params=params_price)
        
        if price_data and len(price_data) > 0:
            ret["cur"] = float(price_data["price"])
        
        return ret

    def get_signature(self, query_params, api_secret):
        query_string = '&'.join([f"{k}={v}" for k, v in query_params.items()])
        sig = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        query_params['signature'] = sig
        return query_params

    def _make_signed_request(self, method, url, api_key, api_secret, query_params=None, data=None):
        headers = {'X-MBX-APIKEY': api_key}
        
        if query_params:
            query_params = self.get_signature(query_params, api_secret)
        
        if data:
            data = self.get_signature(data, api_secret)
        
        return self._make_request(method, url, headers=headers, params=query_params, data=data)

    def get_user_asset(self, api_key, api_secret):
        url = self.gconf['url'] + self.gconf['asset']
        query_params = {
            'timestamp': int(time.time() * 1000),
            'recvWindow': 30000
        }
        return self._make_signed_request("POST", url, api_key, api_secret, data=query_params)

    def get_earn_asset(self, api_key, api_secret):
        url = self.gconf['url'] + self.gconf['earn_asset']
        query_params = {
            'timestamp': int(time.time() * 1000),
            'recvWindow': 30000,
            'size': 100  # 每页结果数量，默认为10
        }
        return self._make_signed_request("GET", url, api_key, api_secret, query_params=query_params)

    def sell_market_order(self, symbol, quantity, api_key, api_secret):
        order_payload = {
            "symbol": symbol,
            "side": "SELL",
            "type": "MARKET",
            "quantity": quantity,
            "newOrderRespType": "FULL",
            "timestamp": int(time.time() * 1000)
        }
        return self._make_signed_request("POST", self.gconf['url'] + self.gconf['order'], api_key, api_secret, data=order_payload)

    def sell_limit_order(self, symbol, quantity, price, api_key, api_secret):
        order_payload = {
            'symbol': symbol,
            'side': 'SELL',
            'type': 'LIMIT',
            'timeInForce': 'FOK',
            'quantity': quantity,
            'price': price,
            "newOrderRespType": "FULL",
            'timestamp': int(time.time() * 1000)
        }
        return self._make_signed_request("POST", self.gconf['url'] + self.gconf['order'], api_key, api_secret, data=order_payload)

    def buy_limit_order(self, symbol, quantity, price, api_key, api_secret):
        order_payload = {
            'symbol': symbol,
            'side': 'BUY',
            'type': 'LIMIT',
            'timeInForce': 'FOK',
            'quantity': quantity,
            'price': price,
            "newOrderRespType": "FULL",
            'timestamp': int(time.time() * 1000)
        }
        return self._make_signed_request("POST", self.gconf['url'] + self.gconf['order'], api_key, api_secret, data=order_payload)

    def buy_market_order(self, symbol, quantity, api_key, api_secret):
        order_payload = {
            'symbol': symbol,
            'side': 'BUY',
            'type': 'MARKET',
            'quantity': quantity,
            "newOrderRespType": "FULL",
            'timestamp': int(time.time() * 1000)
        }
        return self._make_signed_request("POST", self.gconf['url'] + self.gconf['order'], api_key, api_secret, data=order_payload)
