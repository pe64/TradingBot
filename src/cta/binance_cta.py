import json

from redis_opt.redis import Redis
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

    def get_binance_accounts(self):
        return len(self.accounts)
    
    def binance_account_run(self, ids):
        self.accounts[ids]['id']
        message = self.redis_client.BRPop("left#trade#" + self.accounts[ids]['id'], 0)
        order = json.loads(message)
        if order['option'] == "SELL":
            self.sell_asset(order)
        elif order['option'] == "BUY":
            self.buy_asset(order) 
    
    def sell_asset(self, order):
        pass

    def buy_asset(self, order):
        pass

    def update_account(self, account_id):
        self.bn.get_user_asset(
            self.accounts["account_" + str(account_id)]['API_KEY'], 
            self.accounts['account_' + str(account_id)]['API_SECRET'])
        pass

    

    