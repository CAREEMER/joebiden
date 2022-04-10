import discord

from commands import BaseCommand


class Router:
    def __init__(self, prefix: str):
        self.prefix = prefix

    async def dispatch(self, message: discord.Message):
        commands = BaseCommand.__subclasses__()

        command_map = {}
        for command in commands:
            command_map[command.command] = command

        cmd_prefix = self.prefix
        cmd = message.content.split(" ")[0]
        if cmd.startswith(cmd_prefix):
            cmd = cmd.replace(cmd_prefix, "")
            print(cmd)
            cmd_cls = command_map.get(cmd)
            if cmd_cls:
                await cmd_cls().run(message)
