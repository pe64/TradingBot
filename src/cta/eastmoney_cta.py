import time
import json
import sys
import datetime 
from http_opt.eastmoney import HttpEM
from db.account_db import AccountDB
from http_opt.fund_http import fund_http_real_time_charge
from policy.policy import Policy
from utils.redis import Redis

def time_last_nday(date, days):
    ret = (datetime.datetime.strptime(date, "%Y-%m-%d") + 
            datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    return ret

class EastMoneyCta:
    def __init__(self, cf) -> None:
        self.em = []
        self.em_sq = AccountDB(cf['sqlite_path'])
        self.accounts = self.em_sq.get_eastmoney_accounts()
        #for account in self.accounts:
        #    self.em.append(HttpEM(cf, account['arg'], account['id']))
        self.redis_client = Redis(cf)
        self.gconf=cf
        self.policy = []
        self.today = time.strftime("%Y%m%d", time.localtime())
        self.init_flag = 0
        self.new_asset_flag = 0
        self.ttb_yield = 0
        pass
    
    def get_accounts(self):
        return self.accounts

    def run(self, account):
        ret = False
        aid = account['id']
        htp = HttpEM(self.gconf, account)
        while False == htp.get_validate_key():
            htp.update_cookie()
            time.sleep(10)
            continue

        while True:
            _, message = self.redis_client.Subscribe(
                "left#trade#" + str(aid)
            )
            order = json.loads(message)
            if order['trade'] == 'UPDATE':
                htp.update_cookie()
                continue

            asset_str = self.redis_client.GetAssetById(order['asset_id'])
            asset = json.loads(asset_str)

            if order['trade'] == 'SELL':
                if asset['type'] == 'fund':
                    if order['type'] == 'cash':
                        cash = order['quantity']
                        quantity = order['quantity'] / order['price']
                    else:
                        cash = order['quantity'] * order['price']
                        quantity = order['quantity']

                    ret, contract = self.sale_fund(htp, order['symbol'], quantity, asset['market'])
                pass
            elif order['trade'] == 'BUY':
                if asset['type'] == 'fund':
                    if order['type'] == 'cash':
                        cash = order['quantity'] 
                        quantity = cash / order['price']
                    else:
                        cash = order['quantity'] * order['price']
                        quantity = order['quantity']
                    ret, contract = self.buy_fund(htp, order['symbol'], cash)
                pass
                
            else:
                htp.update_cookie()
                #self.update_account_status(htp)
            
            if ret is True:
                ret_msg = {
                    'status': "FILLED",
                    'orderId': contract,
                    'origQty': quantity,
                    'executedQty': quantity,
                    'cummulativeQuoteQty': cash
                }
            else:
                ret_msg = {
                    "status": "EXPIRED"
                }
            self.redis_client.LPush(
                "right#trade#" + str(aid),
                json.dumps(ret_msg)
            )
            
    def get_policy_obj_by_id(self, pid):
        for p in self.policy:
            if pid == p.get_policy_id():
                return p

        return None
    
    def update_policy(self, em):
        for policy in self.em_sq.get_account_policy(em.account_id):
            asset = self.em_sq.get_asset_by_id(policy['asset_id'])
            contracts = self.em_sq.get_his_deals_by_step_and_policy(1, em.account_id, policy['id'], asset['code'])
            for contract in contracts:
                if contract['direction'] == "111":
                    p = self.get_policy_obj_by_id(policy['id'])
                    if p is not None:
                        asset_count = p.add_asset_count(float(contract['vol']))
                        cash_into = p.add_cash_into(float(contract['cash']))
                        self.em_sq.update_policy_asset_count(policy['id'], round(asset_count,2), round(cash_into, 2))
                        self.em_sq.update_his_deals_step(contract['contract_id'], 2)
                        print("\033[36m更新合约[%s]信息成功.\033[0m"%contract['contract_id'])
                elif contract['direction'] == '112':
                    p = self.get_policy_obj_by_id(policy['id'])
                    if p is not None:
                        #TODO:
                        pass

    def init_policy(self, em):
        for policy in self.em_sq.get_account_policy(em.account_id):
            asset = self.em_sq.get_asset_by_id(policy['asset_id'])

            if len(asset) == 0:
                continue
            policy['asset_id'] = asset['code']
            p = Policy(policy, self) 
            self.policy.append(p)
            print("\033[34m账户:%s 策略:%s 剩余现金:%s元 已投入金额:%s元 目标资产:%s.\033[0m"%(em.get_user_id(), p.name, policy['cash'].center(8), policy['cash_inuse'].center(8), asset['name']))
        pass

    def check_policy_update_time(self):
        st = datetime.datetime.strptime(str(datetime.datetime.now().date()) + self.gconf['period']['check_fund']['start'], '%Y-%m-%d%H:%M')
        et = datetime.datetime.strptime(str(datetime.datetime.now().date()) + self.gconf['period']['check_fund']['end'], '%Y-%m-%d%H:%M')
        now_time = datetime.datetime.now()

        return now_time > st and now_time < et
    
    def get_ttb_yield(self,em):
        ret, dm, gs = em.get_ttb_code()
        if ret is True:
            ttb_yield = em.get_ttb_yield(dm, gs)
            return float(ttb_yield)
        else:
            return None

    def login(self):
        for em in self.em:
            while False== em.get_validate_key():
                em.login_em_ver_code()
                em.login_em_platform()

            if self.init_flag < len(self.em):
                print("\033[33m账户:%s 登陆成功\033[0m"%(em.get_user_id()),end="|")
                ret = em.get_asset()
                ttb_yield = self.get_ttb_yield(em)
                print("\033[33m 货币基金收益率 %s %%\033[0m"%(ttb_yield),end="|")
                self.ttb_yield = max(self.ttb_yield, ttb_yield)
                for node in ret:
                    if node['Ljyk'] is None:
                        print("\033[33m总资产:%s元,可用金额:%s元,持仓盈亏:0元.\033[0m"%(node['Zzc'],node['Kyzj'])) 
                    elif float(node['Ljyk']) > 0:
                        print("\033[33m总资产:%s元,可用金额:%s元,持仓盈亏:\033[32m%s\033[33m元.\033[0m"%(node['Zzc'],node['Kyzj'],node['Ljyk'])) 
                    elif  float(node['Ljyk']) < 0:
                        print("\033[33m总资产:%s元,可用金额:%s元,持仓盈亏:\033[31m%s\033[33m元.\033[0m"%(node['Zzc'],node['Kyzj'],node['Ljyk'])) 

                self.update_account_status(em)
                #self.init_policy(em)
                #self.update_policy(em)
                self.init_flag = self.init_flag + 1
            
            if self.check_policy_update_time():
                self.update_account_status(em)
                self.update_policy(em)
            
            if self.check_new_submit_new_asset_time() and self.new_asset_flag < len(self.em):
                self.submit_new_asset(em)
                self.new_asset_flag = self.new_asset_flag + 1
            


    def check_new_submit_new_asset_time(self):
        st = datetime.datetime.strptime(str(datetime.datetime.now().date()) + self.gconf['period']['new_asset']['start'], '%Y-%m-%d%H:%M')
        et = datetime.datetime.strptime(str(datetime.datetime.now().date()) + self.gconf['period']['new_asset']['end'], '%Y-%m-%d%H:%M')
        now_time = datetime.datetime.now()

        return now_time > st and now_time < et

    def submit_new_asset(self, em):
        stock = []
        bond = []

        ret = em.get_can_buy_new_stock()
        for node in ret['NewStockList']:
            if int(node['Ksgsx']) > 0:
                p = {
                    "StockCode":node['Sgdm'],
                    "StockName":node['Zqmc'],
                    "Price":node['Fxj'],
                    "Amount":node['Ksgsx'],
                    "TradeType":"B",
                    "Market":node['Market']
                }
                stock.append(p)

        if len(stock) > 0:
            js = em.submit_bat_trade(stock)
            print("新股申购:",js['Message'])
        else:
            print("今日无新股可申购.")

        ret = em.get_bond_list()
        for node in ret:
            if node['ExIsToday'] is True:
                b = {
                   "StockCode": node['SUBCODE'],
                   "StockName": node['SUBNAME'],
                   "Price": node['PARVALUE'],
                   "Amount": node['LIMITBUYVOL'],
                   "TradeType":"B",
                   "Market": node['Market']
                }
                bond.append(b)

        if len(bond) > 0:
            js = em.submit_bat_trade(bond)
            print("新债申购:", js["Message"])
        else:
            print("今日无新债可申购.")

        return ret

    def update_account_status(self, em):
        r_dic = {}
        today = time.strftime("%Y-%m-%d", time.localtime())
        st = time_last_nday(today, -7)
        records = em.fund_get_his_deals(st, today)
        for record in records:
            r_dic[record['Wtbh']] = record
            pass

        if len(r_dic) == 0:
            return
        
        contracts = self.em_sq.get_his_deals_contract_by_step(0, em.account_id)
        for contract in contracts:
            if contract in r_dic:
                record = r_dic.get(contract)
                self.em_sq.update_his_deals_vol(contract, record['Cjfe'], record['Cjrq'])
    
    def cta_run(self):
        self.login()
        funds = self.em_sq.get_fund_self_selection() 
        self.today = time.strftime("%Y%m%d", time.localtime())
        for fund in funds:
            ret = fund_http_real_time_charge(self.gconf['web_api']['fund'], fund['code']).get("Expansion")
            if len(ret['GSZZL']) !=0:
                today = time.strftime("%Y%m%d",time.strptime(ret['GZTIME'], "%Y-%m-%d %H:%M"))
                para = {
                    "type": "fund",
                    "code": fund['code'],
                    "price": ret['GZ'],
                    "percent": float(ret['GSZZL']),
                    "today": today
                }
                for p in self.policy:
                    p.execute(para)
        
        stocks = self.em_sq.get_stock_self_selection()
        for stock in stocks:
            ret = self.em[0].get_stock_real_charge(stock['code'], stock['market'])
            if ret is not None:
                para = {
                    "type": "stock",
                    "code": stock['code'],
                    "price": float(ret['currentPrice']),
                    "percent": float(ret['zdf']),
                    "today": self.today
                }
                for p in self.policy:
                    p.execute(para)
        bond_dic = {}
        if self.check_stock_time():
            for em in self.em:
                bonds = em.get_bond_code()
                for bond in bonds:
                    days = em.get_bond_days(bond['Zqdm'], bond['Market'])
                    ret, price, zdf, now = em.get_bond_yield(bond['Zqdm'])
                    para = {
                        "type": "bond",
                        "code": bond["Zqdm"],
                        "market": bond["Market"],
                        "percent": zdf,
                        "price": price,
                        "limit_days":days,
                        "today":self.today,
                        "ttb_yield": self.ttb_yield
                    }
                    for p in self.policy:
                        p.execute(para)

                    if price - self.ttb_yield > self.gconf['eastmoney']['bond']['diff'] and self.check_stock_time(now):
                        if bond_dic.get(days) is not None:
                            if bond_dic[days]["price"] > price:
                                continue
                            else:
                                bond_dic[days] = {
                                    "code": bond['Zqdm'],
                                    "days": days,
                                    "zdf": zdf,
                                    "price": price
                                    }

                        else:
                            bond_dic[days] = {
                                "code": bond['Zqdm'],
                                "days": days,
                                "zdf": zdf,
                                "price": price
                            }
        
        for key in bond_dic:
            print("%s 国债[%s] 占用天数: %s, 年化收益率: %s %%"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),bond_dic[key]["code"], bond_dic[key]['days'], bond_dic[key]['price']))
        #print(".", end="")
        sys.stdout.flush()

    def buy_fund(self, em, code, vol):
        try:
            em.check_sdx(code)
            em.check_status(code, None)
            em.sign_contract(code)
            contract = em.fund_submit_trade(code, vol, "buy")
            if contract is None:
                return False, ""
            return True, contract
        except:
            return False, ""
    
    def sale_fund(self, em, code, vol, company):
        try:
            em.check_status(code, company)
            return True, em.fund_submit_trade(code, vol, "sale")
        except:
            return False, ""

    def check_stock_time(self, now=None):
        if now is None:
            now_time = datetime.datetime.now()
        else:
            tmp = str(datetime.datetime.now().date()) + now
            now_time = datetime.datetime.strptime(tmp, '%Y-%m-%d%H:%M:%S')
        st1 = datetime.datetime.strptime(str(now_time.date()) + self.gconf['period']['trading_stock']['start1'], '%Y-%m-%d%H:%M')
        et1 = datetime.datetime.strptime(str(now_time.date()) + self.gconf['period']['trading_stock']['end1'], '%Y-%m-%d%H:%M')
        st2 = datetime.datetime.strptime(str(now_time.date()) + self.gconf['period']['trading_stock']['start2'], '%Y-%m-%d%H:%M')
        et2 = datetime.datetime.strptime(str(now_time.date()) + self.gconf['period']['trading_stock']['end2'], '%Y-%m-%d%H:%M')

        return (now_time > st1 and now_time < et1) or (now_time > st2 and now_time < et2)

    def check_fund_time(self):
        st = datetime.datetime.strptime(str(datetime.datetime.now().date()) + self.gconf['period']['trading_fund']['start'], '%Y-%m-%d%H:%M')
        et = datetime.datetime.strptime(str(datetime.datetime.now().date()) + self.gconf['period']['trading_fund']['end'], '%Y-%m-%d%H:%M')
        now_time = datetime.datetime.now()

        return now_time > st and now_time < et

    def check_order_success(self, em, order):
        flags = False
        ret = True
        for times in range(1,3):
            contracts = em.get_deal_data()
            if order in contracts:
                flags = True
                break
            times = times + 1
            time.sleep(5)

        if flags == False:
            ret = em.stock_revoke_order(order)
        
        return flags == True or ret == False


    def buy_stock(self, em, code, price, vol):
        ret = False
        asset = self.em_sq.get_asset_by_code(code)

        if asset['market'] == "SH":
            order = em.stock_submit_trade(code,asset['name'],price,vol,"HA","B")
        elif asset['market'] == "SZ":
            order = em.stock_submit_trade(code,asset['name'],price,vol,"SA","B")

        if order is not None:
            ret = self.check_order_success(em, order)
        
        if ret is False:
            order = None

        return ret, order
    
    def sale_stock(self, em, code, price, vol):
        ret = False
        asset = self.em_sq.get_asset_by_code(code)
        if asset['market'] == "SH":
            order = em.stock_submit_trade(code, asset['name'], price, vol, "HA", "S")
        elif asset['market'] == "SZ":
            order = em.stock_submit_trade(code, asset['name'], price, vol, "SA", "S")
        
        if order is not None:
            ret = self.check_order_success(em, order)
        
        if ret is False:
            order = None
        
        return ret, order

    def sale_asset(self, para):
        ret = False
        for em in self.em:
            if em.account_id != para['account_id']:
                continue
            asset = self.em_sq.get_asset_by_code(para['code'])
            contract = None
            if asset['type'] == "f" and self.check_fund_time():
                vol = para['vol']
                cash = para['vol'] * para['price']
                contract = self.sale_fund(em, para['code'], para['vol'], asset['market'])
            elif asset['type'] == "s" and self.check_stock_time():
                cash, vol = self.calc_asset(para['vol'], para['price'])
                ret, contract = self.sale_stock(em, para['code'], para['price'], vol)

            if contract is None:
                cash = 0
                vol = 0
                continue
            
            if asset['type'] == "f":
                self.em_sq.insert_his_deals(contract, em.account_id, para['policy_id'], para['code'], "112", para['vol'], self.today)
            elif asset['type'] == "s":
                self.em_sq.insert_his_deals(contract, em.account_id, para['policy_id'], para['code'], "112", para['vol'], self.today, step=2) 

            print("\033[31m%s 账户:%s 触发卖出[%s:%s]条件，卖出%s份.\033[0m"%
                (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), em.get_user_id(),asset['code'], asset['name'], para['vol']))
            ret = True

        return ret, cash, para['vol'] - vol
    
    def calc_asset(self, vol, price):
        sell_num = int(vol/100) * 100
        cash = round(sell_num * price, 2)

        return cash, sell_num
    
    def calc_price(self, buy_count, price):
        vol = int(buy_count/price/100)*100
        cash = buy_count - vol * price
        return cash,vol

    def buy_asset(self, para):
        ret = False
        vol = 0
        free_cash = 0
        
        for em in self.em:
            if em.account_id != para['account_id']:
                continue

            asset = self.em_sq.get_asset_by_code(para['code'])
            contract = None
            if asset['type'] == "f" and self.check_fund_time():
                ret, contract = self.buy_fund(em, para['code'], para['buy_count'])
            elif asset['type'] == "s" and self.check_stock_time():
                free_cash, vol = self.calc_price(para['buy_count'], para['price'])
                ret, contract = self.buy_stock(em, para['code'], para['price'], vol)

            if contract is None or ret is False:
                continue

            if asset['type'] == "f":
                self.em_sq.insert_his_deals(contract, em.account_id, para['policy_id'], para['code'], "111", para['buy_count'], self.today)
            elif asset['type'] == 's':
                self.em_sq.insert_his_deals(contract, em.account_id, para['policy_id'], para['code'], "111", para['buy_count']-free_cash, self.today, step=2)
                pass

            print("\033[32m%s 账户:%s 触发买入[%s:%s]条件，买入%s元.\033[0m"%
                (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), em.get_user_id(), asset['code'], asset['name'], para['buy_count']))

        
        return ret, free_cash, vol
    
    def update_policy_status(self, policy_id, cash_inuse, cash, asset_count, today, price=None):
        self.em_sq.update_policy_status(policy_id, cash_inuse, cash, asset_count, today, price)
        pass

    def lend_bond(self, para):
        price = para['price']
        vol = para['vol']
        code = para['code']
        account_id = para['account_id']
        for em in self.em:
            if em.account_id != account_id:
                continue

            #contract = em.lending_bond(code, price, vol/100)
            print("买入国债[%s] [%s] [%d]"%(code, price, vol))
            #if contract is not None:
            #    ret = self.check_order_success(em, contract)
            #    return ret
            #else:
            #    return False 
            pass
