from utils.time_format import TimeFormat

class AutoBuy:
    def __init__(self, js) -> None:
        self.policy_id = js["id"]
        self.asset_id = js["asset_id"]
        self.cash = float(js["cash"])
        self.asset_count = js["asset_count"]
        self.condition = js['condition']
        self.execute_time = js['execute_time']
        self.period = js['condition']['period']
        self.timestamp = js['timestamp']
        #self.buy_counts = js["buy_count"]
        #self.percent = js["percent"]
        #self.aver_charge = 0.0
        #self.start_charge = 0.0
        #self.start_amount = self.cash
        #self.next_buy_charge = None
        #self.cta = cta
        #self.current_amount = self.cash
        #self.current_earn_percent = 0.0
        #self.current_into = 0.0
        #self.current_asset_percent = 0.0
        #self.current_asset_value = 0.0

    #def asset_init(self, code, start_charge):
    #    self.current_amount = (start_charge * self.asset_count[0]) + self.cash
    #    self.next_exe_charge = start_charge * (1 - self.percent)
    #    self.start_charge = start_charge
    #    self.start_amount = self.current_amount
    #    pass

    #def update_asset(self, current_charge):
    #    self.current_amount = current_charge * self.asset_count + self.cash
    #    self.current_earn_percent = (self.current_amount - self.start_amount) / self.start_amount
    #    self.current_asset_value = int(self.asset_count * current_charge)*100/100
    #    if self.current_into != 0:
    #        self.current_asset_percent = (self.current_asset_value - self.current_into) / self.current_into
    #        self.deg_charge = self.current_into / self.asset_count

    def check_buy_condition(self, cur, close, cash, buy_count, 
                cur_timestamp, last_timestamp, period):

        timedelta = TimeFormat.get_time_delta(period)
        timediff = TimeFormat.calculate_time_difference(last_timestamp, cur_timestamp)
        timerange = TimeFormat.is_within_configured_time(self.execute_time, cur_timestamp)
        return cur < close and cash > buy_count and timediff > timedelta and timerange 

    def execute(self, charge):

        if self.check_buy_condition(
            charge['cur'], 
            charge['close'], 
            self.cash, 
            self.condition['count'], 
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
        policy = {
            'id': self.policy_id,
            'cash_inuse': self.cash_inuse,
            'cash': self.cash - trade_back['balance'],
            'asset_count': self.asset_count + trade_back['asset_count'],
            'timestamp': self.timestamp
        }
        return policy
    #def policy_status(self):
    #    dic = {
    #        "id": self.asset_ids,
    #        "策略类型": self.type,
    #        "当前总资产": int(self.current_amount * 100) / 100,
    #        "剩余现金": int(self.cash * 100) / 100,
    #        "当前资产价值": self.current_asset_value,
    #        "策略总投入": int(self.current_into * 100)/ 100,
    #        "当前持仓数量": self.asset_count,
    #        "当前策略收益": str(int(self.current_earn_percent*10000) / 100) + "%",
    #        "当前投入收益": str(int(self.current_asset_percent * 10000) / 100) + "%",
    #        "持仓成本": str(int(self.deg_charge) * 100 / 100)
    #    }
    #    return dic