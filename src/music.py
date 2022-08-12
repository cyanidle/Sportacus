import asyncio
from dataclasses import dataclass
import logging
from lavaplayer import Lavalink
import lightbulb
from hikari import Snowflake
from python_redis_lib.settings import Reader

log = logging.getLogger("music")
log.info("LOGGING USING NAME: 'music'")

@dataclass
class MusicPlayerSettings:
    lavalink_host: str
    lavalink_port: int
    lavalink_user_id: int
    @staticmethod
    def parse(*args, **kwargs):
        reader:Reader = kwargs["reader"]
        return MusicPlayerSettings(**(reader.config_dict.get("music")))

class MusicPlayer:
    def __init__(self) -> None:
        reader = Reader(file="music.toml")
        ioloop = asyncio.get_running_loop()
        settings = reader.parse(MusicPlayerSettings)
        self.lavalink = Lavalink(host = settings.lavalink_host, port = settings.lavalink_port,
                                 password="youshallnotpass", user_id=settings.lavalink_user_id, loop=ioloop)
        self.lavalink.connect()

    async def add_new_guild(self, guild_id: Snowflake):
        await self.lavalink.create_new_node(guild_id)
        await self.lavalink.wait_for_connection(guild_id)
        

    async def play(self, ctx:lightbulb.SlashContext):
        options = ctx.options
        await self.add_new_guild(ctx.guild_id)
        try:
            tracks = await self.lavalink.search_youtube("aboba")
        except Exception as e:
            log.exception(e)
        await self.lavalink.play(ctx.guild_id, track=tracks[0], start=True)
