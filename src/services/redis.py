import aioredis
from loguru import logger
import discord


class KeySchema:
    def __init__(self, global_prefix):
        self.global_prefix = global_prefix

    def cached_users(self, guild_id: int):
        return f"{self.global_prefix}:CACHED_USERS:{guild_id}"


class RedisClient:
    def __init__(self, bot_name: str):
        self.redis_url = "redis://0.0.0.0:6379"
        self.key_schema = KeySchema(bot_name)
        self.redis_conn = aioredis.from_url(self.redis_url)

    async def ping_redis(self):
        await self.redis_conn.set("PING", "PONG")
        data = await self.redis_conn.get("PING")

        if data.decode("UTF-8") == "PONG":
            logger.info("INITIALIZED REDIS CLIENT ON HOST %s" % self.redis_url)
        else:
            raise Exception("Can't connect to redis using url %s" % self.redis_url)

        await self.redis_conn.delete("PING")

    async def cache_member(self, message: discord.Message):
        cached_members_key = self.key_schema.cached_users(message.guild.id)
        delimeter = "**"

        data = await self.redis_conn.get(cached_members_key)

        if data:
            cache = data.decode("UTF-8").split(delimeter)
        else:
            cache = []

        if not str(message.author.id) in cache:
            cache.append(str(message.author.id))

        await self.redis_conn.set(cached_members_key, delimeter.join(cache))

    async def get_cached_users(self, guild_id: int) -> list[str]:
        cached_members_key = self.key_schema.cached_users(guild_id)
        delimeter = "**"

        data = await self.redis_conn.get(cached_members_key)
        if not data:
            return []

        return data.decode("UTF-8").split(delimeter)
