# -*- coding: utf-8 -*-
import random
from typing import List
import lightbulb
import hikari
import asyncio
import logging
from python_redis_lib.redis import RedisClient
from python_redis_lib.settings import Reader, RedisSettings
from .motivation import Motivation
from .music import MusicPlayer

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
        self._music:MusicPlayer = None

    def registerRedis(self,redis):
        self._redis = redis

    @property
    def redis(self) -> RedisClient:
        if self._redis is None:
            log.error(f"Attempt to use uninitialised Redis client!")
            return self._redis
        else:
            return self._redis

    @property
    def music(self) -> MusicPlayer:
        if self._music is None:
            log.error(f"Attempt to use uninitialised Music client!")
            return self._music
        else:
            return self._music

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
            self._music = MusicPlayer()

        @self.bot.listen(hikari.MessageCreateEvent)
        async def _reply(event:hikari.MessageCreateEvent):
            if event.author.is_bot:
                return
            try:
                await event.message.add_reaction("👌")
            except lightbulb.errors.BadRequestError as e:
                log.error(f"Error replying with emoji:\n{e}")
            await self.motivation.reply(event)

        @self.bot.command
        @lightbulb.command("join", "Join voice chat the user is currently in!")
        @lightbulb.implements(lightbulb.SlashCommand)
        async def join_command(ctx:lightbulb.SlashContext):
            state = ctx.get_guild().get_voice_states().get(ctx.member.id)
            if state is None:
                await ctx.respond("You are not in voice chat!")
                return
            await self.bot.update_voice_state(ctx.guild_id, state.channel_id)
            await ctx.respond("08:08!")

        @self.bot.command
        @lightbulb.command("disconnect", "Leave voice chat")
        @lightbulb.implements(lightbulb.SlashCommand)
        async def disconnect_command(ctx:lightbulb.SlashContext):
            await self.bot.update_voice_state(ctx.guild_id, None)
            await ctx.respond("Disconnecting")

        @self.bot.command
        @lightbulb.command("play", "Queue video from youtube")
        @lightbulb.implements(lightbulb.SlashCommand)
        async def play_command(ctx:lightbulb.SlashContext):
            pass


    def run(self):
        self.bot.run()

