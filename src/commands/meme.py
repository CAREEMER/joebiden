import random

import discord

from .abc import BaseCommand


class Meme(BaseCommand):
    abstract = False
    rights = "any"

    async def process(self, message: discord.Message):
        guild_memes_map = {
            656073003234492416: [
                "https://media.discordapp.net/attachments/679961199059927051/910162647289307167/1.png",
                "https://cdn.discordapp.com/attachments/679961199059927051/924425250849050704/DSC_0267.jpg",
                "https://cdn.discordapp.com/attachments/679961199059927051/937026998545571870/92EA24A2-F5E2-43ED-8EE0-7E9F2E345BFC.jpg",
                "https://cdn.discordapp.com/attachments/679961199059927051/947947316139147334/unknown.png",
            ],
        }

        memes = guild_memes_map.get(message.guild.id)

        if memes:
            await message.reply(random.choice(memes))
        else:
            await message.reply("Don't have any...")
