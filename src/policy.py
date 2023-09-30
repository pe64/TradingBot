from utils.yaml_conf import yaml_load
from policy.policy import Policy
if __name__ == "__main__":
    cf = yaml_load()
    if cf['virtual']['enabled']:
        po = Policy(cf['virtual']['sqlite_path'],cf['redis'])
    else:
        po = Policy(cf['sqlite_path'],cf['redis'])
    po.run_policies_in_thread()
    po.monit_database()