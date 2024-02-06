import json

from aiohttp import web
from aiohttp.web_ws import WebSocketResponse
from sqlalchemy import select

from src.core.database import get_session
from src.models.message_model import Message
from src.schemas.message_schema import MessageResponseScheme


async def get_messages_from_db():
    async with get_session() as session:
        messages = await session.execute(select(Message))
        return messages.scalars()


async def send_history(ws):
    messages = await get_messages_from_db()
    for message in messages:
        await ws.send_json(MessageResponseScheme(id=message.id, text=message.text).dict())


async def save_message_to_db(data):
    async with get_session() as session:
        message = Message(text=data['text'])
        session.add(message)
        await session.commit()
        return message


async def broadcast_message(request, message, exclude=None):
    exclude = exclude or []
    for client in request.app['websockets']:
        if client not in exclude:
            await client.send_json(message)


async def websocket_handler(request):
    ws = WebSocketResponse()
    await ws.prepare(request)

    await send_history(ws)

    try:
        request.app['websockets'].append(ws)

        async for message in ws:
            if message.type == web.WSMsgType.TEXT:

                data = json.loads(message.data)

                if 'type' in data and data['type'] == 'heartbeat':
                    continue

                message = await save_message_to_db(data)

                await broadcast_message(
                    request, MessageResponseScheme(id=message.id, text=message.text).dict(), exclude=[ws]
                )
    finally:
        request.app['websockets'].remove(ws)
        await ws.close()

    return ws
