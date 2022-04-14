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
        lucky_number = random.randint(0, 20)

        if message.author.id in (301676192900317184, 315029938950635520):
            if 5 < lucky_number < 20:
                logger.info(f"{message.author.name} ROLLED PIC!")
                await message.channel.send("https://media.discordapp.net/attachments/913204760650334259/928569786156335124/crazy_cat_bubble.gif")
                return True

        if lucky_number == 2:
            logger.info(f"{message.author.name} ROLLED PIC!")
            await message.channel.send(f">{message.content}", file=discord.File(random.choice(get_pics())))
            return True

        return False


def escape_content(content: str, author_mention: str) -> tuple[bool, str]:
    escaped = False
    reply = ""
    if not content.startswith(prefix):
        return escaped, reply

    blocked_tags = ["everyone", "here"]

    for tag in blocked_tags:
        mention_tag = f"@{tag}"
        if mention_tag in content:
            reply = f"НЕ ИСПОЛЬЗУЙ {tag.upper()}, ПИДОР {author_mention}"
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

    already_replied = await MessageHandlers.soyjack_reply(message)
    if not already_replied:
        await router.dispatch(message)


client.run(token)
