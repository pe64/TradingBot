from conf.yaml_conf import yaml_load
from asset_charge.asset_charge import AssetCharge

if __name__ == "__main__":
    cf = yaml_load()
    ac = AssetCharge(cf)
    ac.run()