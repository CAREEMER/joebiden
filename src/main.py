import os
import random

import discord
from loguru import logger

from router import Router
from utils import get_arts, get_pics
from services.redis import RedisClient

token = os.getenv("TOKEN")
prefix = os.getenv("PREFIX", "!")
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")


client = discord.Client()
router: Router = None

redis: RedisClient = None


@client.event
async def on_ready():
    global redis, router

    logger.info(f"INITIALIZED BOT {client.user.name}")

    redis = RedisClient(bot_name=client.user.name, url=redis_url)
    await redis.ping_redis()

    router = Router(prefix, redis)


class MessageHandlers:
    @staticmethod
    async def soyjack_reply(message):
        lucky_number = random.randint(0, 40)
        if lucky_number == 1:
            logger.info(f"{message.author.name} ROLLED SOYJACK!")
            await message.channel.send(f">{message.content}\n{random.choice(get_arts())}")
        if lucky_number == 2:
            logger.info(f"{message.author.name} ROLLED PIC!")
            await message.channel.send(f">{message.content}", file=discord.File(random.choice(get_pics())))


@client.event
async def on_message(message: discord.Message):
    global redis

    if message.author.bot:
        return

    await redis.cache_member(message)

    await MessageHandlers.soyjack_reply(message)
    await router.dispatch(message)


client.run(token)
