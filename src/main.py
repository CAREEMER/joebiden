import os
import random

import discord
from loguru import logger

from router import Router
from utils import get_arts, get_pics

token = os.getenv("TOKEN")
prefix = os.getenv("PREFIX")


client = discord.Client()
router = Router(prefix)


@client.event
async def on_ready():
    logger.info(f"INITIALIZED BOT {client.user.name}")


class MessageHandlers:
    @staticmethod
    async def soyjack_reply(message):
        lucky_number = random.randint(0, 3)
        if lucky_number == 1:
            logger.info(f"{message.author.name} ROLLED SOYJACK!")
            await message.channel.send(f">{message.content}\n{random.choice(get_arts())}")
        if lucky_number == 2:
            logger.info(f"{message.author.name} ROLLED PIC!")
            await message.channel.send(f">{message.content}", file=discord.File(random.choice(get_pics())))


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    await MessageHandlers.soyjack_reply(message)
    await router.dispatch(message)


client.run(token)
