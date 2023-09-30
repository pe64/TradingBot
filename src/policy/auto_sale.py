from utils.time_format import TimeFormat

class AutoSale:
    def __init__(self, policy_config) -> None:
        self.policy_id = policy_config['id']
        self.asset_id = policy_config['asset_id']
        self.account_id = policy_config['account_id']
        self.cash = float(policy_config['cash'])
        self.asset_count = float(policy_config['asset_count'])
        self.condition = policy_config['condition']
        self.execute_time = policy_config['execute_time']
        self.period = policy_config['condition']['period']
        self.timestamp = policy_config['timestamp']
        self.cash_inuse = float(policy_config['cash_inuse'])

    def check_sell_condition(self, cur, close, asset_count, sell_count, 
            cur_timestamp, last_timestamp, period):
        
        timedelta = TimeFormat.get_time_delta(period)
        timediff = TimeFormat.calculate_time_difference(last_timestamp, cur_timestamp)
        timerange = TimeFormat.is_within_configured_time(self.execute_time, cur_timestamp)
        return cur > close and asset_count > sell_count and timerange and timediff > timedelta 
    
    def execute(self, charge):
        ret = []
        sell_count = 0
        if self.condition['type'] == 'asset':
            sell_count = self.condition['count']
        else :
            sell_count = self.condition['count'] / charge['cur']

        if self.check_sell_condition(
                float(charge['cur']), 
                float(charge['close']), 
                self.asset_count,
                sell_count,
                charge['timestamp'],
                self.timestamp,
                self.period
            ) is False:
            return None

        ret.append({
            'symbol': charge['symbol'],
            'type': self.condition['type'],
            "trade": "SELL",
            "price": charge['cur'],
            'quantity': self.condition['count']
        })
        return ret
    
    def after_trade(self, trade_back):

        if trade_back['status'] != 'FILLED':
            return None

        self.timestamp = trade_back['timestamp']
        self.cash_inuse = self.cash_inuse - float(trade_back['cummulativeQuoteQty'])
        self.cash = self.cash + float(trade_back['cummulativeQuoteQty'])
        self.asset_count = self.asset_count - float(trade_back['executedQty'])

        policy = {
            "id": self.policy_id,
            "cash_inuse": self.cash_inuse,
            "cash": self.cash,
            "asset_count":self.asset_count,
            "timestamp": self.timestamp
        }

        return policy