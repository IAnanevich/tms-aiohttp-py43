from typing import Type, Any

from aiohttp import web
from sqlalchemy import select, exc

from src.core.database import get_session
from src.models.message_model import Message
from src.schemas.message_schema import MessageCreateScheme, MessageResponseScheme, MessageUpdateScheme


async def create_message(request: web.Request) -> web.Response:
    try:
        data: MessageCreateScheme = MessageCreateScheme.parse_obj(await request.json())
    except ValueError as e:
        return web.json_response({'status:': e})

    async with get_session() as session:
        session.add(Message(text=data.text))
        await session.commit()

    return web.json_response({'message': 'Created successfully'})


async def get_messages(request: web.Request) -> web.Response:
    async with get_session() as session:
        messages: Any = await session.execute(select(Message))

    messages_text: list[dict] = [
        MessageResponseScheme(id=message.id, text=message.text).dict() for message in messages.scalars()
    ]

    return web.json_response({'messages': messages_text})


async def get_message(request: web.Request) -> web.Response:
    message_id: int = int(request.match_info['id'])
    async with get_session() as session:
        message: Type[Message] = await session.get(Message, message_id)

        if not message:
            return web.json_response({'status: ': f'Message with {message_id=} not found'}, status=404)

    return web.json_response(MessageResponseScheme(id=message.id, text=message.text).dict())


async def update_message(request: web.Request) -> web.Response:
    message_id: int = int(request.match_info['id'])

    try:
        data: MessageUpdateScheme = MessageUpdateScheme.parse_obj(await request.json())
    except ValueError as e:
        return web.json_response({'status:': e})

    async with get_session() as session:
        message: Type[Message] = await session.get(Message, message_id)

        if not message:
            return web.json_response({'status: ': f'Message with {message_id=} not found'}, status=404)

        message.text = data.text
        session.add(message)
        await session.commit()

    return web.json_response({'status:': 'Message updated successfully'})


async def delete_message(request: web.Request) -> web.Response:
    message_id: int = int(request.match_info['id'])

    async with get_session() as session:
        message = await session.get(Message, message_id)
        if not message:
            return web.json_response({'status: ': f'Message with {message_id=} not found'}, status=404)

        await session.delete(message)
        await session.commit()

    return web.json_response({'status': 'Message deleted successfully'})
