import json
import time
from db.sqlite import SqliteObj
from utils.redis import Redis
from http_opt import fund_http
from http_opt import stock_http
from utils.yaml_conf import yaml_load
from utils.time_format import TimeFormat

def update_fund_kline(asset_sql, history_sql, cf):
    fcodes = asset_sql.get_fund_self_selections()
    for fcode in fcodes:
        his = fund_http.fund_http_history_charge(cf["web_api"]["fund"], fcode[0])
        history_sql.insert_fund_history_charges(his, fcode=fcode[0])

def upload_fund_masum(asset_sql, history_sql, rd):
    periods = [4, 9, 19, 29, 59, 119]
    fcodes = asset_sql.get_fund_self_selections()
    for fcode in fcodes:
        data = {}
        for per in periods:
            data['ma' + str(per)]= history_sql.get_fund_masum(fcode[0], per)
        data['timestamp'] = TimeFormat.get_local_timstamp()
        rd.Set("fund#day#ma#" + fcode[0], json.dumps(data))
    
    time_result = {}
    result = rd.Get("timerecord")
    if result is None or len(result) == 0:
        time_result["fundsum"] = TimeFormat.get_local_timstamp()
    else:
        time_result = json.loads(result)
        time_result["fundsum"] = TimeFormat.get_local_timstamp()
    
    rd.Set("timerecord", json.dumps(time_result))
        

def upload_stock_masum(asset_sql, history_sql, rd):
    periods = [4, 9, 19, 29, 59, 119]
    types = ["day", "week", "month"]
    stocks = asset_sql.get_stock_self_selection()
    for type in types:
        for stock in stocks:
            data = {}
            for per in periods:
                data["ma" + str(per)] = history_sql.get_stock_masum(stock[0], type, per)

            data['timestamp'] = TimeFormat.get_local_timstamp()
            rd.Set("stock#" + type +"#ma#" + stock[0], json.dumps(data))

    time_result = {}
    result = rd.Get("timerecord")
    if result is None or len(result) == 0:
        time_result["stocksum"] = TimeFormat.get_local_timstamp()
    else:
        time_result = json.loads(result)
        time_result["stocksum"] = TimeFormat.get_local_timstamp()
    
    rd.Set("timerecord", json.dumps(time_result))

def update_stock_kline(asset_sql, history_sql, cf):
    beg = ""
    stocks = asset_sql.get_stock_self_selection()
    local_time = TimeFormat.get_local_timstamp()
    for stock in stocks:
        scode = cf["web_api"]['stock']['market_code'][stock[1]] + "." + stock[0]
        date = history_sql.get_stock_last_klines(stock[0], "day")
        if date is not None:
            beg = TimeFormat.format_date(date)
        else:
            beg = ""
        his = stock_http.stock_http_kline(cf["web_api"]["stock"], scode, "day", beg, local_time[:8])
        history_sql.insert_stock_kline(his["data"]["klines"], stock[0], "day")
        date = history_sql.get_stock_last_klines(stock[0], "week")
        if date is not None:
            beg = TimeFormat.format_date(date)
        else:
            beg = ""
        his = stock_http.stock_http_kline(cf["web_api"]["stock"], scode, "week", beg, local_time[:8])
        if TimeFormat.is_first_day_of_week(local_time):
            history_sql.insert_stock_kline(his["data"]["klines"], stock[0], "week")
        else:
            history_sql.insert_stock_kline(his["data"]["klines"][:-1], stock[0], "week")

        date = history_sql.get_stock_last_klines(stock[0], "month")
        if date is not None:
            beg = TimeFormat.format_date(date)
        else:
            beg = ""
        his = stock_http.stock_http_kline(cf["web_api"]["stock"], scode, "month", beg, local_time[:8])
        if TimeFormat.is_first_day_of_month(local_time):
            history_sql.insert_stock_kline(his["data"]["klines"], stock[0], "month")
        else:
            history_sql.insert_stock_kline(his["data"]["klines"][:-1], stock[0], "month")

def main():
    cf = yaml_load()
    asset_sq = SqliteObj(cf["sqlite_path"])
    history_sq = SqliteObj(cf["history_db_path"])
    rd = Redis(cf['redis']['url'], cf['redis']['port'])
    while True:
        local_time = TimeFormat.get_local_timstamp()
        if TimeFormat.is_time_between(local_time, 
                                    cf["period"]["kline"]['start'], 
                                    cf['period']['kline']['end']) is False:
            time.sleep(1800)
            continue

        update_fund_kline(asset_sq, history_sq, cf)
        update_stock_kline(asset_sq, history_sq, cf)
        upload_fund_masum(asset_sq, history_sq, rd)
        upload_stock_masum(asset_sq, history_sq, rd)

        time.sleep(600)
        

    
if __name__ == "__main__":
    main()

