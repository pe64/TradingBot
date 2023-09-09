from conf.yaml_conf import yaml_load
from cta.binance_cta import BinanceCta

if __name__ == "__main__":
    cf = yaml_load()
    em = BinanceCta(cf)
    