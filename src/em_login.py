import time
from utils.yaml_conf import yaml_load
from cta.eastmoney_cta import EastMoneyCta
from http_opt.eastmoney import HttpEM
from utils.redis import Redis

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

                print("\033[33m账户:%s 登陆成功\033[0m"%(htp.get_user_id()),end="|")
                for node in data:
                    if node['Ljyk'] is None:
                        print("\033[33m总资产:%s元,可用金额:%s元,持仓盈亏:0元.\033[0m"%(node['Zzc'],node['Kyzj'])) 
                    elif float(node['Ljyk']) > 0:
                        print("\033[33m总资产:%s元,可用金额:%s元,持仓盈亏:\033[32m%s\033[33m元.\033[0m"%(node['Zzc'],node['Kyzj'],node['Ljyk'])) 
                    elif  float(node['Ljyk']) < 0:
                        print("\033[33m总资产:%s元,可用金额:%s元,持仓盈亏:\033[31m%s\033[33m元.\033[0m"%(node['Zzc'],node['Kyzj'],node['Ljyk'])) 

            except Exception as e:
                print("error:", e)
                continue
        
        time.sleep(60)     