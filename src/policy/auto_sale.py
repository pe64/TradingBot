import json

class AutoSale:
    def __init__(self, policy_config) -> None:
        self.asset_id = policy_config['asset_id']
        pass
    
    def execult(self, charge):
        print(charge)
        ret = {
            "opt":"SALE",
            "price":charge['cur']
        }
        return ret