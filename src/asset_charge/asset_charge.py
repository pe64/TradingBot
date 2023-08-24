import time
import json
from db.em_sqlite import SqliteEM
from http_opt.fund_http import fund_http_real_time_charge
from redis_opt.redis import Redis

class AssetCharge:
    def __init__(self,cf):
        self.gconf = cf
        self.em_sq = SqliteEM(cf['sqlite_path']['em'])
        self.rd = Redis(cf)
        pass

    def run(self):
        funds = self.em_sq.get_fund_self_selection() 
        self.today = time.strftime("%Y%m%d", time.localtime())
        for fund in funds:
            ret = fund_http_real_time_charge(self.gconf['web_api']['fund'], fund)
            if ret is not None:
                charge = {
                    "code":ret["fundcode"],
                    "name":ret["name"],
                    "open":ret['dwjz'],
                    "cur":ret['gsz'],
                    "percent":ret["gszzl"],
                    "timestamp":ret["gztime"]
                }
                self.rd.Publish("fund#"+fund ,json.dumps(charge))
        
        stocks = self.em_sq.get_stock_self_selection()
        for stock in stocks:
            #ret = self.em_sq.get_stock_real_charge(stock['code'], stock['market'])
            if ret is not None:
                charge = {
                    "code": stock['code'],
                    "name": stock['name'],
                }