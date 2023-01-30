import os

import asyncio
from handlers import register_commands
import logging
from aiogram import Dispatcher, Bot
from db import BaseModel, get_session_maker, proceed_schemas, create_async_engine
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
    if DEBUG == False:
        bot = Bot(token=os.getenv('BOT_TOKEN'))
        HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

        WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
        WEBHOOK_PATH = f'/webhook/{os.getenv("BOT_TOKEN")}'
        WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

        WEBAPP_HOST = '0.0.0.0'
        WEBAPP_PORT = os.getenv('PORT', default=8000)
        async_engine = create_async_engine(
            'postgresql+asyncpg://ogqvnmdkjsxjus:a3bac4e2704930bfcc12377ffe53fee216c6c070f6b72fc7da9ad8a123fa532b@ec2-52-30-159-47.eu-west-1.compute.amazonaws.com:5432/daqu593lifqtvi')
        session_maker = get_session_maker(async_engine)

        await proceed_schemas(async_engine, BaseModel.metadata)
        await dp.start_webhook(bot, skip_updates=True,
                               webhook_path=WEBHOOK_PATH,
                               on_startup=on_startup,
                               on_shutdown=on_shutdown,
                               host=WEBAPP_HOST,
                               port=WEBAPP_PORT,
                               session_maker=session_maker)

    else:
        bot = Bot(token=os.getenv('token'))
        async_engine = create_async_engine(
            "postgresql+asyncpg://ogqvnmdkjsxjus:a3bac4e2704930bfcc12377ffe53fee216c6c070f6b72fc7da9ad8a123fa532b@ec2-52-30-159-47.eu-west-1.compute.amazonaws.com:5432/daqu593lifqtvi")
        session_maker = get_session_maker(async_engine)
        await proceed_schemas(async_engine, BaseModel.metadata)
        await dp.start_polling(bot, session_maker=session_maker, skip_updates=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
