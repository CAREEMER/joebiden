from pydantic import BaseModel


class Member(BaseModel):
    id: int
    name: str
    mention: str
    guild_id: int
