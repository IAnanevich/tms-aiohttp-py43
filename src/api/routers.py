from aiohttp import web

from src.api.message import create_message, get_messages, get_message, update_message, delete_message


def setup_routers(app: web.Application) -> None:
    app.router.add_route('GET', '/messages', get_messages)
    app.router.add_route('POST', '/messages', create_message)
    app.router.add_route('GET', '/messages/{id}', get_message)
    app.router.add_route('PUT', '/messages/{id}', update_message)
    app.router.add_route('DELETE', '/messages/{id}', delete_message)
