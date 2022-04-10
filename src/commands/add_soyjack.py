import discord

from .abc import BaseCommand


class AddSoyjack(BaseCommand):
    command = "as"
    rights = "admin"

    async def process(self, message: discord.Message):
        args = self.get_args(message)
        for arg in args:
            mention = self.get_mention(arg)
            if mention:
                mention = int(mention[0])
                await message.reply(f"Added <@{mention}> to the list of soyjacks!")
