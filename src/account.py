import threading

from conf.yaml_conf import yaml_load
from cta.binance_cta import BinanceCta

if __name__ == "__main__":
    cf = yaml_load()
    bn = BinanceCta(cf)
    num = bn.get_binance_accounts_num()
    threads = []

    def run_binance_account(account_id):
        bn.binance_account_run(account_id)
    
    for _ in range(num):
        thread = threading.Thread(target=run_binance_account, args=(_,))
        threads.append(thread)

    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()