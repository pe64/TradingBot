import time
from utils.yaml_conf import yaml_load, api_yaml_load
from cta.eastmoney_cta import EastMoneyCta
from http_opt.eastmoney import HttpEM
from utils.redis import Redis
from utils.time_format import TimeFormat
from gpt.openrouter import OpenRouterService

def login_and_update_cookies(htp, rds):
    img = htp.login_em_ver_code()
    ver_code = gpt.ocr(img)
    print("ver code:" + ver_code)
    htp.login_em_platform(ver_code)
    rds.UpdateEastMoneyCookies(htp.account_id)

if __name__ == "__main__":
    cf = yaml_load()
    api_cf = api_yaml_load()
    em = EastMoneyCta(cf)
    rds = Redis(cf['redis']['url'], cf['redis']['port'])
    htps = []
    accounts = em.get_accounts()
    for account in accounts:
        htps.append(HttpEM(cf, account))
    
    gpt = OpenRouterService(cf['gpt'], api_cf)
    while True:
        for htp in htps:
            try:
                if False == htp.get_validate_key():
                    login_and_update_cookies(htp, rds)

                status, data = htp.get_asset()
                if status == -2:
                    login_and_update_cookies(htp, rds)
                    status, data = htp.get_asset()
                
                status, fund = htp.get_fund_asset()
                if status != 0:
                    login_and_update_cookies(htp, rds)
                    status, fund = htp.get_fund_asset()
                    continue
                
                ts = TimeFormat.get_local_timstamp()

                print("\033[33m[%s]账户:%s 登陆成功\033[0m"%(ts,htp.get_user_id()),end="|")
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

                if TimeFormat.is_time_between(ts, cf['period']['new_asset']['start'], 
                            cf['period']['new_asset']['end']) and TimeFormat.is_work_day(ts) is True:
                    em.submit_new_asset(htp)

            except Exception as e:
                print("error:", e)
                continue
        
        time.sleep(300)     