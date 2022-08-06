# -*- coding: utf-8 -*-
import hikari
import asyncio
import logging

log = logging.getLogger("sportacus")

class Sportacus:

    Instance = None

    def __init__(self) -> None:
        if not self.Instance is None:
            log.error(f"Only one Sportacus should be created at the same time!")
            raise RuntimeError("Only one Sportacus should be created at the same time!")
        self.Instance = self
        self.bot = None

    def init(self):
        with open("TOKEN", "r") as file:
            token = file.readline()
            self.bot = hikari.GatewayBot(token=token)

        @self.bot.listen(hikari.StartedEvent)
        async def Hello(event):
            log.info(f"Ready for some sport??")


    def run(self):
        self.bot.run()




