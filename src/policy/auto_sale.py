import json

class AutoSale:
    def __init__(self, policy_config) -> None:
        self.policy_id = policy_config['id']
        self.cash_inuse = policy_config['cash_inuse']
        self.cash = policy_config['cash']
        self.asset_id = policy_config['asset_id']
        self.account_id = policy_config['account_id']
        self.period = policy_config['condition']['period']
        self.asset_count = float(policy_config['asset_count'])
        self.condition = policy_config['condition']
        self.timestamp = policy_config['timestamp']

    @staticmethod
    def check_sell_condition(close, cur, asset_count, sell_count):
        return cur > close and asset_count > sell_count
    
    def execult(self, charge):
        if self.check_sell_condition(
                float(charge['close']), 
                float(charge['cur']), 
                self.asset_count, 
                self.condition['count']
            ) is False:
            return None

        ret = {
            'symbol': charge['symbol'],
            'type': self.condition['type'],
            "trade": "SELL",
            "price": charge['cur'],
            'quantity': self.condition['count']
        }
        return ret
    
    def after_trade(self, trade_back):
        policy = {
            "id": self.policy_id,
            "cash_inuse": self.cash_inuse,
            "cash": self.cash,
            "asset_count":self.asset_count,
            "timestamp": self.timestamp
        }

        return policy