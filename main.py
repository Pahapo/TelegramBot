import os

import asyncio


from handlers import register_commands
import logging
from aiogram import Dispatcher, Bot
from db import BaseModel, get_session_maker, create_async_engine
from aiogram.dispatcher.dispatcher import MemoryStorage

DEBUG = True
from middlewares.admin_check import AdminCheckMiddleware


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_startup_debug(dispatcher):
    async with session_maker() as session:
        await proceed_schemas(async_engine, Base.metadata)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.message.middleware(AdminCheckMiddleware())
    register_commands(dp)
    
    bot = Bot(token=os.getenv('token'))
    async_engine = create_async_engine(
        os.getenv('asyncpg_db'))
    session_maker = get_session_maker(async_engine)
        #  TO ALEMBIC
        # await proceed_schemas(async_engine, BaseModel.metadata)
    await dp.start_polling(bot, session_maker=session_maker, skip_updates=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
