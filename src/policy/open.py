import json
from db.em_sqlite import SqliteEM

class OpenPst:
    def __init__(self, js, cta) -> None:
        self.id = js['id']
        self.account_id = js['account_id']
        self.asset_id = js['asset_id']
        self.cash = float(js["cash"])
        para = json.loads(js['para'])
        self.buy_count = float(para["buy_count"])
        self.percent = float(para['percent'])
        self.period = para['period']
        self.pause = float(para['pause_percent'])
        self.hold = float(para['hold'])
        self.cash_into = float(js['cash_into'])
        self.cash_inuse = float(js['cash_inuse'])
        self.asset_count = float(js['asset_count'])
        self.date = js['date']
        self.cta = cta
        pass
    
    def check_buy_condition(self, percent, today, earn):
        return int(self.date) < int(today) and \
                percent < self.percent * 100 and \
                earn <= self.pause * 100 and \
                self.cash > self.buy_count

    def check_sale_condition(self, earn):
        return earn > self.hold * 100

    def execute(self, code, current_charge, percent, today):
        if code not in self.asset_id:
            return
        
        para = {}
        earn = 0
        if self.cash_into > 0:
            earn = round((self.asset_count * float(current_charge) - self.cash_into)/self.cash_into*100,4)

        if self.check_buy_condition(percent, today, earn):
            para = {
                "policy_id": self.id,
                "account_id": self.account_id,
                "code": code,
                "buy_count":self.buy_count,
                "price": current_charge
            }
            ret, free_cash, vol = self.cta.buy_asset(para)
            if ret is True:
                self.cash_inuse = self.cash_inuse + self.buy_count - free_cash
                self.cash = self.cash - self.buy_count + free_cash
                self.asset_count = self.asset_count + vol
                self.date = today
                self.cta.update_policy_status(self.id, self.cash_inuse, self.cash, self.asset_count, today)
        elif self.check_sale_condition(earn):
            para ={
                "policy_id": self.id,
                "account_id": self.account_id,
                "code": code,
                "asset_count": self.asset_count,
                "vol": self.asset_count,
                "price": current_charge
            }
            ret = self.cta.sale_asset(para)
            if ret is True:
                self.cash_inuse = self.cash_inuse - self.cash_into
                self.cash_into = 0
                self.cash = self.asset_count * float(current_charge) + self.cash
                self.asset_count = 0
                self.cta.update_policy_status(self.id, self.cash_inuse, self.cash, self.asset_count, today)
            pass