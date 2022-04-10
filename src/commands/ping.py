import discord

from .abc import BaseCommand


class Ping(BaseCommand):
    abstract = False

    async def process(self, message: discord.Message):
        await message.reply("Pong!")
