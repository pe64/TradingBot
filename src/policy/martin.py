import json

class Martin:
    def __init__(self, js, cta) -> None:
        self.id = js["id"]
        self.account_id = js['account_id']
        self.asset_id = js["asset_id"]
        self.cash = float(js["cash"])
        self.asset_count = float(js["asset_count"])
        self.cash_inuse = float(js['cash_inuse'])
        self.cash_into = float(js['cash_into'])
        self.date = int(js['date'])

        para = json.loads(js['para'])
        self.percent = float(para["percent"])
        self.next_exe_charge = float(js['price']) * (1 - self.percent)
        self.period = int(para['period'])
        #self.asset_percent = js['asset_percent']
        self.buy_count = float(para["buy_count"])
        self.sell_percent = float(para["sale_percent"])
        self.buy_percent = float(self.buy_count / self.cash)
        self.current_into = 0.0
        self.current_asset_percent = 0.0
        self.cta = cta
        self.deg_charge = 0.0
        self.max_amount = self.cash
        self.min_amount = self.cash
        self.last_charge = 0.0
        self.current_amount = 0.0
        self.current_asset_value = 0
        self.current_earn_percent = 0
        pass

    def asset_init(self, code, start_charge):
        self.current_amount = round(start_charge * self.asset_count, 3) + self.cash
        self.next_exe_charge = round(start_charge * (1 - self.percent), 3)
        self.start_charge = start_charge
        self.start_amount = self.current_amount

    def update_asset(self, current_charge):
        self.current_amount = round(current_charge * self.asset_count + self.cash, 3)
        self.current_earn_percent = round((self.current_amount - self.start_amount) / self.start_amount,3)
        self.current_asset_value = round(self.asset_count * current_charge, 3)
        if self.current_into != 0 and self.asset_count != 0:
            self.current_asset_percent = (self.current_asset_value - self.current_into) / self.current_into
            self.deg_charge = round(self.current_into / self.asset_count, 3)

        self.max_amount = max(self.max_amount, self.current_amount)
        self.min_amount = min(self.min_amount, self.current_amount)

    #def execute(self, code, current_charge, percent, date):
    def execute(self, args):
        code = args['code']
        current_charge = args['price']
        percent = args['percent']
        date = args['today']
        if code not in self.asset_id or self.date + self.period > int(date):
            return 

        #if self.start_charge is None:
        #    self.asset_init(code, current_charge)
        
        if float(current_charge) < self.next_exe_charge and self.cash > self.buy_count:
            para = {
                "policy_id": self.id,
                "account_id": self.account_id,
                "code": code,
                "buy_count": self.buy_count,
                "price": current_charge,
                "percent": percent,
                "policy": self,
            }
            (ret, money_num, asset_num) = self.cta.buy_asset(para)
            if ret is True:
                self.next_exe_charge = round(current_charge * (1 - self.percent), 3)
                self.cash = self.cash - self.buy_count + money_num
                self.asset_count = asset_num + self.asset_count
                #self.current_into = self.current_into + self.buy_counts - money_num
                self.cash_inuse = self.cash_inuse + self.buy_count - money_num
                self.date = int(date)
                self.cta.update_policy_status(self.id, self.cash_inuse, self.cash, self.asset_count, date, current_charge)

        if self.cash_into > 0:
            self.current_asset_percent = round((self.asset_count*current_charge - self.cash_into) / self.cash_into, 3)

        if self.sell_percent < self.current_asset_percent and self.asset_count != 0:
            para ={
                "policy_id": self.id,
                "account_id": self.account_id,
                "code": code,
                "asset_count": self.asset_count,
                "vol": self.asset_count,
                "price": current_charge,
                "percent": percent,
                "policy": self
            } 
            ret, money, asset = self.cta.sale_asset(para)
            if ret is True:
                self.next_exe_charge = round(current_charge * (1 - self.percent),3)
                self.cash = money + self.cash
                self.cash_inuse = self.cash_inuse - money
                self.cash_into = self.cash_into - money
                if self.cash_into < 0:
                    self.cash_into = 0
                if self.cash_inuse < 0:
                    self.cash_inuse = 0
                
                self.asset_count = asset
                self.date = int(date)
                if self.cash_inuse < 0:
                    self.cash_inuse = 0

                self.cta.update_policy_status(self.id, self.cash_inuse, self.cash, self.asset_count, date, current_charge)
            

        self.update_policy_status(current_charge)
    
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
            self.deg_charge = round(self.cash_into/self.asset_count, 4)
        
        pass

    def policy_status(self):
        dic = {
            #"id": self.asset_ids,
            "策略类型": "马丁格尔策略",
            "当前总资产": round(self.current_amount, 2),
            "总资产最高值": round(self.max_amount,2),
            "总资产最低值": round(self.min_amount, 2),
            "剩余现金": int(self.cash * 100) / 100,
            "当前资产价值": self.current_asset_value,
            "策略总投入": int(self.cash_into * 100)/ 100,
            "当前持仓数量": self.asset_count,
            "当前策略收益": str(int(self.current_earn_percent*10000) / 100) + "%",
            "当前持仓收益": str(int(self.current_asset_percent * 10000) / 100) + "%",
            "持仓成本": str(self.deg_charge)
        }
        return dic