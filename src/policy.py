from conf.yaml_conf import yaml_load
from policy.policy import Policy
if __name__ == "__main__":
    cf = yaml_load()
    po = Policy()