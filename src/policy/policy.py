import json
import threading

from redis_opt.redis import Redis
from locale import currency

from db.policy_db import PolicyDB
from policy.martin import Martin
from policy.balance import Balance
from policy.gerd import Gerd
from policy.autobuy import AutoBuy
from policy.open import OpenPst
from policy.bond import Bond

class Policy:
    def __init__(self, config) -> None:
        self.policy_db = PolicyDB(config["db_path"]["policy"])
        self.policies = self.pdb.get_policys()
        self.redis_client = Redis(config)
        self.threads = []
    
    def create_policy_instance(self, policy_config):
        policy_type = policy_config["type"]
        if policy_type == "autobuy":
            return AutoBuy(policy_config)
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
        for policy_config in self.policys:
            policy_instance = self.create_policy_instance(policy_config)
            policy_thread = threading.Thread(target=self.run_policy, args=(policy_instance,))
            self.threads.append(policy_thread)
            policy_thread.start()

    def run_policy(self, policy):
       asset_id = policy.asset_id

       while True:
            self.rd.PSubscribe(asset_id, policy, callback=self.charge_callback)

    def charge_callback(self, channel, charge, exe_policy):
        para = {}
        popt = exe_policy.execult(charge)
        if popt == None:
            return
        elif popt['opt'] == "BUY":
            self.rd.LPush("left:" + exe_policy.account_id, para)
            ret_opt = self.rd.BRPop("right" + exe_policy.acount_id)
        elif popt['opt'] == "SALE":
            self.rd.LPush("left" + exe_policy.account_id, para)
            ret_opt = self.rd.BRPop("right:" + exe_policy.acount_id)

        pass