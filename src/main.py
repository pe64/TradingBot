import sys
import json
import time
import datetime
#from EastMoney import EastMoney

from threading import Thread
from cta.fund51_cta import Fund51Cta
from conf.yaml_conf import yaml_load
from http_opt import fund_http
from http_opt import stock_http
from db.sqlite import SqliteObj
from crypto.rsa_crypto import JSEncrypt
from cta.virtual_cta import VirtualCta
from http_opt.fund51_http import HttpFund51
from http_opt.eastmoney import HttpEM
from cta.eastmoney_cta import EastMoneyCta
from ocr.ocr import *

def fund51_cta_daemon(*add):
    cf = yaml_load()
    print("start fund51 cta.")
    #while True:
        #now = datetime.datetime.now()
        #if now.hour == 14 and now.minute == 40:
    print("exec fund fund51")
    cta51 = Fund51Cta(cf)
    cta51.custom_policy()
    
    time.sleep(60)


def main(argv):

    cf = yaml_load()
    if argv[1] == "update": 
        if argv[2] == "real":
            pass
        elif argv[2] == "history":
            fund_sq = SqliteObj(cf["sqlite_path"]["fund"])
            stock_sq = SqliteObj(cf["sqlite_path"]["stock"])
            fcodes = fund_sq.get_fund_self_selections()
            for fcode in fcodes:
                his = fund_http.fund_http_history_charge(cf["web_api"]["fund"], fcode[0])
                fund_sq.insert_fund_history_charges(his, fcode=fcode[0])
                js = fund_http.fund_http_real_time_charge(cf["web_api"]["fund"],fcode[0])
                fund_sq.update_fund_real_time_charge(fcode[0], json.loads(js))

            stocks = stock_sq.get_stock_self_selection()
            for stock in stocks:
                scode = cf["web_api"]["stock"]["market"][stock[1]] + "." + stock[0]
                his = stock_http.stock_http_history_charge(cf["web_api"]["stock"], scode)
                stock_sq.insert_stock_history_charge(his["data"]["klines"], stock[0])

            pass
        pass
    elif argv[1] == "virtualcta":
        vc = VirtualCta("conf/cta.yaml")
        vc.cta_run()
        pass

    elif argv[1] == "rsa":
        inc = JSEncrypt(cf["fund51"]["login"]["private_key"])
        #key = ""
        #value = ""
        #with open(cf["web_api"]["fund"]["cta_api"]["private_key"], "r") as f:
        #    key = f.read()
        with open(cf["web_api"]["fund"]["cta_api"]["arguments"], "r") as f:
            value = f.read().encode('utf-8')
            value = json.loads(value)
            value = json.dumps(value)
        inc.rsa_long_encrypt(value, length=100)
        #crypt_text = rsa_long_encrypt(key, value, length=100)
        #print(crypt_text)
    
    elif argv[1] == "login":
        f51 = HttpFund51(cf)
        f51.login_fund51_ver_code()
        f51.login_fund51_platform()
        ret, vol = f51.get_balance()
        print(vol)
        ret = f51.get_account_status()
        for r in ret['currentShareList']:
            f51.redem_fund(r, "20")
        #result = f51.get_account_id("003096")
        #order = f51.buy_fund(result, 24.00)
        #node = f51.get_current_order()
        #node1 = f51.get_order_by_id(order)
        node1 = f51.get_orders_can_back()
        for n in node1:
            buyorder = f51.get_buy_order(n['appSheetSerialNo'])
            f51.revoke_order(buyorder)
        pass
    elif argv[1] == "ocr":
        ocr_fund51("cache/fund51.png")
    
    elif argv[1] == "fund51":
        cta51 = Fund51Cta(cf)
        cta51.custom_policy()

    elif argv[1] == "daemon":
        fund51_cta_daemon()
        pass
    
    elif argv[1] == "east":
        #em=EastMoney('000651','SZ')
        #ret = em.getPrice()
        em = HttpEM(cf, 0)
        em.login_em_ver_code()
        em.login_em_platform()
        em.get_validate_key()
        em.get_stock_real_charge("601166", "SH")
        #em.check_sdx("001632")
        #em.check_status("001632")
        #em.sign_contract("001632")
        #em.fund_submit_trade("004753", 10)
        #orders = em.get_revoke_list()
        #for order in orders:
        #    em.revoke_orders(order["Jjdm"] + "_" + order['Wtbh'] + "_" + order["Wtrq"])
        #orders = em.get_fund_position()
        #orders = em.stock_get_revokes()
        #for order in orders:
        #    em.stock_revoke_order(order["Wtrq"]+"_"+order['Wtbh'])
        orders = em.stock_submit_trade("601166","兴业银行","17.18","100","HA")
    elif argv[1] == "eastcta":
        emcta= EastMoneyCta(cf)
        while True:
            emcta.cta_run()
            time.sleep(120)
        



    #    sqlite.insert_fund_table

    #key = ""
    #value = ""
    #with open(cf["web_api"]["fund"]["cta_api"]["private_key"], "r") as f:
    #    key = f.read()

     #    value = f.read().encode('utf-8')
   
    #    value = json.loads(value)
    #    value = json.dumps(value)
    #crypt_text = rsa_long_encrypt(key, value)


    #    vc = VirtualCta(cf["sqlite_path"]["stock"], "stock", stock[0], "2021-12-31", "2022-08-12")
    #    policy = StealBuy(stock[0], 100000, vc.get_start_charge(), 0.07, 0, 10000, vc)
    #    ret = vc.cta_run(stock[0], policy)
    #    print(ret)


    #"2022-08-23 ,27.31 ,27.39 ,27.50 ,27.15 ,123497,337263045.00,1.28,0.44,0.12,1.38"
    #"日期 开盘价 收盘价 最高价 最低价 成交量 成交额 振幅 涨幅 - 换手率"

    pass

def help():
    pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        help()
        sys.exit()

    main(sys.argv)