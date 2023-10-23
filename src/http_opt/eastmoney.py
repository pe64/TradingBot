import random
import os
import json
import sys
import datetime
import time
import hashlib
from http import cookiejar
from urllib import request,parse
from http_opt.fund51_http import get_time_day, get_time_strl
#from ocr.ocr import ocr_em
from crypto.rsa_crypto import JSEncrypt

class HttpEM:
    def __init__(self, cf, account) -> None:
        self.account_id = account['id']
        self.cookie_path = cf["eastmoney"]["cookie"] + str(self.account_id)

        self.update_cookie()

        self.ver_conf = cf["eastmoney"]["ver_code"]
        self.login_conf = cf["eastmoney"]['login']
        self.validatekey_conf = cf["eastmoney"]["validatekey"]
        self.sign_contract_conf = cf['eastmoney']['sign_contract']
        self.check_sdx_conf = cf['eastmoney']['check_sdx']
        self.check_status_conf = cf['eastmoney']['check_status']
        self.fund_submit_trade_conf = cf['eastmoney']['fund_submit_trade']
        self.get_revoke_list_conf = cf['eastmoney']['get_revoke_list']
        self.headers = cf["eastmoney"]["headers_comm"]
        self.fund_revoke_orders_conf = cf['eastmoney']['fund_revoke_orders']
        self. stock_get_revokes_conf = cf['eastmoney']['stock_get_revokes']
        self.get_fund_position_conf = cf['eastmoney']['get_fund_position']
        self.get_fund_asset_conf = cf['eastmoney']['get_fund_asset']
        self.stock_revoke_order_conf = cf['eastmoney']['stock_revoke_order']
        self.stock_submit_trade_conf = cf['eastmoney']['stock_submit_trade']
        self.stock_list_conf = cf['eastmoney']['stock_list']
        self.get_fund_his_deals_conf = cf['eastmoney']['get_fund_his_deals']
        self.real_charge_conf = cf['eastmoney']['stock_real_charge']
        self.deal_data_conf = cf['eastmoney']['stock_deal_data']
        self.get_can_buy_new_stock_conf = cf['eastmoney']['get_can_buy_new_stock']
        self.get_bond_list_conf = cf['eastmoney']['get_bond_list']
        self.submit_bat_trade_conf = cf['eastmoney']['submit_bat_trade']
        self.get_asset_conf = cf['eastmoney']['get_asset']
        self.ttb_code_conf = cf['eastmoney']['get_ttb_code']
        self.ttb_yield_conf = cf['eastmoney']['get_ttb_yield']
        self.bond_code_conf = cf['eastmoney']['get_bond_code']
        self.bond_days_conf = cf['eastmoney']['get_bond_days']
        self.bond_yield_conf = cf['eastmoney']['get_bond_yield']
        self.lending_bond_conf = cf['eastmoney']['lending_bond']
        self.ttb_yield = 0
        self.validatekey = ""
        self.random = str(random.random())
        #with open(self.login_conf['arguments'], "r") as f:
        #    content = f.read()
        self.user_id = account['userId']
        self.login_js = account
        self.password = self.login_js['password']
        self.new_stock_flag = False
        pass
    
    def update_cookie(self):
        if os.path.exists(self.cookie_path):
            self.cookie = cookiejar.LWPCookieJar(self.cookie_path)
            self.cookie.load(ignore_expires=True,ignore_discard=True)
        else:
            self.cookie = cookiejar.LWPCookieJar()
        self.cookie_handler = request.HTTPCookieProcessor(self.cookie)
        self.opener = request.build_opener(self.cookie_handler)
        pass

    def get_user_id(self):
        return self.user_id[6:] + "******"

    def build_headers(self, conf_head, custom_headers=None):
        if custom_headers is None:
            headers = {}
        else:
            headers = custom_headers
        for item in self.headers:
            sp = item.split(':', 1)
            headers[sp[0]] = sp[1].strip()
        for item in conf_head:
            sp = item.split(':', 1)
            headers[sp[0]] = sp[1].strip()
        return headers

    def wget_em_ver_code(self):
        code_path = self.ver_conf["file"] + str(time.time()) + ".jpg"
        url = self.ver_conf['url'] + "?" + "randNum=" + self.random 
        headers = self.build_headers(self.ver_conf["headers"])
        req = request.Request(url, headers=headers)
        resp = self.opener.open(req)
        text = resp.read()
        sha256_hash = hashlib.sha256()
        sha256_hash.update(text)
        hash_hex = sha256_hash.hexdigest()
        final_path = f"cache/{hash_hex}.jpg"
        with open(final_path, "wb") as f:
            f.write(text)
        
    def login_em_ver_code(self):
        code_path = self.ver_conf["file"] + str(self.account_id) + ".jpg"

        url = self.ver_conf['url'] + "?" + "randNum=" + self.random 
        headers = self.build_headers(self.ver_conf["headers"])
        req = request.Request(url, headers=headers)
        resp = self.opener.open(req)
        text = resp.read()
        with open(code_path, "wb") as f:
            f.write(text)
        os.system("catimg "+code_path)
        #self.ver_code = ocr_em(code_path)
        #if self.ver_code != None and len(self.ver_code) == 6:
        #    break
        #else:
        #    print("ver_code error.")
        #    time.sleep(120)

    def http_post(self, url, arg, headers, raw=False):
        if raw == False:
            data = parse.urlencode(arg).encode('utf-8')
        else:
            data = arg
        req = request.Request(url, method="POST",data=data, headers=headers)
        resp = self.opener.open(req)
        ret = resp.read().decode('utf-8')
        try:
            js = json.loads(ret)
            return js
        except:
            return {"Status":0}

    def login_em_platform(self):
        url = self.login_conf["url"]
        path = self.ver_conf["file"] + str(self.account_id) + ".jpg"
        headers = self.build_headers(self.login_conf["headers"])
        rsa = JSEncrypt(self.login_conf["private_key"])
        self.login_js["password"] = rsa.rsa_long_encrypt(self.password)
        print("input ver code:")
        self.login_js["identifyCode"] = sys.stdin.readline().strip()
        self.login_js["randNumber"] = self.random
        js = self.http_post(url, arg=self.login_js, headers=headers)
        if js["Status"] == 0:
            print("login success %s."%str(datetime.datetime.now()))
            self.cookie.save(filename=self.cookie_path,ignore_discard=True, ignore_expires=True)
            os.rename(path, str(path).replace("vercode"+str(self.account_id), self.login_js['identifyCode']))
            return js['Status']
        else:
            print("login error.")
        pass

    def get_validate_key(self):
        url = self.validatekey_conf['url']
        headers = self.build_headers(self.validatekey_conf["headers"])
        req = request.Request(url, headers=headers)
        resp = self.opener.open(req)
        text = resp.read().decode('utf-8')
        id = text.find("em_validatekey")
        if id == -1 :
            print("login time out %s."%str(datetime.datetime.now()))
            return False
        else:
            id2 = text.find("value=", id)
            self.validatekey = text[id2+7:id2+43]
            sys.stdout.flush()
            return True
    
    def sign_contract(self, fcode):
        url = self.sign_contract_conf['url'] + self.validatekey
        ch = {
            "gw_reqtimestamp": get_time_strl()
        }
        headers = self.build_headers(self.sign_contract_conf['headers'], ch)
        data = {
            "proCode": fcode,
            "eproCode": "1129"
        }
        js = self.http_post(url, arg=data, headers=headers)
        if js["Status"] == 0:
            self.cookie.save(filename=self.cookie_path, ignore_discard=True, ignore_expires=True)
            return True
        else:
            print("sign contract error [%s]"%js['Message'])
            return False
        pass

    def check_sdx(self, fcode):
        url = self.check_sdx_conf['url'] + self.validatekey
        headers = self.build_headers(self.check_sdx_conf['headers'])
        data = {
            "inst_code" :fcode
        }
        js = self.http_post(url, arg=data, headers=headers)
        if js['Status'] == 0:
            self.cookie.save(filename=self.cookie_path,ignore_discard=True, ignore_expires=True)
            return True
        else:
            print("check sdx error [%s]"%js["Message"])
            return False
        pass

    def check_status(self, fcode, company):
        url = self.check_status_conf['url'] + self.validatekey
        headers = self.build_headers(self.check_status_conf['headers'])
        if company is None:
            data = {
                "jjdm": fcode
            }
        else :
            data = {
                "jjdm": fcode,
                "jjgs": company
            }

        js = self.http_post(url, arg=data, headers=headers)
        if js['Status'] == 0:
            self.cookie.save(filename=self.cookie_path,ignore_discard=True, ignore_expires=True)
            return True
        else:
            print("check status error [%s]"%js["Message"])
            return False
        pass
    
    def fund_submit_trade(self, fcode, vol, func):
        tt = 1
        url = self.fund_submit_trade_conf['url'] + self.validatekey
        ch = {
            "gw_reqtimestamp": get_time_strl()
        }
        headers = self.build_headers(self.fund_submit_trade_conf['headers'], custom_headers=ch)
        if func == "buy":
            tt = 1
            jesh = ""
            forcetrade="1"
        else:
            tt = 3
            jesh = "0"
            forcetrade=""
        data = {
            "tradeType": tt,
            "jjdm": fcode,
            "wtje": vol,
            "sffs": 0,
            "jesh": jesh,
            "forceTrade": forcetrade,
            "risk5Trace": 0
        }
        js = self.http_post(url, arg=data, headers=headers)
        if js['Status'] == 0:
            self.cookie.save(filename=self.cookie_path,ignore_discard=True, ignore_expires=True)
            return js['Data'][0]["Wtbh"]
        else:
            print("submit trade error [%s]"%js["Message"])
            return None
        pass

    def get_revoke_list(self):
        url = self.get_revoke_list_conf['url'] + self.validatekey
        headers = self.build_headers(self.submit_trade_conf['headers'])
        data = {
            "qqhs":100,
            "dwc": 1
        }
        js = self.http_post(url, arg=data, headers=headers)
        if js['Status'] == 0:
            return js["Data"]
        else:
            return []
        
    def fund_revoke_orders(self, order):
        url = self.fund_revoke_orders_conf['url'] + self.validatekey
        headers = self.build_headers(self.fund_revoke_orders_conf['headers'])
        data = {
            "revokes": order
        }

        js = self.http_post(url, arg=data, headers=headers)
        if js["Status"] == 0:
            print("revoke %s success."%order)
        else :
            print("revoke order error [%s]"%js['Message'])
    
    def get_fund_asset(self):
        url = self.get_fund_asset_conf['url'] + self.validatekey
        headers = self.build_headers(self.get_fund_asset_conf['headers'])
        data = {
            "validatekey": self.validatekey
        }

        js = self.http_post(url, arg=data, headers=headers)
        
        return js['Status'], js["Data"]

    def get_fund_position(self):
        url = self.get_fund_position_conf["url"] + self.validatekey
        headers = self.build_headers(self.get_fund_position_conf['headers'])
        data = {
            "qqhd": 1000,
            "dwc":1
        }
        js = self.http_post(url, arg=data, headers=headers)
        if js['Status'] == 0:
            return js["Data"]
        else:
            print("get position error [%s]"%js['Message'])
    
    def fund_get_his_deals(self, st, et):
        url = self.get_fund_his_deals_conf['url'] + self.validatekey
        headers = self.build_headers(self.get_fund_his_deals_conf['headers'])
        data = {
            "st": st,
            "et": et,
            "qqhs": 1000,
            "dwc": 1
        }
        js =self.http_post(url, arg=data, headers=headers)
        if js["Status"] == 0:
            return js["Data"]
        else:
            print("get his deal error [%s]"%js['Message'])

    def stock_get_revokes(self):
        url = self.stock_get_revokes_conf['url'] + self.validatekey
        headers = self.build_headers(self.stock_get_revokes_conf['headers'])
        data = {}
        js = self.http_post(url, arg=data, headers=headers)
        if js['Status'] == 0:
            return js["Data"]
        else :
            print("get revoke stock error [%s]"%js['Message'])
    
    def stock_revoke_order(self, order):
        url = self.stock_revoke_order_conf['url'] + self.validatekey
        headers = self.build_headers(self.stock_revoke_order_conf['headers'])
        data = {
            "revokes": get_time_day()+"_"+order
        }

        js = self.http_post(url, arg=data, headers=headers)
        if js["Status"] == 0:
            return True
        else:
            print("revoke error [%s]"%js["Message"])
            return False
    
    def stock_submit_trade(self, scode, sname, price, amount, market, stype):
        url = self.stock_submit_trade_conf['url'] + self.validatekey
        headers = self.build_headers(self.stock_submit_trade_conf['headers'])
        data = {
            "stockCode":scode,
            "price":price,
            "amount":amount,
            "tradeType":stype,
            "zqmc":sname,
            "market":market
        }
        if stype == "S":
            data['gddm'] = ""

        js = self.http_post(url, arg=data, headers=headers)
        if js["Status"] == 0:
            print("submit_success order [%s]"%js["Data"][0]["Wtbh"])
            return js["Data"][0]["Wtbh"]
        else:
            print("submit trade error %s"%(js["Message"]))
            return None
    
    def get_stock_list(self):
        url = self.stock_list_conf['url'] + self.validatekey
        headers = self.build_headers(self.stock_list_conf['headers'])
        data = {
            "qqhs": 1000,
            "dwc": ""
        }
        js = self.http_post(url, data, headers)
        if js["Status"] == 0:
            print("get stock list success.")
            return js["Data"]
        else:
            print("get stock list error. [%s]" %js["Message"])
            return []
    
    def get_deal_data(self):
        url = self.deal_data_conf['url'] + self.validatekey
        headers = self.build_headers(self.deal_data_conf['headers'])
        data = {
            "qqhs": 1000,
            "dwc": ""
        }

        js = self.http_post(url, data, headers)
        if js["Status"] == 0:
            return js["Data"]
        else:
            print("get stock deal data error %s"%js["Message"])
            return []
    
    def get_stock_real_charge(self, code, market):
        url = self.real_charge_conf['url'] + \
            code +"&market=" + market + "&callback=18308463682767140384_" + \
            get_time_strl() +"&_=" + get_time_strl()
        
        headers = self.build_headers(self.real_charge_conf['headers'])
        req = request.Request(url, headers=headers)
        resp = self.opener.open(req)
        text = resp.read().decode('utf-8')
        ids = text.find('{')
        if ids > 0:
            content = text[ids:-2] 
            js = json.loads(content)
            return {
                "buy1": js['fivequote']['buy1'],
                "buy2": js['fivequote']['buy2'],
                "buy3": js['fivequote']['buy3'],
                "buy4": js['fivequote']['buy4'],
                "buy5": js['fivequote']['buy5'],
                "sale1":js['fivequote']['sale1'],
                "sale2":js['fivequote']['sale2'],
                "sale3":js['fivequote']['sale3'],
                "sale4":js['fivequote']['sale4'],
                "sale5":js['fivequote']['sale5'],
                "avg": js['realtimequote']['avg'],
                "currentPrice": js['realtimequote']['currentPrice'],
                "high": js['realtimequote']['high'],
                "low": js['realtimequote']['low'],
                "open": js['realtimequote']['open'],
                "zdf": js['realtimequote']['zdf'][:-1],
            }
        
        return None

    def get_can_buy_new_stock(self):
        url = self.get_can_buy_new_stock_conf['url'] + self.validatekey
        headers = self.build_headers(self.get_can_buy_new_stock_conf['headers'])
        data = {}

        js = self.http_post(url, data, headers)
        return js

    def get_bond_list(self):
        url = self.get_bond_list_conf['url'] + self.validatekey
        headers = self.build_headers(self.get_bond_list_conf['headers'])
        data = {}

        js = self.http_post(url, data, headers)
        if js['Status'] == 0:
            return js['Data']
        else:
            print("get bond list error:%s", js['Message'])
            return []

    
    def submit_bat_trade(self, para):
        url = self.submit_bat_trade_conf['url'] + self.validatekey
        headers = self.build_headers(self.submit_bat_trade_conf['headers'])
        data = json.dumps(para).encode(encoding='utf-8')
        js = self.http_post(url,data,headers,raw=True)
        return js
    
    def get_asset(self):
        url = self.get_asset_conf['url'] + self.validatekey
        headers = self.build_headers(self.get_asset_conf['headers'])
        data = {}
        js = self.http_post(url, data, headers)

        return js["Status"], js['Data']

    def get_ttb_code(self):
        url = self.ttb_code_conf['url']
        headers = self.build_headers(self.ttb_code_conf['headers'])
        req = request.Request(url, headers=headers)
        resp = self.opener.open(req)
        text = resp.read().decode('utf-8')
        id = text.find("jjdm:")
        
        if id == -1:
            print("get ttb code error.")
            return False, None, None
        else:
            jjdm = text[id + 7: id + 13]
            id = text.find("jjgs:")
            jjgs = text[id + 7: id + 9]
            return True, jjdm, jjgs

    def get_ttb_yield(self, jjdm, jjgs):
        url = self.ttb_yield_conf['url'] + get_time_strl() + "&jjgs=" + jjgs + "&jjdm=" + jjdm
        headers = self.build_headers(self.ttb_yield_conf['headers'])
        req = request.Request(url, headers=headers) 
        resp = self.opener.open(req)
        text = resp.read().decode('utf-8')
        js = json.loads(text)
        if js["Status"] == 0:
            self.ttb_yield = js["Data"][0]["Qrnhsy"]
            return self.ttb_yield
        else:
            print("get ttb yield error %s",js['Message'])
            return None

    def get_bond_code(self):
        url = self.bond_code_conf['url']
        headers = self.build_headers(self.bond_code_conf['headers'])
        data = {}

        js = self.http_post(url, data, headers)
        if js["Status"] == 0:
            return js["Data"]
        else:
            print("get bond code error %s" % js['Message'])
            return []

    def get_bond_days(self, code, market):
        url = self.bond_days_conf['url'] + self.validatekey
        headers = self.build_headers(self.bond_days_conf['headers'])

        data = {
            "zqdm": code,
            "market": market
        }
        js = self.http_post(url, data, headers)
        if js["Status"] == 0:
            return int(js["Data"][0]["Jxdays"])
        else:
            return None

    def get_bond_yield(self, code):
        url = self.bond_yield_conf['url'] + get_time_strl() + "&id=" +code + "&dm=" + get_time_strl() + "&_=" + get_time_strl()
        headers = self.build_headers(self.bond_yield_conf['headers'])

        req = request.Request(url, headers=headers) 
        resp = self.opener.open(req)
        text = resp.read().decode('utf-8')
        id = text.find("{")
        if id != -1:
            js = json.loads(text[id:-2])
            return True, float(js['realtimequote']["currentPrice"]), float(js["realtimequote"]['zdf'][:-1]), js['realtimequote']['time']
        else:
            return False, None, None, None
    
    def lending_bond(self, code, price, vol):
        url = self.lending_bond_conf['url'] + self.validatekey
        headers = self.build_headers(self.lending_bond_conf['headers'])

        data = {
            "zqdm": code,
            "rqjg": price,
            "rqsl": vol
        }

        js = self.http_post(url, data, headers)
        if js["Status"] == 0:
            return js['Data'][0]['Wtbh']
        else:
            print("lend bond error. %s" % js["Message"])
            return None