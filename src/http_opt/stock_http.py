import json
from urllib import request
import time

def build_headers(conf_head):
    headers = {
        "Accept": conf_head["accept"],
        "Accept-Language": conf_head["accept_language"],
        "Cache-Control": conf_head["cache_control"],
        "Connection": conf_head["connection"],
        "Pragma": conf_head["pragma"],
        "Referer": conf_head["referer"],
        "User-Agent": conf_head["user_agent"],
        "sec-gpc": conf_head["sec_gpc"],
    }
    return headers


def stock_http_kline(conf, fcode, type, beg, end):

    klt = {
        "day": "101",
        "week": "102",
        "month": "103"
    }

    url = conf["url"] + \
        conf["path"] + "?secid=" + \
        fcode + "&"

    for arg in conf["arguments"]:
        url = url + arg + "&"
    
    url = url + "klt=" + klt[type] + "&"
    url = url + "beg=" + beg + "&"
    url = url + "end=" + end + "&"
    
    url = url +"_="
    ts = time.time()
    url = url + str(int(ts))

    headers = build_headers(conf["headers"])
    req = request.Request(url)
    resp = request.urlopen(req).read().decode('utf-8')
    ret = json.loads(resp)
    return ret

def stock_http_get_code_list(conf):
    url = conf['url'] + \
        conf['path'] + "?"
    for arg in conf["arguments"]:
        url = url + arg +"&"

    url = url +"_="
    ts = time.time()
    url = url + str(int(ts))
    
    req = request.Request(url)
    resp = request.urlopen(req).read().decode('utf-8')
    ret = json.loads(resp)
    return ret

def stock_http_real_time_charge(conf, scode, market):
    url = conf['charge_url'] + \
        conf['charge_path'] + "?" 
    
    for arg in conf['charge_args']:
        url = url + arg + "&"
        
    url = url + "secid=" + conf['market_code'][market] +'.' + scode +"&"

    url = url +"_="
    ts = time.time()
    url = url + str(int(ts))

    req = request.Request(url)
    resp = request.urlopen(req).read().decode('utf-8')
    ret = json.loads(resp)
    if ret["rc"] == 0:
        return ret['data']
    else:
        return None