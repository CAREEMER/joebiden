import discord

from .abc import BaseCommand


class Ping(BaseCommand):
    command = "ping"

    async def process(self, message: discord.Message):
        await message.reply("Pong!")
