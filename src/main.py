import os
import random

import discord
from loguru import logger

from router import Router
from services.redis import RedisClient
from utils import get_arts, get_pics

token = os.getenv("TOKEN")
prefix = os.getenv("PREFIX", "!")
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
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


def escape_content(content: str, author_mention: str) -> tuple[bool, str]:
    escaped = False
    reply = ""
    if not content.startswith(prefix):
        return escaped, reply

    blocked_tags = ["everyone", "here"]

    for tag in blocked_tags:
        mention_tag = f"@{tag}"
        if mention_tag in content:
            reply = content.replace(
                mention_tag, f"НЕ ИСПОЛЬЗУЙ {tag.upper()}, ПИДОР {author_mention}"
            )
            escaped = True

    return escaped, reply


@client.event
async def on_message(message: discord.Message):
    global redis

    if message.author.bot:
        return

    await redis.cache_member(message)

    escaped, warn = escape_content(message.content, message.author.mention)
    if escaped:
        await message.reply(warn)
        return

    await MessageHandlers.soyjack_reply(message)
    await router.dispatch(message)


client.run(token)
