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

def stock_http_history_charge(conf, fcode):
    url = conf["url"] + \
        conf["path"] + "?secid=" + \
        fcode + "&"
    for arg in conf["arguments"]:
        url = url + arg + "&"
    
    url = url +"_="
    ts = time.time()
    url = url + str(int(ts))

    headers = build_headers(conf["headers"])
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req).read().decode('utf-8')
    start = resp[19:-2]
    ret = json.loads(start)
    return ret
