import time
import sys
import datetime 
from http_opt.eastmoney import HttpEM
from db.em_sqlite import SqliteEM
from http_opt.fund_http import fund_http_real_time_charge
from policy.policy import Policy

def time_last_nday(date, days):
    ret = (datetime.datetime.strptime(date, "%Y-%m-%d") + 
            datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    return ret

class EastMoneyCta:
    def __init__(self, cf) -> None:
        self.em = []
        self.em_sq = SqliteEM(cf['sqlite_path']['em'])
        accounts = self.em_sq.get_accounts()
        for account in accounts:
            self.em.append(HttpEM(cf, account['arg'], account['id']))
        self.gconf=cf
        self.policy = []
        self.today = time.strftime("%Y%m%d", time.localtime())
        self.init_flag = 0
        pass

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
                        asset_count = p.add_asset_count(contract['vol'])
                        cash_into = p.add_cash_into(contract['cash'])
                        self.em_sq.update_policy_asset_count(policy['id'], float(asset_count), float(cash_into))
                        self.em_sq.update_his_deals_step(contract['contract_id'], 2)
                        print("更新合约[%s]信息成功."%contract['contract_id'])
                elif contract['direction'] == '112':
                    p = self.get_policy_obj_by_id(policy['id'])
                    if p is not None:
                        #TODO:
                        pass

    def init_policy(self, em):
        for policy in self.em_sq.get_account_policy(em.account_id):
            asset = self.em_sq.get_asset_by_id(policy['asset_id'])
            #contracts = self.em_sq.get_his_deals_by_step_and_policy(1, em.account_id, policy['id'], asset['code'])
            #for contract in contracts:
            #    if contract['direction'] == "111":
            #        policy['asset_count'] = float(policy['asset_count']) + float(contract['vol'])
            #        policy['cash_into'] = float(policy['cash_into']) + float(contract['cash'])
            #        self.em_sq.update_policy_asset_count(policy['id'], policy['asset_count'], float(policy['cash_into']))
            #        self.em_sq.update_his_deals_step(contract['contract_id'], 2)

            if len(asset) == 0:
                continue
            policy['asset_id'] = asset['code']
            p = Policy(policy, self) 
            self.policy.append(p)
            print("账户:%s 策略:%s 剩余现金:%s元 已投入金额:%s元 目标资产:%s."%(em.get_user_id(), p.name, policy['cash'].center(8), policy['cash_inuse'].center(8), asset['name']))
        pass

    def check_policy_update_time(self):
        st = datetime.datetime.strptime(str(datetime.datetime.now().date()) + self.gconf['period']['check_fund']['start'], '%Y-%m-%d%H:%M')
        et = datetime.datetime.strptime(str(datetime.datetime.now().date()) + self.gconf['period']['check_fund']['end'], '%Y-%m-%d%H:%M')
        now_time = datetime.datetime.now()

        return now_time > st and now_time < et

    def login(self):
        for em in self.em:
            while False== em.get_validate_key():
                em.login_em_ver_code()
                em.login_em_platform()

            if self.init_flag == 0:
                print("账户:%s 登陆成功。"%(em.get_user_id()))
                self.update_account_status(em)
                self.init_policy(em)
                self.update_policy(em)
                self.init_flag = 1
            
            if self.check_policy_update_time():
                self.update_account_status(em)
                self.update_policy(em)
            
            if self.check_new_submit_new_asset_time():
                self.submit_new_asset(em)

    def check_new_submit_new_asset_time(self):
        st = datetime.datetime.strptime(str(datetime.datetime.now().date()) + self.gconf['period']['new_asset']['start'], '%Y-%m-%d%H:%M')
        et = datetime.datetime.strptime(str(datetime.datetime.now().date()) + self.gconf['period']['new_asset']['end'], '%Y-%m-%d%H:%M')
        now_time = datetime.datetime.now()

        return now_time > st and now_time < et
        #return True

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
                for p in self.policy:
                    p.execute(fund['code'], ret['GZ'], float(ret['GSZZL']), today)
        
        stocks = self.em_sq.get_stock_self_selection()
        for stock in stocks:
            ret = self.em[0].get_stock_real_charge(stock['code'], stock['market'])
            if ret is not None:
                for p in self.policy:
                    p.execute(stock['code'], float(ret['currentPrice']), float(ret['zdf']), self.today)
        
        print(".", end="")
        sys.stdout.flush()

    def buy_fund(self, em, code, vol):
        em.check_sdx(code)
        em.check_status(code, None)
        em.sign_contract(code)
        return True, em.fund_submit_trade(code, vol, "buy")
    
    def sale_fund(self, em, code, vol, company):
        em.check_status(code, company)
        return em.fund_submit_trade(code, vol, "sale")

    def check_stock_time(self):
        st1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + self.gconf['period']['trading_stock']['start1'], '%Y-%m-%d%H:%M')
        et1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + self.gconf['period']['trading_stock']['end1'], '%Y-%m-%d%H:%M')
        st2 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + self.gconf['period']['trading_stock']['start2'], '%Y-%m-%d%H:%M')
        et2 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + self.gconf['period']['trading_stock']['end2'], '%Y-%m-%d%H:%M')
        now_time = datetime.datetime.now()

        return (now_time > st1 and now_time < et1) or (now_time > st2 and now_time < et2)

    def check_fund_time(self):
        st = datetime.datetime.strptime(str(datetime.datetime.now().date()) + self.gconf['period']['trading_fund']['start'], '%Y-%m-%d%H:%M')
        et = datetime.datetime.strptime(str(datetime.datetime.now().date()) + self.gconf['period']['trading_fund']['end'], '%Y-%m-%d%H:%M')
        now_time = datetime.datetime.now()

        return now_time > st and now_time < et

    def check_order_success(em, order):
        flags = True
        ret = True
        for times in range(1,3):
            contracts = em.stock_get_revokes()
            if order not in contracts:
                flags = False
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
                vol = 0
                cash = para['vol'] * para['price']
                contract = self.sale_fund(em, para['code'], para['vol'], asset['market'])
            elif asset['type'] == "s" and self.check_stock_time():
                cash,vol = self.calc_asset(para['vol'], para['price'])
                contract = self.sale_stock(em, para['code'], vol, asset['market'])

            if contract is None:
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
        cash = sell_num * price

        return cash, sell_num
    
    def calc_price(self, buy_count, price):
        vol = (buy_count/price/100)*100
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
                ret, contract = self.buy_stock(em, para['code'], vol, para['price'])

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