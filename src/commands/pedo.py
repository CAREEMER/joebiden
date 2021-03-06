import random

import discord

from .abc import BaseCommand


class Pedo(BaseCommand):
    timeout = 60
    abstract = False

    async def process(self, message: discord.Message):
        today_pedo = await self.redis.get_pedo_of_the_day(message.guild.id)
        if not today_pedo:
            guild_members = []
            async for member in message.guild.fetch_members():
                guild_members.append(member)

            today_pedo = random.choice(guild_members).id
            await self.redis.set_pedo_of_the_day(message.guild.id, today_pedo)

        await message.reply(f"Педофил дня - <@{today_pedo}>")
