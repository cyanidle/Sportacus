import asyncio
from dataclasses import dataclass
from lavaplayer import Lavalink
import lightbulb
from python_redis_lib.settings import Reader

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

    def play(self, ctx:lightbulb.SlashContext):
        pass