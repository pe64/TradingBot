import datetime
from asyncore import loop
from email import header
from threading import get_ident
import time
import json
from urllib import request,parse
from http import cookiejar
from crypto.rsa_crypto import JSEncrypt
from ocr.ocr import ocr_fund51

def get_time_strl():
    return str(int(time.time() * 1000))

def get_time_day():
    return time.strftime("%Y%m%d", time.localtime())

class HttpFund51:
    def __init__(self, cf) -> None:
        #self.cookie = cookiejar.CookieJar() 
        #self.cookie = cookiejar.MozillaCookieJar(cf["fund51"]["cookie"])
        self.cookie = cookiejar.LWPCookieJar(cf["fund51"]["cookie"])
        #self.cookie = cookiejar.LWPCookieJar()
        self.cookie.load(ignore_expires=True,ignore_discard=True)
        #self.cookie.save(ignore_discard=True, ignore_expires=True)
        self.cookie_handler = request.HTTPCookieProcessor(self.cookie)
        self.opener = request.build_opener(self.cookie_handler)
        self.ver_conf = cf["fund51"]["ver_code"]
        self.login_conf = cf["fund51"]["login"]
        self.balance_conf = cf["fund51"]["balance"]
        self.status_conf = cf["fund51"]["status"]
        self.countid_conf = cf['fund51']['countid']
        self.buyfund_conf = cf['fund51']["buyfund"]
        self.checktime_conf = cf['fund51']['checktime']
        self.checkpwd_conf = cf['fund51']['checkpwd']
        self.order_conf = cf["fund51"]["order"]
        self.buyorder_conf = cf['fund51']['buyorder']
        self.revoke_conf = cf["fund51"]['revoke']
        self.redem_conf = cf['fund51']['redem']
        self.autobuy_order_conf = cf['fund51']['autobuy_order']
        self.headers = cf["fund51"]["headers_comm"]
        self.timestr = str(int(time.time()))
        with open(self.login_conf["arguments"]) as f:
            content = f.read()
        self.login_js = json.loads(content)
        self.password = self.login_js["tradePassword"]
        pass

    def build_headers(self, conf_head):
        headers = {}
        for item in self.headers:
            sp = item.split(':', 1)
            headers[sp[0]] = sp[1].strip()
        for item in conf_head:
            sp = item.split(':', 1)
            headers[sp[0]] = sp[1].strip()
        return headers

    def login_fund51_ver_code(self):
        code_path = self.ver_conf["file"]

        url = self.ver_conf["url"] + \
            "?d=" + get_time_strl()
        headers = self.build_headers(self.ver_conf["headers"])
        req = request.Request(url, headers=headers)
        #resp = request.urlretrieve(url, code_path)
        while(1):
            resp = self.opener.open(req)
            text = resp.read()
            with open(code_path, "wb") as f:
                f.write(text)
            self.ver_code = ocr_fund51(code_path)
            if self.ver_code != None and len(self.ver_code) == 6:
                break
            else:
                print("ver_code error [%s]."%self.ver_code)
                time.sleep(30)
        #text = resp.read().decode('utf-8')

    def login_fund51_platform(self):
        url = self.login_conf['url']
        headers = self.build_headers(self.login_conf["headers"])
        self.login_js["rand"] = str(self.ver_code).strip()
        value = json.dumps(self.login_js)
        rsa = JSEncrypt(self.login_conf["private_key"])
        value = rsa.rsa_long_encrypt(value)
        data = {
            "taccoCustAcco.encryptLoginInfo" : value,
            "taccoCustAcco.fromIndex": "1"
        }
        data = parse.urlencode(data).encode('utf-8')
        req = request.Request(url, method="POST",data=data, headers=headers)
        #self.cookie.load(ignore_expires=True,ignore_discard=True)
        #self.cookie_handler = request.HTTPCookieProcessor(self.cookie)
        #self.opener = request.build_opener(self.cookie_handler)
        resp = self.opener.open(req)
        #resp = request.urlopen(req)
        ret = resp.read().decode('utf-8')
        js = json.loads(ret)
        if js["code"] == '0000':
            print("login success.")
            self.cookie.save(ignore_discard=True, ignore_expires=True)
            return True,"success"
        else :
            print("login error [%s]"%js["message"])
            return False, js["message"]

    def get_balance(self):
        url = self.balance_conf["url"] + "?" +"_="+get_time_strl()
        headers = self.build_headers(self.balance_conf["headers"])
        req = request.Request(url, headers=headers)
        resp = self.opener.open(req)    
        ret = resp.read().decode('utf-8')
        js = json.loads(ret)
        if js["code"] == "0000":
            return True, js["singleData"]["sumAvailablevol"]
        elif js["code"] == "LT99":
            print('get_balance error [%s]', js['message'])
            pass
        else:
            return False, js["message"]

    def get_account_status(self):
        url = self.status_conf["url"] + "?" + "_=" + get_time_strl()
        headers = self.build_headers(self.status_conf["headers"])
        req = request.Request(url, headers=headers)
        resp = self.opener.open(req)    
        ret = resp.read().decode('utf-8')
        js = json.loads(ret)
        if js["code"] == "0000":
            print('get account status success.')
            return js['singleData']
        else :
            print("get account status error [%s:%s]"%(js['code'],js['message']))
    
    def get_account_id(self, fcode):
        url = self.countid_conf["url"] + "?" + "fundCode=" + fcode + "&" + "_=" + get_time_strl()
        headers = self.build_headers(self.countid_conf['headers'])
        req = request.Request(url, headers=headers)
        resp = self.opener.open(req)
        ret = resp.read().decode('utf-8')
        js = json.loads(ret)
        if js['code'] != "0000":
            print('get account id error.')
            return None

        if self.check_time_work() and self.check_password(js['custId']):
            return {"codeOfTargetFund": fcode,
                    "targetShareType": js['singleData']['pcBuyInitResult'][0]["shareType"],
                    "fundName": js['singleData']['pcBuyInitResult'][0]["fundName"],
                    "taCode": js['singleData']['pcBuyInitResult'][0]["taCode"], 
                    "transActionAccountId": js['listData'][0]["transActionAccountId"], 
                    "tradePassword": self.password,
                    "userName": js['custId'], 
                    "fundCode": js['singleData']['fundtzeroList'][0]['fundCode'],
                    "fundType": js['singleData']['pcBuyInitResult'][0]["fundType"],
                    "shareType": js['singleData']['pcBuyInitResult'][0]["shareType"],
                    "bankFundNo": js['singleData']['fundtzeroList'][0]['bankFundNo'],
                    "spUser": js['singleData']['fundtzeroList'][0]['spUser']
                    }

    def check_password(self, custId):
        url = self.checkpwd_conf['url']
        headers = self.build_headers(self.checkpwd_conf['headers'])
        data = {
            "custId" : custId,
            "tradePassword" : self.password
        }
        data = parse.urlencode(data).encode('utf-8')
        req = request.Request(url, method="POST", data=data, headers=headers)
        resp = self.opener.open(req)
        ret = resp.read().decode('utf-8')
        js = json.loads(ret)
        if js['code'] == "0000":
            print("check password success.")
            return True
        else:
            print("check password error [%s:%s]."%(js['code'], js["message"]))
            return False

    def check_time_work(self):
        url = self.checktime_conf['url']
        headers = self.build_headers(self.checktime_conf['headers'])
        req = request.Request(url, headers=headers)
        resp = self.opener.open(req)
        ret = resp.read().decode('utf-8')
        js = json.loads(ret)
        if js['ovRETCODE'] == '0000':
            return True
        else:
            return False

    def buy_fund(self, data, money):
        url = self.buyfund_conf['url']
        data["totalUsableVolText"] = str(money)
        arg = json.dumps(data)
        headers=self.build_headers(self.buyfund_conf["headers"])
        puts = {"rsZcDto": arg}
        puts = parse.urlencode(puts).encode('utf-8')
        req = request.Request(url, method="POST", data=puts, headers=headers)
        
        resp = self.opener.open(req)
        ret = resp.read().decode('utf-8')
        js = json.loads(ret)
        if js['code'] == '0000':
            print('buy fund success.')
            return js['singleData']
        else:
            print("buy fund error [%s:%s]"%(js['code'],js['message']))
            return []
    
    def get_current_order(self):
        url = self.order_conf['url'] + "?" + "_=" + get_time_strl()
        headers = self.build_headers(self.order_conf['headers'])
        req = request.Request(url, headers=headers)
        resp = self.opener.open(req)
        ret = resp.read().decode('utf-8')
        js = json.loads(ret)
        if js['code'] == '0000':
            print('get current order success.')
            return js['listData']
        else:
            print('get current error [%s:%s]'%(js['code'], js['message']))
            return []
    
    def get_order_by_id(self, order):
        orders = self.get_current_order()
        for ord in orders:
            if order == ord['appSheetSerialNo']:
                return ord
    
    def get_orders_can_back(self):
        orders = self.get_current_order()
        can_backs = []
        today = time.strftime("%Y.%m.%d", time.localtime())
        now = datetime.datetime.now()

        for order in orders:
            if order['cancelflag'] != "1" or (now.hour < 15 and order["transActionDate"] == today):
                can_backs.append(order)

        return can_backs

    def get_buy_order(self, order):
        url = self.buyorder_conf['url'] + '?' + "appsheetserialno=" + \
            order + "&offer=1&limit=1&_=" + get_time_strl()
        headers = self.build_headers(self.buyorder_conf['headers'])
        req = request.Request(url, headers=headers)
        resp = self.opener.open(req)
        ret = resp.read().decode('utf-8')
        js = json.loads(ret)
        if js['code'] == "0000":
            print('get buy order success.')
            return js['singleData']['ov_cursor'][0]
        else:
            print('get buy order error'%(js['code'], js['message']))
            return None

    def get_autobuy_order(self, limit, fcode):
        url = self.autobuy_order_conf["url"] + "?" + \
            "offer=1&" + "limit=" + str(limit) + "&fundCode=" + fcode + "&_=" + get_time_strl()
        headers = self.build_headers(self.autobuy_order_conf['headers'])
        req = request.Request(url, headers=headers)
        resp = self.opener.open(req)
        ret = resp.read().decode('utf-8')
        js = json.loads(ret)
        if js["code"] == "0000":
            print("get autobuy seccess.")
            return js['singleData']['ov_cursor']
        else:
            print('get autobuy order error [%s:%s]'%(js["code"], js['message']))
            return None

    def revoke_order(self, order):
        url = self.revoke_conf['url'] 
        headers = self.build_headers(self.revoke_conf['headers'])

        data = {
            "transActionAccountId": order["vc_transactionaccountid"],
            "capitalMethod": order["capitalmethod"],
            "revokeAppSheetNo": order['vc_appsheetserialno'],
            "businessCode": order['vc_businesscode'],
            "checkFlag": order['c_checkflag'],
            "tradePassword": self.password
        }

        data = json.dumps(data)
        puts = {
            "strPCRevokeDTO": data,
        }
        puts = parse.urlencode(puts).encode('utf-8')
        req = request.Request(url, method="POST", data=puts, headers=headers) 
        resp = self.opener.open(req)
        ret = resp.read().decode('utf-8')
        js =json.loads(ret)
        if js['code'] == "0000":
            print("revoke success.")
            pass
        else:
            print("revoke error [%s:%s]"%(js['code'], js["message"]))

    def redem_fund(self, fund, vol):
        url = self.redem_conf['url']
        headers = self.build_headers(self.redem_conf['headers'])
        if vol == None:
            vol =fund["currentValueText"]  
        data = {
            "transActionAccountId": fund["transActionAccountId"],
            "fundName": fund["fundName"],
            "shareType": fund["shareType"],
            "totalUsableVolText": fund["currentValueText"],
            "fundCode": fund["fundCode"],
            "largeRedemptionSelect": "1",
            "money": vol,
        }

        pwd = {
            "tradePassword": self.password
        }

        js_pwd = json.dumps(pwd)
        js_data = json.dumps(data)


        rsa = JSEncrypt(self.login_conf["private_key"])
        puts = {
            "strPCShareDTO": js_data,
            "pcShareRedemption": rsa.rsa_long_encrypt(js_pwd)
        }

        puts = parse.urlencode(puts).encode('utf-8')
        req = request.Request(url, method="POST", data=puts, headers=headers) 
        resp = self.opener.open(req)
        ret = resp.read().decode('utf-8')
        js =json.loads(ret)
        if js['code'] == "0000":
            print("redem fund success.")
        else:
            print('redem fund error [%s:%s]'%(js['code'], js['message']))