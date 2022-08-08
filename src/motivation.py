# -*- coding: utf-8 -*-
import logging
import random
import re
import hikari
import asyncio
from typing import List

log = logging.getLogger("motivation")

class Motivation:
    def __init__(self) -> None:
        self.sources:List[str] = []
        with open("conf/motivation.txt", mode = "r", encoding="utf-8") as file:
            self.sources = file.read().split("\n")
        self.matcher = re.compile("[\s({]м+отивац[а-я]{2,3}[\s.?!:)}]")

    async def reply(self, event: hikari.GuildMessageCreateEvent):
        raw = f" {event.content.lower()} "
        if self.matcher.match(raw):
            await event.message.respond(random.choice(self.sources))
        
