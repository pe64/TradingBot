import time
from datetime import datetime, timedelta
import json
from db.em_sqlite import SqliteEM
from http_opt.fund_http import fund_http_real_time_charge
from redis_opt.redis import Redis
from binance.binance import BinanceOpt
from stock.stock_charge import StockCharge

class AssetCharge:
    def __init__(self,cf):
        self.gconf = cf
        self.em_sq = SqliteEM(cf['sqlite_path']['em'])
        self.bn = BinanceOpt(cf)
        self.stock = StockCharge(cf)
        self.rd = Redis(cf)
        pass

    def run(self):
        funds = self.em_sq.get_fund_self_selection() 
        stocks = self.em_sq.get_stock_self_selection()
        coins = self.em_sq.get_coin_self_selection()

        while True:
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
        
            for stock in stocks:
                ret = self.stock.get_stock_charge(stock['code'], stock['market'])
                if ret is not None:
                    self.rd.Publish("stock#" + stock['code'], json.dumps(ret))

            current_utc_time = datetime.utcnow()
            # 判断当前时间属于哪个时间段
            if 0 <= current_utc_time.hour < 8:
                start_time = current_utc_time.replace(hour=0, minute=0, second=0, microsecond=0)
                end_time = start_time.replace(hour=8)
            elif 8 <= current_utc_time.hour < 16:
                start_time = current_utc_time.replace(hour=8, minute=0, second=0, microsecond=0)
                end_time = start_time.replace(hour=16)
            else:
                start_time = current_utc_time.replace(hour=16, minute=0, second=0, microsecond=0)
                end_time = start_time.replace(hour=0) + timedelta(days=1)

            start_time_stamp = int(start_time.timestamp()) * 1000
            end_time_stamp = int(end_time.timestamp()) * 1000

            for coin in coins:
                ret = self.bn.get_kline_data(coin, "8h", start_time_stamp, end_time_stamp)
                ret['timestamp'] = time.strftime("%Y-%m-%d %H:%M", time.localtime())
                self.rd.Publish("coin#binance#8h#"+coin ,json.dumps(ret))
            
            time.sleep(10)
