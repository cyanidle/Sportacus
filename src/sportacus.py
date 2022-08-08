# -*- coding: utf-8 -*-
import random
from typing import List
import lightbulb
import discord
import asyncio
import logging
from python_redis_lib.redis import RedisClient
from python_redis_lib.settings import Reader, RedisSettings
from .motivation import Motivation

log = logging.getLogger("sportacus")

class Sportacus:

    Instance = None

    def __init__(self) -> None:
        if not self.Instance is None:
            log.error(f"Only one Sportacus should be created at the same time!")
            raise RuntimeError("Only one Sportacus should be created at the same time!")
        self.Instance = self
        self.bot:lightbulb.BotApp = None
        self._redis:RedisClient = None
        self.motivation = Motivation()

    def registerRedis(self,redis):
        self._redis = redis

    @property
    def redis(self) -> RedisClient:
        if self._redis is None:
            log.error(f"Attempt to use uninitialised Redis client!")
            return self._redis
        else:
            return self._redis

    def init(self):
        with open("TOKEN", "r") as file:
            token = file.readline()
            self.bot = lightbulb.BotApp(token=token, prefix="!")

        
        


    def run(self):
        self.bot.run()

