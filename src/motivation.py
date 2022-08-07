# -*- coding: utf-8 -*-
import logging
import random
import hikari
from typing import List

log = logging.getLogger("motivation")
class Motivation:
    def __init__(self) -> None:
        self.sources:List[str] = []
        with open("conf/motivation.txt", mode = "r", encoding="utf-8") as file:
            for line in file.readlines():
                self.sources.append(line)

    async def reply(self, event: hikari.GuildMessageCreateEvent):
        if event.content.__contains__("отивац"):
            await event.message.respond(random.choice(self.sources))