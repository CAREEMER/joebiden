import re

import discord
from loguru import logger


class BaseCommand:
    command = ""
    mention_regex = re.compile(r"\<\@([0-9]+)\>")
    rights = "any"

    def can_perform(self, author_id):
        if self.rights == "admin":
            return author_id == 349568149055602689
        return True

    async def run(self, message: discord.Message):
        if not self.can_perform(message.author.id):
            await message.reply("You do not have sufficient rights.")
            return

        logger.info(f"{message.author.display_name} USES COMMAND {self.command}")
        await self.process(message)

    def get_args(self, message: discord.Message) -> list[str]:
        """
        Retrieves args from the message:
        "!ping arg1 arg2 arg3" -> ["arg1", "arg2", "arg3"]
        """
        return message.content.split(" ")[1:]

    def get_id_from_mention(self, arg: str) -> list[str]:
        return self.mention_regex.findall(arg)

    async def process(self, message: discord.Message):
        pass
