import json
class Balance:
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
        self.act_percent = float(para['act_percent'])
        self.period = int(para['period'])

        self.cta = cta
        self.max_amount = self.cash
        self.min_amount = self.cash

    def balance_asset(self, id, current_charge):
        amount = 0
        for value in self.current_asset_value:
            amount = amount + value

        self.current_amount = amount + self.cash
        if self.start_amount == 0:
            self.start_amount = self.current_amount

        current_value = self.current_asset_value[id]
        balance_value = self.asset_percent[id] * self.current_amount
        diff_value = self.current_amount * self.percent
        need_value = balance_value - current_value 
        if abs(need_value) > diff_value:
            if need_value > 0:
                stock,money = self.cta.buy_asset(self.asset_ids[id], need_value, current_charge)
                self.asset_count[id] = self.asset_count[id] + stock
                self.cash = self.cash - (need_value - money)
            else:
                asset_num = int(abs(need_value) / current_charge) * 1000 /1000
                sell_num, money = self.cta.sell_asset(self.asset_ids[id], asset_num, current_charge)
                self.asset_count[id] = self.asset_count[id] - asset_num + sell_num
                self.cash = self.cash + money

            self.current_asset_value[id] = int(current_charge * self.asset_count[id])*100/100

    def execute(self, code, current_charge, percent, today):
        if code not in self.asset_id or int(today) < self.date + self.period:
            return 

        amount = round(current_charge * self.asset_count + self.cash, 3)
        asset_charge = round(current_charge * self.asset_count,3)
        asset_need = round(amount * self.percent, 3)
        diff_charge = round(asset_charge - asset_need,3)
        diff_percent = round(diff_charge/amount,4)
        if diff_percent > self.act_percent:
            para = {
                "policy_id": self.id,
                "account_id": self.account_id,
                "code":code,
                "asset_count":self.asset_count,
                "vol":round(diff_charge/current_charge,2),
                "price": current_charge,
                "percent": percent
            }
            ret, money, asset = self.cta.sale_asset(para)
            if ret is True:
                self.cash = money + self.cash
                self.cash_inuse = self.cash_inuse - money
                if self.cash_inuse < 0:
                    self.cash_inuse = 0
                self.cash_into = self.cash_into - money
                if self.cash_into < 0:
                    self.cash_into
                self.asset_count = self.asset_count - para['vol'] + asset
                self.date = int(today)
                if self.cash_inuse < 0:
                    self.cash_inuse = 0

                self.cta.update_policy_status(self.id, self.cash_inuse, self.cash, self.asset_count, today, current_charge)
            
        elif diff_percent < 0 - self.act_percent:
            para = {
                "policy_id":self.id,
                "account_id": self.account_id,
                "code": code,
                "buy_count":abs(diff_charge),
                "price":current_charge,
                "percent": percent,
                "policy":self
            }
            (ret, money_num, asset_num) = self.cta.buy_asset(para)
            if ret is True:
                self.cash = self.cash - para['buy_count'] + money_num
                self.asset_count = asset_num + self.asset_count
                self.cash_inuse = self.cash_inuse + abs(diff_charge) - money_num
                self.date = int(today)
                self.cta.update_policy_status(self.id, self.cash_inuse, self.cash, self.asset_count, today, current_charge)
            pass
        self.update_policy_status(current_charge)

    def update_policy_status(self, current_charge):
        self.current_amount = round(self.asset_count * current_charge, 2) + self.cash
        self.max_amount = round(max(self.max_amount, self.current_amount),2)
        self.min_amount = round(min(self.min_amount, self.current_amount),2)
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
        
    def policy_status(self):
        dic = {
            #"id": self.asset_ids,
            "策略类型": "动态平衡策略",
            "当前总资产": int(self.current_amount * 100) / 100,
            "总资产最高值": self.max_amount,
            "总资产最低值": self.min_amount,
            "剩余现金": int(self.cash * 100) / 100,
            "当前资产价值": self.current_asset_value,
            "策略总投入": int(self.cash_into * 100)/ 100,
            "当前持仓数量": self.asset_count,
            "当前策略收益": str(int(self.current_earn_percent*10000) / 100) + "%",
            "当前持仓收益": str(int(self.current_asset_percent * 10000) / 100) + "%",
            "持仓成本": str(int(self.deg_charge) * 100 / 100)
        }
        return dic    