import os
import random

import discord

from commands import BaseCommand

token = os.getenv("TOKEN")


client = discord.Client()


def get_arts() -> list[str]:
    arts_directory = os.path.join(os.getcwd() + "arts")
    arts = []

    for file_name in os.listdir(arts_directory):
        with open(os.path.join(arts_directory, file_name)) as file:
            arts.append(file.read())


@client.event
async def on_ready():
    print(client.user.name)


class MessageHandlers:
    @staticmethod
    async def soyjack_reply(message):
        if random.randint(0, 10) == 1:
            await message.channel.send(f">{message.content} {random.choice(get_arts())}")


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    await MessageHandlers.soyjack_reply(message)

    commands = BaseCommand.__subclasses__()

    command_map = {}
    for command in commands:
        command_map[command.command] = command

    print(command_map)

    cmd_prefix = "!"
    cmd = message.content.split(" ")[0]
    if cmd.startswith(cmd_prefix):
        cmd = cmd.replace(cmd_prefix, "")
        print(cmd)
        cmd_cls = command_map.get(cmd)
        if cmd_cls:
            await cmd_cls().run(message)


client.run(token)
