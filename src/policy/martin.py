import json

class Martin:
    def __init__(self, js, cta) -> None:
        self.id = js["id"]
        self.asset_id = js["asset_id"]
        self.cash = float(js["cash"])
        self.asset_count = float(js["asset_count"])
        self.next_exe_charge = float(js['price'])
        self.cash_inuse = float(js['cash_inuse'])
        self.cash_into = float(js['cash_into'])

        para = json.loads(js['para'])
        self.percent = float(para["percent"])
        #self.asset_percent = js['asset_percent']
        self.buy_counts = float(para["buy_count"])
        self.sell_percent = float(para["sale_percent"])
        self.buy_percent = float(self.buy_counts / self.cash)
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

    def execute(self, code, current_charge, percent, date):
        if code not in self.asset_id:
            return 

        #if self.start_charge is None:
        #    self.asset_init(code, current_charge)
        
        if float(current_charge) < self.next_exe_charge and self.cash > self.buy_counts:
            (ret, money_num, asset_num) = self.cta.buy_asset(self.asset_id[0], 
                    self.buy_counts, current_charge)
            if ret is True:
                self.next_exe_charge = round(current_charge * (1 - self.percent), 3)
                self.cash = self.cash - self.buy_counts + money_num
                self.asset_count = asset_num + self.asset_count
                #self.current_into = self.current_into + self.buy_counts - money_num
                self.cash_inuse = self.cash_inuse + self.buy_counts - money_num
                self.cta.update_policy_status(self.id, self.cash_inuse, self.cash, self.asset_count, date, self.next_exe_charge)
        if self.cash_into > 0:
            self.current_asset_percent = round((self.asset_count*current_charge - self.cash_into) / self.cash_into, 3)

        #if self.asset_count == 0 :
        #    if current_charge * (1 - self.percent) > self.next_exe_charge:
        #        self.next_exe_charge = round(current_charge * (1 - self.percent), 3)

        if self.sell_percent < self.current_asset_percent and self.asset_count != 0:
            (ret,asset_num, money_num) = self.cta.sale_asset(self.asset_ids[0],
                    self.asset_count, current_charge)
            if ret is True:
                self.next_exe_charge = round(current_charge * (1 - self.percent),3)
                self.cash = self.cash + money_num
                self.asset_count = asset_num
                self.cash_inuse = self.cash_inuse - money_num
                if self.cash_inuse < 0:
                    self.cash_inuse = 0

                self.cta.update_policy_status(self.id, self.cash_inuse, self.cash, self.asset_count, date, self.next_exe_charge)
            
            #self.buy_counts = self.cash * self.buy_percent


        #self.update_asset(current_charge)

    def policy_status(self):
        dic = {
            #"id": self.asset_ids,
            "策略类型": "马丁格尔策略",
            "当前总资产": round(self.current_amount, 2),
            "总资产最高值": self.max_amount,
            "总资产最低值": self.min_amount,
            "剩余现金": int(self.cash * 100) / 100,
            "当前资产价值": self.current_asset_value,
            "策略总投入": int(self.current_into * 100)/ 100,
            "当前持仓数量": self.asset_count,
            "当前策略收益": str(int(self.current_earn_percent*10000) / 100) + "%",
            "当前持仓收益": str(int(self.current_asset_percent * 10000) / 100) + "%",
            "持仓成本": str(int(self.deg_charge) * 100 / 100)
        }
        return dic