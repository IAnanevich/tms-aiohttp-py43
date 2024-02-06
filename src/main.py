import os.path
import sys

from aiohttp import web

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.routers import setup_routers
from src.core.database import init_db, close_db

app = web.Application()


if __name__ == '__main__':
    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)
    setup_routers(app)
    web.run_app(app)
