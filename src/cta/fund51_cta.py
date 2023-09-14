from http_opt.fund51_http import HttpFund51
from http_opt.fund_http import fund_http_real_time_charge
from utils.yaml_conf import yaml_load

class Fund51Cta:
    def __init__(self, conf) -> None:
        self.gconf = conf
        self.handle = HttpFund51(conf)
        pass

    def custom_policy(self):
        self.login()
        today_order = self.handle.get_orders_can_back()
        hold = self.handle.get_account_status().get("currentShareList")
        for order in today_order:
            rate = 0.0
            for h in hold:
                if order['fundCode'] == h["fundCode"]:
                    rate = float(h["totalprofitlossText"]) / (float(h["availableVol"]) * float(h["navText"]) - float(h["totalprofitlossText"]) )
                    break
            
            ret = fund_http_real_time_charge(self.gconf['web_api']['fund'], order['fundCode']).get("Expansion")
            print("check %s . "%order['fundCode'])
            if (len(ret['GSZZL']) !=0 and float(ret['GSZZL']) > 0.5) or rate > 0.5:
                buyorder = self.handle.get_buy_order(order['appSheetSerialNo'])
                self.handle.revoke_order(buyorder)
                print("revoke %s."%(order['fundCode']))
            pass

        for h in hold:
            rate = (float(h["totalprofitlossText"]) / (float(h["availableVol"]) * float(h["navText"]) - float(h["totalprofitlossText"])))*100
            if rate > 15.0:
                records = self.handle.get_autobuy_order(7, h['fundCode'])
                cfm = 0
                for record in records:
                    if record['c_confirmflag'] != "1":
                        cfm = 1
                        break
                if cfm == 0:
                    self.handle.redem_fund(h, None)
            
            if rate > 0.5:
                records = self.handle.get_autobuy_order(25, h['fundCode'])
                cfm = 0
                for record in records:
                    if record['c_confirmflag'] != "1":
                        cfm = 1
                        break
                
                if cfm == 0:
                    self.handle.redem_fund(h, None)
    
    def login(self):
        ret = False
        while ret == False:
            self.handle.login_fund51_ver_code()
            ret, msg = self.handle.login_fund51_platform()
            print("login is %s"%ret)


if __name__ == "__main__":
    cf = yaml_load()
    cta51 = Fund51Cta(cf)
    cta51.custom_policy()