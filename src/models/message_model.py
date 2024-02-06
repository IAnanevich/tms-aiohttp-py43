from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from src.core.database import Base


class Message(Base):
    __tablename__ = 'messages'

    id = Column('id', Integer, primary_key=True)
    text = Column('text', String, nullable=False)
    created_at = Column('created_at', DateTime, default=datetime.now)
