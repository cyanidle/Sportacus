# -*- coding: utf-8 -*-
from python_redis_lib.redis import RedisClient
from src.sportacus import Sportacus
from python_redis_lib.settings import LoggingSettings, Reader, RedisSettings
from python_redis_lib.initlogging import initLogging
from python_redis_lib.supervisor import get_loop
import threading



def main():
    logging_conf_reader = Reader(file="logging.toml")
    initLogging(__file__, settings=logging_conf_reader.parse(LoggingSettings, key="logging"))
    sportacus = Sportacus()
    sportacus.init()
    redis_thr = threading.Thread(target=main_redis, args=[sportacus])
    redis_thr.daemon = True
    redis_thr.start()
    sportacus.run()
    

def main_redis(sportacus: Sportacus):
    config_reader = Reader(file="config.toml")
    ioloop = get_loop()
    redis = RedisClient(config_reader.parse(RedisSettings, key="redis"), ioloop=ioloop)
    sportacus.registerRedis(redis)
    redis.run()

if __name__ == "__main__":
    main()
