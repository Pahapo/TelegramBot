import os

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, Identity, Integer, Text, VARCHAR
from .base import BaseModel

metadata = MetaData()


class invite_message_class(BaseModel):
    __tablename__ = 'invite_message'
    id = Column(Integer, Identity(), primary_key=True)
    invite_message = Column(Text, nullable=True)
    invite_picture = Column(String(200), nullable=True)


class SendMessage(BaseModel):
    __tablename__ = 'send_message'
    id = Column(Integer, Identity(), primary_key=True)
    message = Column(Text, nullable=True)
    picture = Column(String(200), nullable=True)

    def __str__(self) -> str:
        return f'<MessageId:{self.id}>'


class User(BaseModel):
    __tablename__ = 'users'
    id = Column(Integer, Identity(), primary_key=True)
    user_id = Column(VARCHAR(200), unique=True, nullable=False)
    bot_token = Column(VARCHAR(200), nullable=False, default=os.getenv('token'))

    def __str__(self) -> str:
        return f'<User:{self.user_id}>'


class Statistics(BaseModel):
    __tablename__ = 'statistics'
    id = Column(Integer, Identity(), primary_key=True)
    blocked = Column(Integer, nullable=True)
    available = Column(Integer, nullable=True)
