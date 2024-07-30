import json
import time
from db.sqlite import SqliteObj
from utils.redis import Redis
from http_opt import fund_http
from http_opt import stock_http
from utils.yaml_conf import yaml_load
from utils.time_format import TimeFormat

def update_fund_kline(cf, sql):
    fcodes = sql.get_fund_self_selections()
    for fcode in fcodes:
        his = fund_http.fund_http_history_charge(cf["web_api"]["fund"], fcode[0])
        sql.insert_fund_history_charges(his, fcode=fcode[0])

def upload_fund_masum(sql, rd):
    periods = [4, 9, 19, 29, 59, 119]
    fcodes = sql.get_fund_self_selections()
    for fcode in fcodes:
        data = {}
        for per in periods:
            data['ma' + str(per)]= sql.get_fund_masum(fcode[0], per)
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
        

def upload_stock_masum(sql, rd):
    periods = [4, 9, 19, 29, 59, 119]
    types = ["day", "week", "month"]
    stocks = sql.get_stock_self_selection()
    for type in types:
        for stock in stocks:
            data = {}
            for per in periods:
                data["ma" + str(per)] = sql.get_stock_masum(stock[0], type, per)

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

def update_stock_kline(cf, sql_handel):
    stocks = sql_handel.get_stock_self_selection()
    local_time = TimeFormat.get_local_timstamp()
    for stock in stocks:
        scode = cf["web_api"]['stock']['market_code'][stock[1]] + "." + stock[0]
        his = stock_http.stock_http_kline(cf["web_api"]["stock"], scode, "day")
        sql_handel.insert_stock_kline(his["data"]["klines"], stock[0], "day")
        if TimeFormat.is_first_day_of_week(local_time):
            his = stock_http.stock_http_kline(cf["web_api"]["stock"], scode, "week")
            sql_handel.insert_stock_kline(his["data"]["klines"], stock[0], "week")
        if TimeFormat.is_first_day_of_month(local_time):
            his = stock_http.stock_http_kline(cf["web_api"]["stock"], scode, "month")
            sql_handel.insert_stock_kline(his["data"]["klines"], stock[0], "month")


def main():
    cf = yaml_load()
    fund_sq = SqliteObj(cf["sqlite_path"])
    stock_sq = SqliteObj(cf["sqlite_path"])
    rd = Redis(cf['redis']['url'], cf['redis']['port'])
    while True:
        local_time = TimeFormat.get_local_timstamp()
        if TimeFormat.is_time_between(local_time, 
                                    cf["period"]["kline"]['start'], 
                                    cf['period']['kline']['end']) is False:
            time.sleep(1800)
            continue

        update_fund_kline(cf, fund_sq)
        update_stock_kline(cf, stock_sq)
        upload_fund_masum(fund_sq, rd)
        upload_stock_masum(stock_sq, rd)
        

    
if __name__ == "__main__":
    main()

