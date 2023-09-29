import redis

class Redis:
    def __init__(self, cf):
        self.r = redis.StrictRedis(host=cf["redis"]["url"], port=cf['redis']['port'], db=0)
        self.pubsub = self.r.pubsub()

    def Subscribe(self, key, callback=None):
        self.pubsub.subscribe(key)
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                if callback:
                    callback(message['channel'], message['data'])
                else:
                    return message['channel'], message['data']

    def PSubscribe(self, pattern, policy, callback=None):
        self.pubsub.psubscribe(pattern)
        for message in self.pubsub.listen():
            if message['type'] == 'pmessage':
                if callback:
                    callback(message['channel'], message['data'], policy)
                else:
                    return message['channel'], message['data']
    
    def Publish(self, key, content):
        self.r.publish(key, content) 
    
    def LPush(self, key, content):
        self.r.lpush(key, content)
    
    def BRPop(self, key, timeout):
        result = self.r.brpop(key, timeout)
        if result:
            _, data = result
            return data
        return None
    
    def Set(self, key, value):
        self.r.set(key, value)

    def Get(self, key):
        return self.r.get(key)

    def GetAssetById(self, asset_id):
        asset_str = self.r.get("asset#" + str(asset_id))
        return asset_str
    
    def UpdateEastMoneyCookies(self, account_id):
        msg ='{"trade":"UPDATE"}'
        self.r.publish("left#trade#" + str(account_id),msg)