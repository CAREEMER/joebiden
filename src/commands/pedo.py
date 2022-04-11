import random
from datetime import date

import discord

from .abc import BaseCommand


class Pedo(BaseCommand):
    timeout = 60

    async def get_redis_date(self) -> bytes:
        today = str(date.today())
        return await self.redis.get(today) or bytes()

    async def set_redis_date(self, member_id):
        today = str(date.today())
        await self.redis.set(today, str(member_id))

    async def process(self, message: discord.Message):
        today_pedo = (await self.get_redis_date()).decode("UTF-8")
        if not today_pedo:
            today_pedo = random.choice(await message.guild.fetch_members()).id
            await self.set_redis_date(today_pedo)

        await message.reply(f"Педофил дня - <@{today_pedo}>")
