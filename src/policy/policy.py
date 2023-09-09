import json
import threading

from redis_opt.redis import Redis
from locale import currency

from db.policy_db import PolicyDB
from db.asset_db import AssetDB

from policy.martin import Martin
from policy.balance import Balance
from policy.gerd import Gerd
from policy.autobuy import AutoBuy
from policy.open import OpenPst
from policy.bond import Bond
from policy.auto_sale import AutoSale

class Policy:
    def __init__(self, config) -> None:
        self.policy_db = PolicyDB(config["sqlite_path"])
        self.asset_db = AssetDB(config['sqlite_path'])
        self.policies = self.policy_db.get_policys()
        self.redis_client = Redis(config)
        self.threads = []
    
    def create_policy_instance(self, policy_config):
        policy_type = policy_config["type"]
        if policy_type == "autobuy":
            return AutoBuy(policy_config)
        elif policy_type == "autosale":
            return AutoSale(policy_config)
        elif policy_type == "balance":
            return Balance(policy_config)
        elif policy_type == "gerd":
            return Gerd(policy_config)
        elif policy_type == "martin":
            return Martin(policy_config)
        elif policy_type == "open":
            return OpenPst(policy_config)
        elif policy_type == "bond":
            return Bond(policy_config)
        else:
            raise ValueError(f"Unsupported policy type: {policy_type}")
    
    def run_policies_in_thread(self):
        for policy_config in self.policies:
            policy_instance = self.create_policy_instance(policy_config)
            policy_thread = threading.Thread(target=self.run_policy, args=(policy_instance,))
            self.threads.append(policy_thread)
            policy_thread.start()

    def get_asset_by_id(self, asset_id):
        asset_str = self.redis_client.Get("asset#" + str(asset_id))
        return json.loads(asset_str)

    def run_policy(self, policy):
        subscribe_key = ""
        asset = self.get_asset_by_id(policy.asset_id)
        
        if asset['type'] == "coin":
            subscribe_key = asset['type'] + "#" + asset['market'] + "#8h#" + asset['symbol']
        else:
            subscribe_key = asset['type'] + "#" + asset['symbol']
        while True:
            self.redis_client.PSubscribe(subscribe_key, policy, callback=self.charge_callback)

    def charge_callback(self, channel, charge, exe_policy):

        trade_message = exe_policy.execult(json.loads(charge))
        if trade_message is None:
            return
        
        self.redis_client.LPush("left#trade#" + str(exe_policy.account_id), json.dumps(trade_message))
        trade_back = self.redis_client.BRPop("right#trade#" + str(exe_policy.account_id), 30)

        exe_policy.after_trade(trade_back)
        