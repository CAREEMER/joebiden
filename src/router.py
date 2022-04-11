import discord
from loguru import logger

from commands import BaseCommand
from services.redis import RedisClient


class Router:
    def __init__(self, prefix: str, redis: RedisClient):
        self.prefix = prefix
        self.redis = redis

        commands = BaseCommand.__subclasses__()

        self.command_map = {}
        for command in commands:
            if not getattr(command, "abstract", False):
                self.command_map[command.__name__.lower()] = command(self.redis)

        logger.info(f"INITIALIZED ROUTER. COMMANDS: {', '.join(list(self.command_map.keys()))}")

    async def dispatch(self, message: discord.Message):
        cmd = message.content.split(" ")[0]

        if cmd.startswith(self.prefix):
            cmd = cmd.replace(self.prefix, "")
            cmd_obj = self.command_map.get(cmd)
            if cmd_obj:
                await cmd_obj.run(message)
