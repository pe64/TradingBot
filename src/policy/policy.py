import json
import threading

from utils.redis import Redis
from utils.time_format import TimeFormat
from locale import currency

from db.policy_db import PolicyDB
from db.asset_db import AssetDB

from policy.martin import Martin
from policy.balance import Balance
from policy.gerd import Gerd
from policy.auto_buy import AutoBuy
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

    def run_policy(self, policy):
        subscribe_key = ""
        asset_str = self.redis_client.GetAssetById(policy.asset_id)

        asset = json.loads(asset_str)
        if asset['type'] == "coin":
            subscribe_key = asset['type'] + "#" + \
                            asset['market'] + "#" + \
                            policy.period + "#" + \
                            asset['symbol']
        else:
            subscribe_key = asset['type'] + "#" + \
                            policy.period + '#' + \
                            asset['symbol']
        while True:
            self.redis_client.PSubscribe(
                subscribe_key, 
                policy, 
                callback=self.charge_callback
            )

    def charge_callback(self, channel, charge, exe_policy):

        trade_message = exe_policy.execute(json.loads(charge))
        if trade_message is None:
            return
        trade_message['policy_id'] = exe_policy.policy_id
        trade_message['asset_id'] = exe_policy.asset_id
        self.redis_client.Publish("left#trade#" + str(exe_policy.account_id), json.dumps(trade_message))
        back = self.redis_client.BRPop("right#trade#" + str(exe_policy.account_id) + "#" + str(exe_policy.policy_id), 120)
        if back is None:
            return 
        
        trade_back = json.loads(back)
        trade_back['timestamp'] = TimeFormat.get_current_timestamp_format()
        policy_change = exe_policy.after_trade(trade_back)
        if policy_change is None:
            return

        self.redis_client.LPush("policy#database", json.dumps(policy_change))
    
    def monit_database(self):
        while True:
            policy_change = self.redis_client.BRPop("policy#database", 0)
            if policy_change is None:
                continue

            policy = json.loads(policy_change)
            self.policy_db.update_policy_status(
                policy['id'], 
                policy['cash_inuse'], 
                policy['cash'], 
                policy['asset_count'],
                policy['timestamp']
            )
        