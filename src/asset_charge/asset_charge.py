from re import A
import time
from datetime import datetime, timedelta
import json
from db.asset_db import AssetDB
from http_opt.fund_http import fund_http_real_time_charge
from http_opt.stock_http import stock_http_real_time_charge
from utils.redis import Redis
from http_opt.binance_http import BinanceOpt
from asset_charge.stock_charge import StockCharge
import threading
from utils.yaml_conf import yaml_load
from utils.time_format import TimeFormat

class AssetCharge:
    def __init__(self, cf):
        self.gconf = cf
        self.virtual_flag = cf['virtual']['enabled']
        if self.virtual_flag:
            self.asset_db = AssetDB(cf['virtual']['sqlite_path'])
        else:
            self.asset_db = AssetDB(cf['sqlite_path'])
        self.virtual_start = cf['virtual']['start_time']
        self.virtual_end = cf['virtual']['end_time']
        self.bn = BinanceOpt(cf)
        self.stock = StockCharge(cf)
    
    def fetch_fund_data(self, rd, fund, days =0):
        periods = [4, 9, 19, 29, 59, 119]
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
            result = rd.Get("fund#day#ma#" + fund['symbol'])
            if result is not None and result != "":
                charge['day'] = {}
                sum_js = json.loads(result)
                for per in periods:
                    sum = sum_js["ma" + str(per)] + float(ret['gsz'])
                    charge["day"]["ma" + str(per + 1)] = round(float(sum / (per + 1)),3)
                
            rd.Publish("fund#1d#" + fund['symbol'], json.dumps(charge))
            rd.Set("fund#1d#" + fund['symbol'], json.dumps(charge))


    def fetch_stock_data(self, rd, stock, days=0):
        periods = [4, 9, 19, 29, 59, 119]
        types = ["day", "week", "month"]
        #stock_info = self.stock.get_stock_charge(stock['symbol'], stock['market'])
        stock_info = stock_http_real_time_charge(self.gconf['web_api']['stock'], stock['symbol'], stock['market'])
        if stock_info is None :
            return

        if TimeFormat.stock_check_intime(stock_info['f86'], stock_info['f80']) is False:
            return

        data =  {
            "symbol": stock['symbol'],
            "name": stock['name'],
            "open": float(stock_info['f46']),
            "close": float(stock_info['f60']),
            "cur": float(stock_info['f43']),
            "high": float(stock_info['f44']),
            "low": float(stock_info['f45']),
            "percent": round((float(stock_info['f43']) - float(stock_info['f60'])) / float(stock_info['f60']) * 100, 2),
            "volume": int(stock_info['f48']),
            "timestamp": TimeFormat.transform_datatime_from_timestamp(stock_info['f86'])
        }

        for type in types:
            result = rd.Get("stock#" + type + "#ma#" + stock['symbol'])
            if result is None or len(result) == 0:
                continue
            data[type] = {}
            sum_js = json.loads(result)
            for per in periods:
                sum = sum_js["ma" + str(per)] + float(stock_info['f43'])
                data[type]["ma" + str(per + 1)] = round(float(sum / (per + 1)),3)

        rd.Publish("stock#1d#" + stock['symbol'], json.dumps(data))
        rd.Set("stock#1d#" + stock['symbol'], json.dumps(data))
        return

    def fetch_coin_data(self, rd, coin, days=0):
        if self.virtual_flag:
            utc, zone = TimeFormat.get_utc_time(self.virtual_start, days)
        else:
            utc, zone = TimeFormat.get_utc_time()
        intervals = [
            "8h", 
            "1d", 
            "1w"
        ]

        for interval in intervals:
            start_time_stamp = TimeFormat.calculate_time_range(utc, interval)
            ret = self.bn.get_kline_data(coin['symbol'], interval, start_time_stamp, cur=(self.virtual_flag is False))
            if ret is not None:
                ret['timestamp'] = TimeFormat.get_current_timestamp_format(zone)
                rd.Publish(f"coin#binance#{interval}#{coin['symbol']}", json.dumps(ret))
                rd.Set(f"coin#binance#{interval}#{coin['symbol']}", json.dumps(ret))


    def fetch_assets(self, asset_list, fetch_func):
        rd = Redis(self.gconf['redis']['url'], self.gconf['redis']['port'])
        days = 0
        while True:
            for asset in asset_list:
                fetch_func(rd, asset, days)

            if self.virtual_flag:
                days = days + 1
            time.sleep(10)

    def upload_asset(self, rd, assets):
        for asset in assets:
            rd.Set("asset#" + str(asset['id']), json.dumps(asset))

    def run(self):
        rd = Redis(self.gconf['redis']['url'], self.gconf['redis']['port'])
        funds = self.asset_db.get_fund_self_selection()
        stocks = self.asset_db.get_stock_self_selection()
        coins = self.asset_db.get_coin_self_selection()
        self.upload_asset(rd, funds)
        self.upload_asset(rd, stocks)
        self.upload_asset(rd, coins)
        fund_thread = threading.Thread(target=self.fetch_assets, args=(funds, self.fetch_fund_data))
        stock_thread = threading.Thread(target=self.fetch_assets, args=(stocks, self.fetch_stock_data))
        coin_thread = threading.Thread(target=self.fetch_assets, args=(coins, self.fetch_coin_data))

        fund_thread.start()
        stock_thread.start()
        coin_thread.start()

        fund_thread.join()
        stock_thread.join()
        coin_thread.join()

