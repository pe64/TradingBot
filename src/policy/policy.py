import json
from locale import currency

from policy.martin import Martin
from policy.balance import Balance
from policy.gerd import Gerd
from policy.autobuy import AutoBuy
from policy.open import OpenPst

class Policy:
    def __init__(self, js, cta) -> None:
        #self.police = []
        #js = {}
        #with open(conf_path, "r") as f:
        #    line = f.read()
        #    js = json.loads(line)
        #js = cta.get_policy_config()
        self.name = ""
        if js["type"] == "autobuy":
            self.policy = AutoBuy(js, cta)
        elif js["type"] == "balance":
            self.policy = Balance(js, cta)
        elif js["type"] == "gerd":
            self.policy = Gerd(js, cta)
            self.name = "平衡策略"
        elif js["type"] == "martin":
            self.policy = Martin(js, cta)
            self.name = "马丁策略"
        elif js["type"] == "open":
            self.policy = OpenPst(js, cta)
            self.name = "低吸建仓"

    def get_policy_id(self):
        return int(self.policy.id)

    def add_asset_count(self, asset_count):
        self.policy.asset_count = self.policy.asset_count + float(asset_count)
        return self.policy.asset_count
    
    def add_cash_into(self, cash):
        self.policy.cash_into = self.policy.cash_into + float(cash)
        return self.policy.cash_into

    def execute(self, para):
        self.policy.execute(para)
     
    def policy_status(self):
        return self.policy.policy_status()
                
