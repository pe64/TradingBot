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
    def __init__(self, db_path, redis_conf) -> None:
        self.policy_db = PolicyDB(db_path)
        self.asset_db = AssetDB(db_path)
        self.policies = self.policy_db.get_policys()
        #self.redis_client = Redis(redis_conf['url'], redis_conf['port'])
        self.redis_url = redis_conf['url']
        self.redis_port = redis_conf['port']
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
        redis_client = Redis(self.redis_url, self.redis_port)
        asset_str = redis_client.GetAssetById(policy.asset_id)
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
            redis_client.Subscribe(
                subscribe_key, 
                policy, 
                callback=self.charge_callback
            )

    def charge_callback(self, channel, charge, exe_policy, redis_client):
        charge_msg = json.loads(charge)
        actions = exe_policy.execute(charge_msg)
        if actions is None:
            return

        for trade_message in actions:
            trade_message['policy_id'] = exe_policy.policy_id
            redis_client.LPush("left#trade#" + str(exe_policy.account_id), json.dumps(trade_message))
            back = redis_client.BRPop("right#trade#" + str(exe_policy.account_id) + "#" + str(exe_policy.policy_id), 120)
            if back is None:
                continue 
        
            trade_back = json.loads(back)
            trade_back['timestamp'] = charge_msg['timestamp']
            policy_change = exe_policy.after_trade(trade_back)
            if policy_change is None:
                continue

            redis_client.LPush("policy#database", json.dumps(policy_change))
    
    def monit_database(self):
        redis_client = Redis(self.redis_url, self.redis_port)
        while True:
            policy_change = redis_client.BRPop("policy#database", 0)
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
        