import time
from datetime import datetime, timedelta
import json
from db.asset_db import AssetDB
from http_opt.fund_http import fund_http_real_time_charge
from redis_opt.redis import Redis
from http_opt.binance_http import BinanceOpt
from stock.stock_charge import StockCharge
import threading
from conf.yaml_conf import yaml_load

class AssetCharge:
    def __init__(self, cf):
        self.gconf = cf
        self.asset_db = AssetDB(cf['sqlite_path'])
        self.bn = BinanceOpt(cf)
        self.stock = StockCharge(cf)
        self.rd = Redis(cf)
    
    @staticmethod
    def get_time_range_1w(current_utc_time):
        # 计算前7天的UTC时间
        start_time = current_utc_time - timedelta(days=7)
    
        # 计算当前UTC时间
        end_time = current_utc_time
    
        return start_time, end_time

    @staticmethod
    def get_time_range_1d(current_utc_time):
        # 计算前一天的UTC 00:00时间
        start_time = current_utc_time.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    
        # 计算当前UTC时间
        end_time = current_utc_time
    
        return start_time, end_time

    @staticmethod
    def get_time_range_8h(current_utc_time):
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
        return start_time_stamp, end_time_stamp

    def fetch_fund_data(self, fund):
        ret = fund_http_real_time_charge(self.gconf['web_api']['fund'], fund['symbol'])
        if ret is not None:
            charge = {
                "symbol": ret["fundcode"],
                "name": ret["name"],
                "open": ret['dwjz'],
                "close": ret['dwjz'],
                "cur": ret['gsz'],
                "percent": ret["gszzl"],
                "timestamp": ret["gztime"]
            }
            self.rd.Publish("fund#" + fund['symbol'], json.dumps(charge))

    def fetch_stock_data(self, stock):
        ret = self.stock.get_stock_charge(stock['symbol'], stock['market'])
        if ret is not None:
            self.rd.Publish("stock#" + stock['symbol'], json.dumps(ret))

    def fetch_coin_data(self, coin):
        current_utc_time = datetime.utcnow()
        start_time_stamp, end_time_stamp = self.get_time_range_8h(current_utc_time)
        ret = self.bn.get_kline_data(coin['symbol'], "8h", start_time_stamp, end_time_stamp)
        if ret is None:
            return

        ret['timestamp'] = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        self.rd.Publish("coin#binance#8h#" + coin['symbol'], json.dumps(ret))

        start_time_stamp, end_time_stamp = self.get_time_range_1d(current_utc_time)
        ret = self.bn.get_kline_data(coin['symbol'], "1d", start_time_stamp, end_time_stamp)
        if ret is None:
            return

        ret['timestamp'] = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        self.rd.Publish("coin#binance#1d#" + coin['symbol'], json.dumps(ret))

        start_time_stamp, end_time_stamp = self.get_time_range_1w(current_utc_time)
        ret = self.bn.get_kline_data(coin['symbol'], "1w", start_time_stamp, end_time_stamp)
        if ret is None:
            return

        ret['timestamp'] = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        self.rd.Publish("coin#binance#1w#" + coin['symbol'], json.dumps(ret))




    def fetch_assets(self, asset_list, fetch_func):
        while True:
            self.today = time.strftime("%Y%m%d", time.localtime())
            for asset in asset_list:
                fetch_func(asset)
            time.sleep(10)

    def upload_asset(self, assets):
        for asset in assets:
            self.rd.Set("asset#" + str(asset['id']), json.dumps(asset))

    def run(self):
        funds = self.asset_db.get_fund_self_selection()
        stocks = self.asset_db.get_stock_self_selection()
        coins = self.asset_db.get_coin_self_selection()
        self.upload_asset(funds)
        self.upload_asset(stocks)
        self.upload_asset(coins)
        fund_thread = threading.Thread(target=self.fetch_assets, args=(funds, self.fetch_fund_data))
        stock_thread = threading.Thread(target=self.fetch_assets, args=(stocks, self.fetch_stock_data))
        coin_thread = threading.Thread(target=self.fetch_assets, args=(coins, self.fetch_coin_data))

        fund_thread.start()
        stock_thread.start()
        coin_thread.start()

        fund_thread.join()
        stock_thread.join()
        coin_thread.join()

