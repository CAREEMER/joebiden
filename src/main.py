import os
import random
import datetime

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


garv_timeout_c: datetime.datetime = None
art_timeoit_c: datetime.datetime = None
bear_timeout_c: datetime.datetime = None


def update_timeout(is_garv: bool = True, is_bear: bool = False):
    global garv_timeout_c, art_timeoit_c, bear_timeout_c

    if is_garv:
        garv_timeout_c = datetime.datetime.now()

    if is_bear:
        bear_timeout_c = datetime.datetime.now()

    else:
        art_timeoit_c = datetime.datetime.now()


def can_art(is_garv: bool = True, is_bear: bool = False):
    if is_garv:
        if not garv_timeout_c:
            return True
        return ((datetime.datetime.now() - datetime.timedelta(minutes=1)) > garv_timeout_c) and random.randint(0, 3) == 1

    if is_bear:
        if not bear_timeout_c:
            return True

        return ((datetime.datetime.now() - datetime.timedelta(minutes=1)) > bear_timeout_c) and random.randint(0, 2) == 1

    if not art_timeoit_c:
        return True
    return ((datetime.datetime.now() - datetime.timedelta(minutes=2)) > art_timeoit_c) and random.randint(0, 10) == 1


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
        if not message.content:
            return

        # if garv
        if message.author.id == 949379472912707639:
            lucky = can_art(is_garv=True)
            if lucky:
                update_timeout(is_garv=True)
        elif message.author.id == 301676192900317184:
            if can_art(is_garv=False, is_bear=True):
                update_timeout(is_garv=False, is_bear=True)
                await message.reply("https://media.discordapp.net/attachments/679961199059927051/1022429235190698034/bruh.jpg")
                return True

            lucky = False
        else:
            lucky = can_art(is_garv=False)
            if lucky:
                update_timeout(is_garv=False)

        # if message.author.id in (301676192900317184, 315029938950635520):
        #     if 5 < lucky_number < 20:
        #         logger.info(f"{message.author.name} ROLLED PIC!")
        #         await message.channel.send("https://media.discordapp.net/attachments/913204760650334259/928569786156335124/crazy_cat_bubble.gif")
        #         return True

        if lucky:
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


if __name__ == "__main__":
    client.run(token)
