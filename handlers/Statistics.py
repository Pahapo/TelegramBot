import time

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.future import select
from sqlalchemy import update, insert
from db.model import invite_message_class, User, SendMessage, Statistics
from sqlalchemy.exc import IntegrityError
from aiogram.utils.keyboard import (ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.result import ChunkedIteratorResult
from aiogram import Bot
from .admin import start, write_info, set_state_file_id, send_complete_post
from .InviteMessageImageText import back_to_start
from .DoSendMessage import SendMessageKeyboard


async def get_statistics_by_user(message: types.Message, bot: Bot, session_maker: sessionmaker, state: FSMContext):
    async with session_maker() as session:
        stmt = await session.execute(select(Statistics))
        result = stmt.scalar()
        result: Statistics
        if result:
            prompt = f'Статистика \n' + \
                     f'Отправлено: {result.available}\n' + \
                     f'Заблокировано или не удалось отправить: {result.blocked}\n' + \
                     f'Заняло по времени: ' \
                     f'{time.strftime("%H:%M:%S", time.gmtime(result.available + result.blocked * 0.001875))}'

            await bot.send_message(chat_id=message.from_user.id, text=prompt)
        else:
            prompt = 'Нет информации, сделайте рассылку'
            await bot.send_message(chat_id=message.from_user.id, text=prompt)
