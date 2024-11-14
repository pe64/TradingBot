from web3 import Web3
import requests
from requests.adapters import HTTPAdapter
from eth_account import Account

# 配置代理
proxies = {
    'http': 'http://127.0.0.1:7890',  # 替换为你的代理地址
    'https': 'http://127.0.0.1:7890'  # 替换为你的代理地址
}

# 创建一个会话对象
session = requests.Session()
session.proxies = proxies
session.mount('http://', HTTPAdapter())
session.mount('https://', HTTPAdapter())

# 使用公共RPC地址，并设置代理
web3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/eth', session=session))

# 检查是否成功连接
if web3.is_connected():
    print("Successfully connected to Ethereum network")
else:
    print("Failed to connect to Ethereum network")

def private_key_to_address(private_key: str) -> str:
    """
    将以太坊私钥转换为地址
    """
    account = Account.from_key(private_key)
    return account.address

address = private_key_to_address("1")
print("address:" + address)