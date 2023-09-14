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

        for account in self.accounts_db:
            self.accounts["account_" + str(account['id'])] = account
            self.update_account(account['id'])

    def get_binance_accounts_num(self):
        return len(self.accounts)
    
    def binance_account_run(self, ids):
        account_id = self.accounts_db[ids]['id']
        while True:
            _, message = self.redis_client.Subscribe(
                "left#trade#" + 
                str(account_id)
            )
            order = json.loads(message)
            if order['trade'] == "SELL":
                self.sell_sopt_asset(order, account_id)
            elif order['trade'] == "BUY":
                self.buy_sopt_asset(order, account_id) 
            else:
                self.update_account(str(account_id))
    
    def sell_sopt_asset(self, order, account_id):
        api_key = self.accounts["account_" + str(account_id)]['API_KEY']
        api_secret = self.accounts["account_" + str(account_id)]['API_SECRET']
        if order['type'] == "asset":
            self.bn.sell_market_order(
                order['symbol'], 
                order['count'], 
                api_key, 
                api_secret
            )
        elif order['type'] == 'cash':
            self.bn.sell_limit_order(
                order['symbol'], 
                order['count'], 
                order['price'],
                api_key, 
                api_secret
            )
        pass

    def buy_sopt_asset(self, order, account_id):
        api_key = self.accounts['account_' + str(account_id)]['API_KEY']
        api_secret = self.accounts['account_' + str(account_id)]['API_SECRET']
        if order['type'] == "asset":
            self.bn.buy_market_order(
                order['symbol'],
                order['count'],
                api_key,
                api_secret
            )
        elif order['type'] == 'cash':
            self.bn.buy_limit_order(
                order['symbol'],
                order['count'] / order['price'],
                order['price'],
                api_key,
                api_secret
            )
        pass

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