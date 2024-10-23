import json
from urllib import request
import time
import re
import io
import gzip

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
        "sec-ch-ua-platform": conf_head["sec_ch_ua_platform"],
    }

    return headers

def fund_http_real_time_charge(conf, fcode):
    url = conf["url"] + \
            conf["path"] + fcode +".js"
    #for arg in conf["real_time_charge"]["arguments"] :
    #    url = url + arg + "&"
        
    #url = url + "Fcodes=" + fcode 

    #url = url +"_="
    #ts = time.time()
    #url = url + str(int(ts))

    headers = build_headers(conf["headers"])
    headers['upgrade-insecure-requests'] = 1
    headers['authority'] = "fund.rabt.top"
    try:
        req = request.Request(url, headers=headers)
        response = request.urlopen(req)
        content_encoding = response.info().get('Content-Encoding')

        if content_encoding == 'gzip':
            compress_data = response.read()
            buffer = io.BytesIO(compress_data)
            with gzip.GzipFile(fileobj=buffer) as f:
                data = f.read()
    
        else: 
            data = response.read()

        encoding = response.info().get_content_charset('utf-8')
        response_str = data.decode('utf-8')
        ret = re.search(r'jsonpgz\((.*?)\);', response_str).group(1)
        js = json.loads(ret)
        return js
    except:
        return None

def fund_http_history_charge(conf, fcode):
    url = conf["his_url"] + conf["his_path"] + '?fundCode=' + fcode + '&' 

    for arg in conf["his_args"]:
        url = url + arg + "&"
        
    url = url +"_="

    ts = time.time()

    url = url + str(int(ts))
    headers = build_headers(conf["headers"])
    headers['Referer'] = "https://fundf10.eastmoney.com/"
    req = request.Request(url, headers=headers)
    response = request.urlopen(req)
    ret = response.read().decode('utf-8')
    if ret != None:
        return json.loads(ret)
    else:
        return None

def fund_http_get_all_fund(conf):
    url = conf["all_fund_url"]

    req = request.Request(url)
    resp = request.urlopen(req).read().decode('utf-8')
    start = resp[9:-1].lstrip()
    ret = json.loads(start)
    return ret
    