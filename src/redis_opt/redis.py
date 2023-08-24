import redis

class Redis:
    def __init__(self, cf):
        self.r = redis.StrictRedis(host=cf["redis"]["url"], port=cf['redis']['port'], db=0)
        self.timeout = cf['redis']['timeout']

    def Publish(self, key, content):
        self.r.publish(key, content) 
    
    def LPush(self, key, content):
        self.r.lpush(key, content)
    
    def BRPop(self, key):
        result = self.r.brpop(key, self.timeout)
        if result:
            _, data = result
            return data
        return None
    