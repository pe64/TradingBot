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
        self.ttb_diff = float(para['ttb_diff'])
        self.limit_days = int(para['limit_days'])
        self.cta = cta
        
        pass

    def execute(self, args):
        if args['type'] != "bond":
            return 

        code = args['code']
        price = args['price']
        percent = args['percent']
        today = args['today']
        limit_days = args['limit_days']
        if code not in self.asset_id:
            return
    
        para = {}
        earn = 0
