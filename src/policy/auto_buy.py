from utils.time_format import TimeFormat

class AutoBuy:
    def __init__(self, js) -> None:
        self.policy_id = js["id"]
        self.asset_id = js["asset_id"]
        self.account_id = js['account_id']
        self.cash = float(js["cash"])
        self.asset_count = float(js["asset_count"])
        self.condition = js['condition']
        self.execute_time = js['execute_time']
        self.period = js['condition']['period']
        self.timestamp = js['timestamp']
        self.cash_inuse = float(js['cash_inuse'])

    def check_buy_condition(self, cur, close, cash, buy_count, 
                cur_timestamp, last_timestamp, period):

        timedelta = TimeFormat.get_time_delta(period)
        timediff = TimeFormat.calculate_time_difference(last_timestamp, cur_timestamp)
        timerange = TimeFormat.is_within_configured_time(self.execute_time, cur_timestamp)
        return cur < close and cash > buy_count and timediff > timedelta and timerange 

    def execute(self, charge):
        buy_count = 0
        if self.condition['type'] == 'cash':
            buy_count = self.condition['count']
        else:
            buy_count = self.condition['count'] * charge['cur']

        if self.check_buy_condition(
            charge['cur'], 
            charge['close'], 
            self.cash, 
            buy_count, 
            charge['timestamp'], 
            self.timestamp,
            self.period
        ) is False:
            return None
        
        ret = {
            'symbol': charge['symbol'],
            'type': self.condition['type'],
            'trade': "BUY",
            'price': charge['cur'],
            'quantity': self.condition['count']
        }

        return ret

    def after_trade(self, trade_back):

        if trade_back['status'] != "FILLED":
            return None

        self.timestamp = trade_back['timestamp']
        self.cash_inuse = self.cash_inuse + float(trade_back['cummulativeQuoteQty'])
        self.cash = self.cash - float(trade_back['cummulativeQuoteQty'])
        self.asset_count = self.asset_count + float(trade_back['executedQty'])

        policy = {
            'id': self.policy_id,
            'cash_inuse': self.cash_inuse,
            'cash': self.cash,
            'asset_count': self.asset_count, 
            'timestamp': self.timestamp
        }

        return policy