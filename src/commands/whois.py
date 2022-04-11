import random

import discord

from .abc import BaseCommand


class Whois(BaseCommand):
    rights = "any"
    abstract = False

    async def process(self, message: discord.Message):
        prop = " ".join(self.get_args(message))

        # random_user = random.choice(await self.redis.get_cached_users(message.guild.id))
        guild_members = []
        async for member in message.guild.fetch_members():
            guild_members.append(member)

        random_user = random.choice(guild_members)

        if random_user:
            await message.reply(f"{random_user.mention} - {prop}")
        else:
            await message.reply("Can't find any...")
