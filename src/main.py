import os.path
import sys

import aiohttp_jinja2
import jinja2
from aiohttp import web

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.routers import setup_routers
from src.core.database import init_db, close_db


async def init_app():
    app = web.Application()
    app['websockets'] = []
    setup_routers(app)

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./templates'))

    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)

    return app


if __name__ == '__main__':
    web.run_app(init_app())
