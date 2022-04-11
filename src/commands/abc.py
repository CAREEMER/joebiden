import re
import time
from typing import List

import discord
from loguru import logger

from services.redis import RedisClient


class BaseCommand:
    timeout = 10
    abstract = True
    mention_regex = re.compile(r"\<\@([0-9]+)\>")
    rights = "any"
    admin_id = 349568149055602689

    def __init__(self, redis: RedisClient):
        self.redis = redis
        self.command = self.__class__.__name__.lower()
        self.last_calls = {}

    def can_perform(self, author_id):
        if self.rights == "admin":
            return author_id == self.admin_id
        return True

    async def run(self, message: discord.Message):
        if not self.is_available(message.guild.id) or message.author.id == self.admin_id:
            logger.info(f"{message.author.name} TIMED OUT AT {self.command} COMMAND")
            return

        if not self.can_perform(message.author.id):
            await message.reply("You do not have sufficient rights.")
            return

        logger.info(f"{message.author.display_name} USES COMMAND {self.command}")
        await self.process(message)

        self.last_calls[message.guild.id] = time.time()

    def get_args(self, message: discord.Message) -> List[str]:
        """
        Retrieves args from the message:
        "!ping arg1 arg2 arg3" -> ["arg1", "arg2", "arg3"]
        """
        return message.content.split(" ")[1:]

    def get_id_from_mention(self, arg: str) -> List[str]:
        return self.mention_regex.findall(arg)

    async def process(self, message: discord.Message):
        pass

    def is_available(self, guild_id: int):
        last_call = self.last_calls.get(guild_id)
        return not last_call or time.time() - last_call >= self.timeout
