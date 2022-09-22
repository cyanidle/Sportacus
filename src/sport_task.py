from dataclasses import dataclass
from python_redis_lib.redis import RedisClient, RedisSerialisable

@dataclass(kw_only=True, slots=True)
class SportTask(RedisSerialisable):
    pass