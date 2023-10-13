import json
import random
import time

from utils.redis import Redis
from db.account_db import AccountDB
from http_opt.binance_http import BinanceOpt

class BinanceCta:
    def __init__(self, config) -> None:
        self.config = config
        self.db = AccountDB(config['sqlite_path'])
        self.bn = BinanceOpt(config)
        self.accounts = {}
        self.accounts_db = self.db.get_binance_accounts()
        #self.redis_client = Redis(config['redis']['url'],config['redis']['port'])
        self.redis_url = config['redis']['url']
        self.redis_port = config['redis']['port']
        redis_client = Redis(self.redis_url, self.redis_port)
        self.exchange_info = {}
        self.virtual_flag = config['virtual']['enabled']
        self.virtual_cash = config['virtual']['cash']

        for account in self.accounts_db:
            self.accounts["account_" + str(account['id'])] = account
            ret = self.update_account(account['id'])
            redis_client.Set("binance#" + str(account['id']), json.dumps(ret))
            redis_client.LTrim("left#trade#" + str(account['id']))
            redis_client.LTrim("right#trade#" + str(account['id']))
        
        info = self.bn.get_exchange_info()

        for symbol_info in info['symbols']:
            if "filters" in symbol_info:
                for filter in symbol_info['filters']:
                    symbol_info[filter['filterType']] = filter
            self.exchange_info[symbol_info['symbol']] = symbol_info
        pass


    def get_accounts(self):
        return self.accounts_db
    
    def virtual_buy_asset(self, price, cash):
        if self.virtual_cash > cash:
            self.virtual_cash = self.virtual_cash - cash
            ret_msg = {
                    "status": "FILLED",
                    "orderId": "VIRTUAL",
                    "origQty": cash / price,
                    "executedQty": cash / price,
                    "cummulativeQuoteQty": cash
            }
        else:
            ret_msg = {
                "status": "EXPIRED"
            }
        return ret_msg
    
    def virtual_sell_asset(self, price, quantity):
        self.virtual_cash = self.virtual_cash + price * quantity
        return {
                    "status": "FILLED",
                    "orderId": "VIRTUAL",
                    "origQty": quantity, 
                    "executedQty": quantity,
                    "cummulativeQuoteQty": quantity * price
            }

    def virtual_trade(self, order, account_id):
        if order['trade'] == "BUY":
            if order['type'] == "cash":
                ret_msg = self.virtual_buy_asset(order['price'], order['quantity'])
            else:
                ret_msg = self.virtual_buy_asset(order['price'], order['quantity'] * order['price'])
        else:
            if order['type'] == "asset":
                ret_msg = self.virtual_sell_asset(order['price'], order['quantity'])
            else:
                ret_msg = self.virtual_sell_asset(order['price'], order['quantity'] / order['price'])
        
        sleep_time = random.randint(0, 30)
        print("action: " + order['trade'] +" " + order['symbol'],"cash: " + str(self.virtual_cash), sleep_time)

        time.sleep(sleep_time)
        return ret_msg
    
    def run(self, account):
        redis_client = Redis(self.redis_url, self.redis_port)
        ret_msg = {"status":"EXPIRED"}
        account_id = account['id']
        while True:
            message = redis_client.BRPop(
                "left#trade#" + 
                str(account_id),
                0
            )
            order = json.loads(message)

            if self.virtual_flag:
                ret_msg = self.virtual_trade(order, account_id)
            elif order['trade'] == "SELL":
                ret_msg = self.sell_sopt_asset(order, account_id)
            elif order['trade'] == "BUY":
                ret_msg = self.buy_sopt_asset(order, account_id) 
            else:
                ret_msg = self.update_account(str(account_id))
                redis_client.Set("binance#" + str(account_id), json.dumps(account))
            
            redis_client.LPush("right#trade#" + str(account_id) + "#" + str(order['policy_id']), json.dumps(ret_msg))
        

    def round_quantity(self, symbol, quantity, price):
        if symbol in self.exchange_info and 'quoteAssetPrecision' in self.exchange_info[symbol]:
            quote_asset_precision = int(self.exchange_info[symbol]['quoteAssetPrecision'])
            original_quantity = quantity / price

            # Check if LOT_SIZE filter exists
            if "LOT_SIZE" in self.exchange_info[symbol]:
                min_qty = float(self.exchange_info[symbol]['LOT_SIZE']['minQty'])
                original_quantity = round(original_quantity / min_qty) * min_qty

            return round(original_quantity, quote_asset_precision), quote_asset_precision

        return None   

    def sell_sopt_asset(self, order, account_id):
        ret_msg = {"status":"EXPIRED"}
        api_key = self.accounts["account_" + str(account_id)]['API_KEY']
        api_secret = self.accounts["account_" + str(account_id)]['API_SECRET']
        if order['type'] == "asset":
            order_msg = self.bn.sell_market_order(
                order['symbol'], 
                order['quantity'], 
                api_key, 
                api_secret
            )
        elif order['type'] == 'cash':
            quantity, pcs = self.round_quantity(order['symbol'], order['quantity'], order['price'])
            order_msg = self.bn.sell_limit_order(
                order['symbol'], 
                quantity, 
                float(order['price']),
                api_key, 
                api_secret
            )
        
        if order_msg is not None:
            ret_msg = {
                "status": order_msg['status'],
                "orderId": order_msg['orderId'],
                "origQty": order_msg['origQty'],
                "executedQty": order_msg['executedQty'],
                "cummulativeQuoteQty": order_msg['cummulativeQuoteQty']
            }

        return ret_msg

    def buy_sopt_asset(self, order, account_id):
        ret_msg = {"status":"EXPIRED"}
        api_key = self.accounts['account_' + str(account_id)]['API_KEY']
        api_secret = self.accounts['account_' + str(account_id)]['API_SECRET']
        if order['type'] == "asset":
            order_msg = self.bn.buy_market_order(
                order['symbol'],
                order['quantity'],
                api_key,
                api_secret
            )
        elif order['type'] == 'cash':
            quantity, pcs = self.round_quantity(order['symbol'], order['quantity'], order['price'])
            price = "{:.{}f}".format(order['price'], pcs)
            order_msg = self.bn.buy_limit_order(
                order['symbol'],
                quantity,
                price,
                api_key,
                api_secret
            )
        if order_msg is not None:
            ret_msg = {
                "status": order_msg['status'],
                "orderId": order_msg['orderId'],
                "origQty": order_msg['origQty'],
                "executedQty": order_msg['executedQty'],
                "cummulativeQuoteQty": order_msg['cummulativeQuoteQty']
            }

        return ret_msg
    def buy_feature_asset(self, order):
        pass
    
    def sell_feature_asset(self, order):
        pass

    def update_account(self, account_id):
        account = {
            "coin": {},
            "earn": {},
        }
        message = self.bn.get_user_asset(
            self.accounts["account_" + str(account_id)]['API_KEY'], 
            self.accounts['account_' + str(account_id)]['API_SECRET'])

        if message is not None:
            for msg in message:
                account['coin'][msg['asset']] = {
                    "count" : msg['free']
                }

        message = self.bn.get_earn_asset(
            self.accounts["account_" + str(account_id)]['API_KEY'], 
            self.accounts['account_' + str(account_id)]['API_SECRET'])
        if message is not None and message['total'] > 0:
            for msg in message['rows']:
                account['earn'][msg['asset']] = {
                    "count":msg['totalAmount'],
                    "productId": msg['productId'],
                    "canReem": msg['canRedeem']
                }

        self.accounts['account_' + str(account_id)]['asset'] = account
        return account