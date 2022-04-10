import os
import random

import discord
from loguru import logger

from router import Router
from utils import get_arts

token = os.getenv("TOKEN")


client = discord.Client()
router = Router("!")


@client.event
async def on_ready():
    logger.info(f"INITIALIZED BOT {client.user.name}")


class MessageHandlers:
    @staticmethod
    async def soyjack_reply(message):
        if random.randint(0, 20) == 1:
            logger.info(f"{message.author.name} ROLLED SOYJACK!")
            await message.channel.send(f">{message.content}\n{random.choice(get_arts())}")


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    await MessageHandlers.soyjack_reply(message)
    await router.dispatch(message)


client.run(token)
