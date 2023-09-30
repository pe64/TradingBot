import json

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
        self.redis_client = Redis(config)
        self.exchange_info = {}

        for account in self.accounts_db:
            self.accounts["account_" + str(account['id'])] = account
            self.update_account(account['id'])
        
        info = self.bn.get_exchange_info()

        for symbol_info in info['symbols']:
            if "filters" in symbol_info:
                for filter in symbol_info['filters']:
                    symbol_info[filter['filterType']] = filter
            self.exchange_info[symbol_info['symbol']] = symbol_info
        pass


    def get_accounts(self):
        return self.accounts_db
    
    def run(self, account):
        account_id = account['id']
        while True:
            message = self.redis_client.BRPop(
                "left#trade#" + 
                str(account_id),
                0
            )
            order = json.loads(message)
            if order['trade'] == "SELL":
                self.sell_sopt_asset(order, account_id)
            elif order['trade'] == "BUY":
                self.buy_sopt_asset(order, account_id) 
            else:
                self.update_account(str(account_id))

    def round_quantity(self, symbol, quantity, price):
        if symbol in self.exchange_info and 'quoteAssetPrecision' in self.exchange_info[symbol]:
            quote_asset_precision = int(self.exchange_info[symbol]['quoteAssetPrecision'])
            original_quantity = quantity / price

            # Check if LOT_SIZE filter exists
            if "LOT_SIZE" in self.exchange_info[symbol]:
                min_qty = float(self.exchange_info[symbol]['LOT_SIZE']['minQty'])
                original_quantity = round(original_quantity / min_qty) * min_qty

            return round(original_quantity, quote_asset_precision)

        return None   

    def sell_sopt_asset(self, order, account_id):
        order_msg = {}
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
            quantity = self.round_quantity(order['symbol'], order['quantity'], order['price'])
            order_msg = self.bn.sell_limit_order(
                order['symbol'], 
                quantity, 
                order['price'],
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
            self.redis_client.LPush("right#trade#" + str(account_id) + "#" + str(order['policy_id']), json.dumps(ret_msg))

    def buy_sopt_asset(self, order, account_id):
        order_msg = {}
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
            quantity = self.round_quantity(order['symbol'], order['quantity'], order['price'])
            order_msg = self.bn.buy_limit_order(
                order['symbol'],
                quantity,
                order['price'],
                api_key,
                api_secret
            )

        ret_msg = {"status":"EXPIRED"}
        push_key = "right#trade#" + str(account_id) + "#" + str(order['policy_id'])

        if order_msg is None:
            self.redis_client.LPush(push_key, json.dumps(ret_msg))
            return

        ret_msg = {
            "status": order_msg['status'],
            "orderId": order_msg['orderId'],
            "origQty": order_msg['origQty'],
            "executedQty": order_msg['executedQty'],
            "cummulativeQuoteQty": order_msg['cummulativeQuoteQty']
        }
        self.redis_client.LPush(push_key, json.dumps(ret_msg))

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
        self.redis_client.Set("binance#" + str(account_id), json.dumps(account))