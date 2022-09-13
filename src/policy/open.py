import json
from db.em_sqlite import SqliteEM

class OpenPst:
    def __init__(self, js, cta) -> None:
        self.id = js['id']
        self.account_id = js['account_id']
        self.asset_id = js['asset_id']
        self.cash = float(js["cash"])
        self.cash_into = float(js['cash_into'])
        self.cash_inuse = float(js['cash_inuse'])
        self.asset_count = float(js['asset_count'])
        self.date = js['date']

        para = json.loads(js['para'])
        self.period = para['period']
        self.buy_count = float(para["buy_count"])
        self.percent = float(para['percent'])
        self.pause = float(para['pause_percent'])
        self.hold = float(para['hold'])
        self.cta = cta

        self.current_amount = 0.0
        self.max_amount = 0.0
        self.min_amount = self.cash + self.cash_inuse
        pass
    
    def check_buy_condition(self, percent, today, earn):
        return int(self.date)+self.period <= int(today) and \
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
                "price": current_charge,
                "percent":percent,
                "policy": self,
            }
            ret, free_cash, vol = self.cta.buy_asset(para)
            if ret is True:
                self.cash_inuse = self.cash_inuse + self.buy_count - free_cash
                self.cash = self.cash - self.buy_count + free_cash
                self.asset_count = self.asset_count + vol
                self.date = today
                self.cta.update_policy_status(self.id, self.cash_inuse, self.cash, self.asset_count, today, current_charge)
        elif self.check_sale_condition(earn):
            para ={
                "policy_id": self.id,
                "account_id": self.account_id,
                "code": code,
                "asset_count": self.asset_count,
                "vol": self.asset_count,
                "price": current_charge,
                "policy": self
            }
            ret = self.cta.sale_asset(para)
            if ret is True:
                self.cash_inuse = self.cash_inuse - self.cash_into
                self.cash_into = 0
                self.cash = round(self.asset_count * float(current_charge),2) + self.cash
                self.asset_count = 0
                self.date = today
                self.cta.update_policy_status(self.id, self.cash_inuse, self.cash, self.asset_count, today, current_charge)
    
        self.update_policy_status(float(current_charge))
    
    def update_policy_status(self, current_charge):
        self.current_amount = round(self.asset_count * current_charge, 2) + self.cash
        self.max_amount = max(self.max_amount, self.current_amount)
        self.min_amount = min(self.min_amount, self.current_amount)
        self.current_asset_value = round(self.asset_count * current_charge)
        self.current_earn_percent = round((self.current_amount - (self.cash + self.cash_inuse)) / (self.cash + self.cash_inuse), 2)
        if self.cash_into == 0 :
            self.current_asset_percent = 0
        else:
            self.current_asset_percent = round((self.asset_count * float(current_charge) - self.cash_into)/self.cash_into, 2)
        if self.asset_count == 0:
            self.deg_charge = 0
        else:
            self.deg_charge = round(self.cash_into/self.asset_count, 2)
        pass
            
    def policy_status(self):
        dic = {
            #"id": self.asset_ids,
            "策略类型": "低吸建仓策略",
            "当前总资产": round(self.current_amount, 2),
            "总资产最高值": round(self.max_amount, 2),
            "总资产最低值": round(self.min_amount, 2),
            "剩余现金": round(self.cash, 2),
            "当前资产价值": self.current_asset_value,
            "策略总投入": round(self.cash_into, 4) ,
            "当前持仓数量": round(self.asset_count,4),
            "当前策略收益": str(int(self.current_earn_percent*10000) / 100) + "%",
            "当前持仓收益": str(int(self.current_asset_percent * 10000) / 100) + "%",
            "持仓成本": str(self.deg_charge)
        }
        return dic