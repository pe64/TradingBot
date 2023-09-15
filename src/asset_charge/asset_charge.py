import time
from datetime import datetime, timedelta
import json
from db.asset_db import AssetDB
from http_opt.fund_http import fund_http_real_time_charge
from utils.redis import Redis
from http_opt.binance_http import BinanceOpt
from stock.stock_charge import StockCharge
import threading
from utils.yaml_conf import yaml_load
from utils.time_format import TimeFormat

class AssetCharge:
    def __init__(self, cf):
        self.gconf = cf
        self.asset_db = AssetDB(cf['sqlite_path'])
        self.bn = BinanceOpt(cf)
        self.stock = StockCharge(cf)
        self.rd = Redis(cf)
    
    def fetch_fund_data(self, fund):
        ret = fund_http_real_time_charge(self.gconf['web_api']['fund'], fund['symbol'])
        if ret is not None:
            charge = {
                "symbol": ret["fundcode"],
                "name": ret["name"],
                "open": float(ret['dwjz']),
                "close": float(ret['dwjz']),
                "cur": float(ret['gsz']),
                "percent": float(ret["gszzl"]),
                "timestamp": TimeFormat.transform_datatime_format(ret["gztime"])
            }
            self.rd.Publish("fund#1d#" + fund['symbol'], json.dumps(charge))


    def fetch_stock_data(self, stock):
        stock_info = self.stock.get_stock_charge(stock['symbol'], stock['market'])
        if stock_info is None:
            return

        data =  {
            "symbol": stock['symbol'],
            "name": stock_info[0],
            "open": float(stock_info[1]),
            "close": float(stock_info[2]),
            "cur": float(stock_info[3]),
            "high": float(stock_info[4]),
            "low": float(stock_info[5]),
            "percent": round((float(stock_info[3]) - float(stock_info[2])) / float(stock_info[2]) * 100, 2),
            "volume": int(stock_info[8]),
            "timestamp": TimeFormat.transform_datatime_format(stock_info[30] + " " + stock_info[31])
        }

        self.rd.Publish("stock#1d#" + stock['symbol'], json.dumps(data))
        return

    def fetch_coin_data(self, coin):
        current_utc_time = datetime.utcnow()
        intervals = [
            "8h", 
            "1d", 
            "1w"
        ]

        for interval in intervals:
            start_time_stamp = TimeFormat.calculate_time_range(current_utc_time, interval)
            ret = self.bn.get_kline_data(coin['symbol'], interval, start_time_stamp)
            if ret is None:
                continue
            else:
                ret['timestamp'] = time.strftime("%Y%m%d%H%M%S", time.localtime())
                self.rd.Publish(f"coin#binance#{interval}#{coin['symbol']}", json.dumps(ret))


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

