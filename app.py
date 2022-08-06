# -*- coding: utf-8 -*-
import hikari

token = ""
with open("TOKEN", "r") as file:
    token = file.readline()

bot = hikari.GatewayBot(token=token)