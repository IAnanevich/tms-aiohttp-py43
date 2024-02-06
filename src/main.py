import os.path
import sys

from aiohttp import web

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.routers import setup_routers
from src.core.database import Base, engine

app = web.Application()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    setup_routers(app)
    web.run_app(app)
