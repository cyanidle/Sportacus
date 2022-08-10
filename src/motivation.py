# -*- coding: utf-8 -*-
import logging
import random
import re
import hikari
import asyncio
from typing import List

from python_redis_lib.settings import Reader

log = logging.getLogger("motivation")

class Motivation:
    def __init__(self) -> None:
        self.sources:List[str] = []
        motivation_reader = Reader(file="motivation.toml")
        self.sources = motivation_reader.config_dict.get("motivation").get("phrases")
        self.matcher = re.compile("[\s({]м+отивац[а-я]{2,3}[\s.?!:)}]")

    async def reply(self, event: hikari.GuildMessageCreateEvent):
        if isinstance(event.content, str):
            raw = f" {event.content.lower()} "
            if self.matcher.match(raw):
                await event.message.respond(random.choice(self.sources))
        
