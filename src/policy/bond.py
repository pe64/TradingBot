import json

class Bond:
    def __init__(self, js, cta) -> None:
        self.id = js['id']
        self.account_id = js['account_id']
        self.asset_id = js['asset_id']
        self.cash = float(js['cash'])
        self.asset_count = float(js['asset_count'])
        self.cash_inuse = float(js['cash_inuse'])
        self.cash_into = float(js['cash_into'])
        self.date = int(js['date'])

        para = json.loads(js['para'])
        self.period = int(para['period'])
        
        pass