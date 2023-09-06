import json

class AutoSale:
    def __init__(self, policy_config) -> None:
        self.asset_id = policy_config['asset_id']
        self.account_id = policy_config['account_id']
        pass
    
    def execult(self, charge):
        ret = {
            "trade":"SALE",
            "price":charge['cur']
        }
        return ret
    
    def after_trade(self, trade_back):
        pass