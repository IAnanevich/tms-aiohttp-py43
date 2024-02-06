from typing import Type

from aiohttp import web

from src.core.database import session
from src.models.message_model import Message
from src.schemas.message_schema import MessageCreateScheme, MessageResponseScheme, MessageUpdateScheme


async def create_message(request: web.Request) -> web.Response:
    data: MessageCreateScheme = MessageCreateScheme.parse_obj(await request.json())

    session.add(Message(text=data.text))
    session.commit()

    return web.json_response({'message': 'Created successfully'})


async def get_messages(request: web.Request) -> web.Response:
    messages: list[Type[Message]] = session.query(Message).all()

    messages_text: list[dict] = [
        MessageResponseScheme(id=message.id, text=message.text).dict() for message in messages
    ]

    return web.json_response({'messages': messages_text})


async def get_message(request: web.Request) -> web.Response:
    message_id: int = int(request.match_info['id'])
    message: Type[Message] = session.get(Message, message_id)

    return web.json_response(MessageResponseScheme(id=message.id, text=message.text).dict())


async def update_message(request: web.Request) -> web.Response:
    message_id: int = int(request.match_info['id'])
    data: MessageUpdateScheme = MessageUpdateScheme.parse_obj(await request.json())
    message: Type[Message] = session.get(Message, message_id)
    message.text = data.text
    session.add(message)
    session.commit()

    return web.json_response({'status:': 'Message updated successfully'})


async def delete_message(request: web.Request) -> web.Response:
    message_id: int = int(request.match_info['id'])
    session.delete(session.get(Message, message_id))
    session.commit()

    return web.json_response({'status': 'Message deleted successfully'})