import yaml
import time
from db.sqlite import SqliteObj
import datetime
from datetime import datetime as d1
from policy.policy import Policy

def time_next_day(date):
    ret = (d1.strptime(date, "%Y-%m-%d") + 
            datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    return ret

class VirtualCta:
    def __init__(self, cta_path) -> None:
        cta_conf = ''
        self.policy = []
        with open(cta_path, "r") as f:
            line = f.read()
            cta_conf = yaml.load(line, Loader=yaml.FullLoader)
        self.date = ""
        self.start_time = cta_conf["start_date"]
        self.end_time = cta_conf["end_date"]
        self.type = cta_conf["asset_type"]

        if self.type == "stock":
            self.assets = cta_conf["stock_code"]
            self.sqlite = SqliteObj(cta_conf["stock_db"])
        else: 
            self.assets = cta_conf['fund_code']
            self.sqlite = SqliteObj(cta_conf["fund_db"])

        for policy in cta_conf["policy"]:
            p = Policy(policy, self)
            self.policy.append(p) 

    def buy_asset(self, code, cash, charge):
        if self.type == "stock":
            asset_num = int(cash / charge / 100) * 100 
            money_num = cash - (asset_num * charge)
        else :
            asset_num = int(cash / charge * 1000) / 1000
            money_num = 0
        if asset_num != 0:
            print("\033[31m[%s]:%s buy asset_num: %d charge:￥%s cash: %d \033[0m"%(self.date,code, asset_num, charge, cash-money_num))
        return (asset_num, money_num)

    def sell_asset(self, code, asset_num, charge):
        if self.type == "stock":
            sell_num = int(asset_num /100) * 100
        else:
            sell_num = asset_num

        money_num = round(sell_num * charge, 4)

        asset_num = asset_num - sell_num
        if money_num != 0:
            print("\033[32m[%s]:%s sell stock_num: %d charge:￥%s cash: %d \033[0m"%(self.date,code, sell_num, charge, money_num))

        return (asset_num, money_num) 

    def cta_run(self):
        self.date = self.start_time 
        ts = time.strptime(self.date, "%Y-%m-%d")
        ts_end = time.strptime(self.end_time, "%Y-%m-%d")
        while(ts < ts_end):
            for code in self.assets:
                if self.type == "stock":
                    charge = self.sqlite.get_stock_history_charge_by_date(code, self.date)
                else:
                    charge = self.sqlite.get_fund_history_charge_by_date(code, self.date)

                if charge is None:
                    continue

                for p in self.policy:
                    if charge is None:
                        break

                    p.execute(code, charge, 0.0)

            self.date = time_next_day(self.date)
            ts = time.strptime(self.date, "%Y-%m-%d")

        for p in self.policy:
            ret = p.policy_status()
            print(ret)

        return 
    
    def get_start_charge(self):
        return self.charge_list[0]