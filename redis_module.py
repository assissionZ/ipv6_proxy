
import config

import os
import redis

from log import MyLogger


class RedisModule:
    def __init__(self, log_name):
        # log
        self.log = MyLogger()

        # redis
        self.r = None
        self.ex_time = 99999    # 过期时间 5秒

    def connect_redis(self):
        try:
            host = config.redis_config["host"]
            port = config.redis_config["port"]
            self.r = redis.Redis(host=host, port=port)
        except Exception as e:
            print(e)
            return None