from pydantic import BaseModel


class MessageCreateScheme(BaseModel):
    text: str


class MessageUpdateScheme(BaseModel):
    text: str


class MessageResponseScheme(BaseModel):
    id: int
    text: str
