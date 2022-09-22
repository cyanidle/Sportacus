# -*- coding: utf-8 -*-
import lightbulb
import hikari
import logging
from python_redis_lib.redis import RedisClient
from python_redis_lib.settings import get_env_value
from python_redis_lib.supervisor import WorkerBase
from .motivation import Motivation
log = logging.getLogger("sportacus")

class Sportacus(WorkerBase):
    
    Instance = None

    def __init__(self) -> None:
        if not self.Instance is None:
            log.error(f"Only one Sportacus should be created at the same time!")
            raise RuntimeError("Only one Sportacus should be created at the same time!")
        self.Instance = self
        self.bot:lightbulb.BotApp = None
        self._redis:RedisClient = None
        self.motivation = Motivation()
        self._is_in_settings_mode = False

    def registerRedis(self,redis):
        self._redis = redis

    @property
    def redis(self) -> RedisClient:
        if self._redis is None:
            log.error(f"Attempt to use uninitialised Redis client!")
            return self._redis
        else:
            return self._redis

    async def _author_is_admin(self, ctx:lightbulb.Context):
        roles = await ctx.member.fetch_roles()
        permissions = [hikari.Permissions.NONE]
        for role in roles:
            permissions.append(role.permissions)
        if hikari.Permissions.ADMINISTRATOR in permissions:
            return True
        else:
            await ctx.respond("You must be an administrator to do that!")

    def init(self):
        self.bot = lightbulb.BotApp(token=get_env_value("BOT_TOKEN"), prefix="!")

        @self.bot.command
        @lightbulb.command("help", "List commands and their descriptions")
        @lightbulb.implements(lightbulb.SlashCommand)
        async def help(ctx:lightbulb.Context):
            await ctx.respond("Your mother doesnt love you!")

        

        @self.bot.command
        @lightbulb.command("set_channel", "Choose channel to set for sport challenges!")
        @lightbulb.implements(lightbulb.SlashCommand)
        async def create_task(ctx:lightbulb.Context): 
            if not await self._author_is_admin(ctx):
                return    
            
            await ctx.respond("Your mother doesnt love you!")

        @self.bot.command
        @lightbulb.command("settings", "Choose channel to set for sport challenges!")
        @lightbulb.implements(lightbulb.SlashCommand)
        async def settings(ctx:lightbulb.Context): 
            if not await self._author_is_admin(ctx):
                return
            self._is_in_settings_mode = True
            await ctx.respond("Choose channel for challenges")


        @self.bot.listen(hikari.StartedEvent)
        async def _hello(event:hikari.StartedEvent):
            log.info(f"Ready for some sport??")

        @self.bot.listen(hikari.MessageCreateEvent)
        async def _reply(event:hikari.MessageCreateEvent):
            if event.author.is_bot:
                return
            try:
                await event.message.add_reaction("👌")
            except lightbulb.errors.BadRequestError as e:
                log.error(f"Error replying with emoji:\n{e}")
            await self.motivation.reply(event)

        @self.bot.listen(hikari.ReactionAddEvent)
        async def _reply(event:hikari.ReactionAddEvent):
            event.channel_id

    def run(self):
        self.bot.run()

    def handleTerm(self) -> None:
        pass