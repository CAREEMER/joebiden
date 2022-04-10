import discord
import random
from loguru import logger

from .abc import BaseCommand


class Whois(BaseCommand):
    command = "whois"
    rights = "any"

    async def process(self, message: discord.Message):
        prop = " ".join(self.get_args(message))

        prop_user: discord.Member = random.choice(message.guild.members)
        logger.info(message.guild.members)

        if prop_user:
            await message.reply(prop_user.mention + " - " + prop)
        else:
            await message.reply("Can't find any...")
