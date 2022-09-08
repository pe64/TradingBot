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
        "Sec-Fetch-Dest": conf_head["sec_fetch_dest"],
        "Sec-Fetch-Mode": conf_head["sec_fetch_mode"],
        "Sec-Fetch-Site": conf_head["sec_fetch_site"],
        "User-Agent": conf_head["user_agent"],
        "sec-ch-ua": conf_head["sec_ch_ua"],
        "sec-ch-ua-mobile": conf_head["sec_ch_ua_mobile"],
        "sec-ch-ua-platform": conf_head["sec_ch_ua_platform"]
    }

    return headers

def fund_http_real_time_charge(conf, fcode):
    url = conf["url"] + \
            conf["path"] + \
            conf["real_time_charge"]["file"] + \
            "?FCODE=" + fcode + "&"
    for arg in conf["real_time_charge"]["arguments"] :
        url = url + arg + "&"
        
    url = url +"_="

    ts = time.time()

    url = url + str(int(ts))

    headers = build_headers(conf["headers"])

    req = request.Request(url, headers=headers)
    response = request.urlopen(req)
    ret = response.read().decode('utf-8')
    js = json.loads(ret)
    return js

def fund_http_history_charge(conf, fcode):
    url = conf["url"] + conf["path"] + conf["history_charge"]["file"] + '?FCODE=' + fcode + '&' 

    for arg in conf["history_charge"]["arguments"] :
        url = url + arg + "&"
        
    url = url +"_="

    ts = time.time()

    url = url + str(int(ts))
    headers = build_headers(conf["headers"])
    req = request.Request(url, headers=headers)
    response = request.urlopen(req)
    return response.read().decode('utf-8')

def fund_http_get_all_fund(conf):
    url = conf["all_fund_url"]

    req = request.Request(url)
    resp = request.urlopen(req).read().decode('utf-8')
    start = resp[9:-1].lstrip()
    ret = json.loads(start)
    return ret
    