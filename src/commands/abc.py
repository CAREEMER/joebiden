import re

import discord


class BaseCommand:
    command = "help"
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

        await self.process(message)

    def get_args(self, message: discord.Message):
        return message.content.split(" ")[1:]

    def get_mention(self, arg: str):
        return self.mention_regex.findall(arg)

    async def process(self, message: discord.Message):
        pass
