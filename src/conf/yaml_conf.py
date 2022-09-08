import yaml
yaml_path = "conf/trading_bot.yaml"

def yaml_load() :
    content = ""
    with open(yaml_path,"r") as f:
        content = f.read()
        pass
    
    cf = yaml.load(content,  Loader=yaml.FullLoader)
    return cf 