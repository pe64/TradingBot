import time
from utils.yaml_conf import yaml_load
from cta.eastmoney_cta import EastMoneyCta
from http_opt.eastmoney import HttpEM
from utils.redis import Redis

if __name__ == "__main__":
    cf = yaml_load()
    em = EastMoneyCta(cf)
    rds = Redis(cf)
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
            except Exception as e:
                print("error:", e)
                continue
        time.sleep(60)     