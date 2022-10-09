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
        self.buy_count = int(para['buy_count'])
        self.last_price = 0.0
        self.buy_count_limit = 1000
        self.cta = cta
        
        pass
    
    def check_buy_bond(self, price, ttb_yield, today, limit_days):
        return price - ttb_yield > self.ttb_diff and \
                    price > self.price and \
                        self.date != today and \
                            limit_days < self.limit_days

    def execute(self, args):
        if args['type'] != "bond":
            return 

        code = args['code']
        price = args['price']
        today = args['today']
        limit_days = args['limit_days']
        ttb_yield = args['ttb_yield']
        if code not in self.asset_id:
            return

        if self.check_buy_bond(price, ttb_yield, today, limit_days):
            vol = int(self.buy_count/1000) * 1000
            para = {
                "policy_id": self.id,
                "account_id": self.account_id,
                "code":code,
                "asset_count": self.asset_count,
                "vol": vol,
            }
            ret = self.cta.lend_bond(para)
