class Balance:
    def __init__(self, js, cta) -> None:
        self.id = js["id"]
        self.asset_ids = js["asset_id"]
        self.cash = js["cash"]
        self.start_charge = js["start_charge"]
        self.percent = js["percent"]
        self.asset_count = js["asset_count"]
        self.asset_percent = js["asset_percent"]
        self.balance_asset_price = []
        self.current_asset_value = []
        self.cta = cta
        self.current_amount = self.cash
        self.max_amount = self.cash
        self.min_amount = self.cash
        for i in range(len(self.asset_ids)):
            self.balance_asset_price.append(0.0)
            self.current_asset_value.append(0.0)
        
        self.start_amount = self.cash
        self.current_earn_percent = 0.0
        self.current_into = 0.0
        self.current_asset_percent = 0.0
        self.next_sell_charge = 0.0

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

    def execute(self, code, current_charge, percent):
        if code not in self.asset_ids:
            return 
        
        id = self.asset_ids.index(code)
        self.balance_asset_price[id] = current_charge
        self.current_asset_value[id] = int(self.asset_count[id] * current_charge)*100/100
        if 0 not in self.balance_asset_price:
            self.balance_asset(id, current_charge)
            self.current_earn_percent = (self.current_amount - self.start_amount) / self.start_amount

        self.max_amount = max(self.max_amount, self.current_amount)
        self.min_amount = min(self.min_amount, self.current_amount)

    def policy_status(self):
        dic = {
            #"id": self.asset_ids,
            "策略类型": "动态平衡策略",
            "当前总资产": int(self.current_amount * 100) / 100,
            "总资产最高值": self.max_amount,
            "总资产最低值": self.min_amount,
            "剩余现金": int(self.cash * 100) / 100,
            "当前资产价值": self.current_asset_value,
            "策略总投入": int(self.current_into * 100)/ 100,
            "当前持仓数量": self.asset_count,
            "当前策略收益": str(int(self.current_earn_percent*10000) / 100) + "%",
            "当前持仓收益": str(int(self.current_asset_percent * 10000) / 100) + "%",
            #"持仓成本": str(int(self.deg_charge) * 100 / 100)
        }
        return dic    