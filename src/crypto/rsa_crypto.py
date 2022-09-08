import base64
import rsa
#from Crypto.PublicKey import RSA
#from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5

class JSEncrypt:
    def __init__(self, key_path) -> None:
        self.key = ""
        with open(key_path, "r") as f:
            key = f.read()
        self.key = base64.b64decode(key)

    def rsa_long_encrypt(self, msg, length=100):
        """
        单次加密串的长度最大为 (key_size/8)-11
        1024bit的证书用100, 2048bit的证书用 200
        """
        pubkey = rsa.PublicKey.load_pkcs1_openssl_der(self.key)
        #pubobj = RSA.importKey(self.key)
        #pubobj = Cipher_pkcs1_v1_5.new(pubobj)
        res = []
        for i in range(0, len(msg), length):
            #byt = pubobj.encrypt(msg[i:i+length].encode("utf-8")) 
            byt = rsa.encrypt(msg[i:i+length].encode("utf-8"),pubkey) 
            res.append(byt)
        cipher_text = b''.join(res)
        result = base64.b64encode(cipher_text)
        return result.decode()


def rsa_long_decrypt(priv_key_str, msg, length=128):
    """
    1024bit的证书用128,2048bit证书用256位
    """
    privobj = RSA.importKey(priv_key_str)
    privobj = Cipher_pkcs1_v1_5.new(privobj)
    res = []
    for i in range(0, len(msg), length):
        res.append(privobj.decrypt(msg[i:i+length], 'xyz'))
    return "".join(res)
