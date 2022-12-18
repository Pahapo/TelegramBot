import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InputFile
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from model import Base, metadata
import os

def create_async_engine(url : str) -> AsyncEngine:
    return _create_async_engine(url, echo=True)

async def proceed_schemas(engine: AsyncEngine, metadata) -> None:
    with engine.connect() as conn:
        conn.run_sync(metadata.create_all())

def get_session_maker(engine : AsyncEngine) -> sessionmaker:
    return sessionmaker(engine, class_=AsyncSession)


API = os.getenv('BOT_TOKEN')
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{API}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)
engine = create_async_engine("postgresql://ogqvnmdkjsxjus:a3bac4e2704930bfcc12377ffe53fee216c6c070f6b72fc7da9ad8a123fa532b@ec2-52-30-159-47.eu-west-1.compute.amazonaws.com:5432/daqu593lifqtvi")
session_maker = get_session_maker(engine)
proceed_schemas(engine, Base.metadata)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)