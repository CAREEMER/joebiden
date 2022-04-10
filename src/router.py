import discord

from commands import BaseCommand
from loguru import logger


class Router:
    def __init__(self, prefix: str):
        self.prefix = prefix

        commands = BaseCommand.__subclasses__()

        self.command_map = {}
        for command in commands:
            if not getattr(command, "abstract", False):
                self.command_map[command.__name__.lower()] = command

        logger.info(f"INITIALIZED ROUTER. COMMANDS: {[command for command in self.command_map]}")

    async def dispatch(self, message: discord.Message):
        cmd = message.content.split(" ")[0]

        if cmd.startswith(self.prefix):
            cmd = cmd.replace(self.prefix, "")
            cmd_cls = self.command_map.get(cmd)
            if cmd_cls:
                await cmd_cls().run(message)
