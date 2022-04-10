from .abc import BaseCommand, soyjacks


class SoyjackList(BaseCommand):
    command = "ls"
    rights = "admin"

    async def process(self, message):
        await message.reply("List of soyjacks: " + ", ".join([str(s) for s in soyjacks]))
