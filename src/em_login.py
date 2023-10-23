import time
from utils.yaml_conf import yaml_load
from cta.eastmoney_cta import EastMoneyCta
from http_opt.eastmoney import HttpEM
from utils.redis import Redis
from utils.time_format import TimeFormat

def login_and_update_cookies(htp, rds):
    htp.login_em_ver_code()
    ret = htp.login_em_platform()
    rds.UpdateEastMoneyCookies(htp.account_id)

    return ret == 0

if __name__ == "__main__":
    cf = yaml_load()
    em = EastMoneyCta(cf)
    rds = Redis(cf['redis']['url'], cf['redis']['port'])
    htps = []
    accounts = em.get_accounts()
    for account in accounts:
        htps.append(HttpEM(cf, account))
    
    while True:
        for htp in htps:
            try:
                if False == htp.get_validate_key():
                    htp.login_em_ver_code()
                    htp.login_em_platform()
                    rds.UpdateEastMoneyCookies(htp.account_id)


                status, data = htp.get_asset()
                if status == -2:
                    htp.login_em_ver_code()
                    htp.login_em_platform()
                    rds.UpdateEastMoneyCookies(htp.account_id)
                    status, data = htp.get_asset()
                
                status, fund = htp.get_fund_asset()
                if status != 0:
                    htp.login_em_ver_code()
                    htp.login_em_platform()
                    rds.UpdateEastMoneyCookies(htp.account_id)
                    status, fund = htp.get_fund_asset()

                print("\033[33m[%s]账户:%s 登陆成功\033[0m"%(TimeFormat.get_local_timstamp(),htp.get_user_id()),end="|")
                for node in data:
                    if node['Ljyk'] is None:
                        print("\033[33m总资产:%s元,可用金额:%s元,持仓盈亏:0元\033[0m"%(node['Zzc'],node['Kyzj']), end=',') 
                    elif float(node['Ljyk']) > 0:
                        print("\033[33m总资产:%s元,可用金额:%s元,持仓盈亏:\033[32m%s\033[33m元\033[0m"%(node['Zzc'],node['Kyzj'],node['Ljyk']), end=',') 
                    elif  float(node['Ljyk']) < 0:
                        print("\033[33m总资产:%s元,可用金额:%s元,持仓盈亏:\033[31m%s\033[33m元\033[0m"%(node['Zzc'],node['Kyzj'],node['Ljyk']), end=',') 

                for f in fund:
                    if f['Jjyk'] is None:
                        pass
                    elif float(f['Jjyk']) > 0:
                        print("\033[33m基金盈亏:\033[32m%s\033[33m元.\033[0m"%(f['Jjyk']))
                    elif float(f['Jjyk']) < 0:
                        print("\033[33m基金盈亏:\033[31m%s\033[33m元.\033[0m"%(f['Jjyk']))
                    pass

                if htp.new_stock_flag is False:
                    em.submit_new_asset(htp)

            except Exception as e:
                print("error:", e)
                continue
        
        time.sleep(60)     