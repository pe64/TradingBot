from utils.yaml_conf import yaml_load
from policy.policy import Policy
if __name__ == "__main__":
    cf = yaml_load()
    po = Policy(cf['sqlite_path'],cf['redis'])
    po.run_policies_in_thread()
    po.monit_database()