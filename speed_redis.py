import redis
import json
from redis.commands.json.path import Path

class SpeedRedis:
    def __init__(self) -> None:
        with open("config.json") as f:
            config = json.load(f)
            self.client = redis.Redis(
                            host=config["REDIS_HOST"], 
                            port=config["REDIS_PORT"]
                        )

    def get_message(self, key, is_json = True):
       if not is_json:
           return self.client.get(key)
       
       value = self.client.get(key)
       return json.loads(value) if value else None
    
    def set_message(self, key, value, expired=2):
        self.client.set(key, value, ex=expired)

    def hset(self, hash_key, obj, expired=2):
       self.client.hset(hash_key, mapping=obj)
       self.client.expire(hash_key, expired)

    def hmget(self, hash_key, keys):
        value = self.client.hmget(hash_key, keys)
        return value
    
    def set_json(self, key, object, expired=2):
        resp = self.client.json().set(key, Path.root_path(), object)
        self.client.expire(key, expired)
        return resp

    def get_json(self, key):
        return self.client.json().get(key)
    