import asyncio
from lavaplayer import Lavalink
import lightbulb


class MusicPlayer:
    def __init__(self) -> None:
        ioloop = asyncio.get_running_loop()
        self.lavalink = Lavalink(loop=ioloop)

    def play(self, ctx:lightbulb.SlashContext):
        self.lavalink