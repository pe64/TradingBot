import threading

from utils.yaml_conf import yaml_load
from cta.binance_cta import BinanceCta
from cta.eastmoney_cta import EastMoneyCta

if __name__ == "__main__":
    cf = yaml_load()
    bn = BinanceCta(cf)
    em = EastMoneyCta(cf)
    account_bn = bn.get_accounts()
    account_em = em.get_accounts()
    threads = []

    def run_binance_account(account):
        bn.run(account)
    
    def run_eastmoney_account(account):
        em.run(account)
    
    for account in account_bn:
        thread = threading.Thread(target=run_binance_account, args=(account,))
        threads.append(thread)
    
    for account in account_em:
        thread = threading.Thread(target=run_eastmoney_account, args=(account,))
        threads.append(thread)

    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()