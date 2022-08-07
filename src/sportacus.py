# -*- coding: utf-8 -*-
import random
from typing import List
import lightbulb
import hikari
import asyncio
import logging
from python_redis_lib.redis import RedisClient
from python_redis_lib.settings import Reader, RedisSettings
from .motivation import motivation as huiynya

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
        # motivation_reader = Reader(file="motivation.toml", dir="conf")
        # try:
        #     self.motivation:List[str] = motivation_reader.config_dict["motivation"]["phrases"]
        # except KeyError:
        #     log.error(f"Motivation not configured correctly")

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

        @self.bot.command
        @lightbulb.command("help", "List commands and their descriptions")
        @lightbulb.implements(lightbulb.SlashCommand)
        async def help(ctx:lightbulb.Context):
            await ctx.respond("Your mother doesnt love you!")

        @self.bot.listen(hikari.StartedEvent)
        async def _hello(event:hikari.StartedEvent):
            log.info(f"Ready for some sport??")

        @self.bot.listen(hikari.MessageCreateEvent)
        async def _reply(event:hikari.MessageCreateEvent):
            try:
                await event.message.add_reaction("👌")
            except lightbulb.errors.BadRequestError as e:
                log.error(f"Error replying with emoji:\n{e}")
        @self.bot.listen(hikari.GuildMessageCreateEvent)
        async def motivation_handle(event):
            await huiynya(event)


    def run(self):
        self.bot.run()

