class Gerd():
    def __init__(self, js, cta) -> None:
        self.id = js["id"]
        self.asset_ids = js["asset_id"]
        self.cash = js["cash"]
        self.percent = js["percent"]
        self.start_charge = js["start_charge"]
        self.asset_count = js["asset_count"]
        self.sell_percent = js["sell_percent"]
        self.buy_counts = js["buy_count"]
        self.gerd_sell_charge_list = []
        self.gerd_sell_count_list = []
        self.cta = cta
        self.current_into = 0.0
        self.max_amount = self.cash
        self.min_amount = self.cash
        self.buy_percent = float(self.buy_counts / self.cash)
        self.current_amount = 0.0
        self.current_asset_value = 0
        self.current_earn_percent = 0.0
        self.current_asset_percent = 0.0
        self.deg_charge = 0.0
        pass

    def asset_init(self, start_charge):
        self.current_amount = round(start_charge * self.asset_count + self.cash, 3)
        self.next_exe_charge = round(start_charge * (1 - self.percent), 3)
        self.next_sell_charge = round(start_charge * (1 + self.sell_percent), 3)
        self.start_charge = start_charge
        self.start_amount = self.current_amount
    
    def update_asset(self, current_charge):
        self.current_amount = round(current_charge * self.asset_count + self.cash, 3)
        self.current_earn_percent = round((self.current_amount - self.start_amount) / self.start_amount, 3)
        self.current_asset_value = round(self.asset_count * current_charge, 3)
        if self.current_into != 0:
            self.current_asset_percent = (self.current_asset_value - self.current_into) / self.current_into
            self.deg_charge = round(self.current_into / self.asset_count, 3)
        
        self.max_amount = max(self.max_amount, self.current_amount)
        self.min_amount = min(self.min_amount, self.current_amount)
        
    def execute(self, code, current_charge, percent):
        if code not in self.asset_ids:
            return 

        if self.start_charge is None:
            self.asset_init(current_charge)
        
        if current_charge < self.next_exe_charge and self.cash > self.buy_counts:
            (asset_num, money_num) = self.cta.buy_asset(self.asset_ids[0], 
                    self.buy_counts, current_charge)
            self.gerd_sell_charge_list.append(self.next_sell_charge)
            self.next_sell_charge = round(current_charge * (1 + self.sell_percent), 3)
            self.gerd_sell_count_list.append(asset_num)
            self.next_exe_charge = round(current_charge * (1 - self.percent), 3)
            self.cash = self.cash - self.buy_counts + money_num
            self.asset_count = round(asset_num + self.asset_count, 4)
            self.current_into = self.current_into + self.buy_counts - money_num
    
        if self.current_into != 0:
            self.current_asset_percent = (self.current_asset_value - self.current_into) / self.current_into
        if self.asset_count == 0 :
            if current_charge * (1 - self.percent) > self.next_exe_charge:
                self.next_exe_charge = round(current_charge * (1 - self.percent))

        if len(self.gerd_sell_count_list) != 0 and  current_charge > self.next_sell_charge:
            sell_num = self.gerd_sell_count_list.pop()
            (asset_num, money_num) = self.cta.sell_asset(self.asset_ids[0],
                sell_num, current_charge)

            if len(self.gerd_sell_charge_list) != 0:
                self.next_sell_charge = self.gerd_sell_charge_list.pop()
            self.next_exe_charge = round(current_charge * (1 - self.percent), 3)
            self.cash = self.cash + money_num
            self.asset_count = round(self.asset_count - sell_num + asset_num, 4)
            self.current_into = self.current_into - money_num
            if self.current_into < 0:
                self.current_into = 0

        self.update_asset(current_charge)

    def policy_status(self):
        dic = {
            #"id": self.asset_ids,
            "策略类型": "网  格  策略",
            "当前总资产": int(self.current_amount * 100) / 100,
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