import random

import discord
from loguru import logger

from .abc import BaseCommand


class Whois(BaseCommand):
    rights = "any"
    abstract = False

    async def process(self, message: discord.Message):
        prop = " ".join(self.get_args(message))

        random_user = random.choice(await self.redis.get_cached_users(message.guild.id))

        if random_user:
            await message.reply(f"<@{random_user}> - {prop}")
        else:
            await message.reply("Can't find any...")
