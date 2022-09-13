import yaml
import time
import json
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
            with open(policy, "r") as f:
                line = f.read()
                js = json.loads(line)
            p = Policy(js, self)
            self.policy.append(p) 

    def buy_asset(self, para):
        if self.type == "stock":
            asset_num = int(para['buy_count'] / para['price']/ 100) * 100 
            money_num = para['buy_count'] - (asset_num * para['price'])
        else :
            asset_num = round(para['buy_count'] / para['price'],3)
            money_num = 0
        if asset_num != 0:
            print("\033[31m[%s]:%s buy asset_num: %s percent:%s charge:￥%s cash: %d \033[0m"% \
            (self.date, para['code'], str(asset_num).center(8), str(para['percent']).center(6), str(para['price']).center(8), para['buy_count']-money_num))
        para['policy'].cash_into = para['policy'].cash_into + para['buy_count'] - money_num
        #para['policy'].asset_count = para['policy'].asset_count + asset_num
        return (True, money_num, asset_num)

    def update_policy_status(self, ids, cash_inuse, cash, asset_count, today,price):
        pass

    def sale_asset(self, para):
        if self.type == "stock":
            sell_num = int(para['vol']/100) * 100
        else:
            sell_num = para['vol']

        money_num = round(sell_num * para['price'], 4)

        free_num = para['vol'] - sell_num
        if money_num != 0:
            print("\033[32m[%s]:%s sell stock_num: %d charge:￥%s cash: %d \033[0m"%(self.date,para['code'], sell_num, para['price'], money_num))

        return True, money_num, free_num

    def cta_run(self):
        self.date = self.start_time 
        ts = time.strptime(self.date, "%Y-%m-%d")
        ts_end = time.strptime(self.end_time, "%Y-%m-%d")
        while(ts < ts_end):
            for code in self.assets:
                if self.type == "stock":
                    charge, percent = self.sqlite.get_stock_history_charge_by_date(code, self.date)
                else:
                    charge, percent = self.sqlite.get_fund_history_charge_by_date(code, self.date)

                if charge is None or percent is None:
                    continue

                for p in self.policy:
                    if charge is None:
                        break

                    p.execute(code, charge, percent, self.date.replace("-",""))

            self.date = time_next_day(self.date)
            ts = time.strptime(self.date, "%Y-%m-%d")

        for p in self.policy:
            ret = p.policy_status()
            print(ret)

        return 
    
    def get_start_charge(self):
        return self.charge_list[0]