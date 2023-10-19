import os

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.future import select
from sqlalchemy import update, insert, delete
from db.model import invite_message_class, User, SendMessage, Statistics
from sqlalchemy.exc import IntegrityError
from aiogram.utils.keyboard import (ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.result import ChunkedIteratorResult
from aiogram import Bot
from .admin import start, write_info, send_complete_post
from .InviteMessageImageText import back_to_start
from aiogram.exceptions import TelegramRetryAfter
import asyncio
import time


async def SendMessageCommand(message: types.Message, bot: Bot, session_maker: sessionmaker):
    await start(message)
    async with session_maker() as session:
        UserList = await session.execute(select(User).where(User.bot_token == str(os.getenv('token'))))
        UserList = UserList.scalars().all()
        not_available = 0
        available = 0
        result = await session.execute(select(SendMessage))
        result = result.scalar()
        result: SendMessage
        data = {
            'image': result.picture,
            'text': result.message
        }
        tasks = []
        if len(data['image']) == 0:
            for user in UserList:
                tasks.append([bot.send_message(chat_id=user.user_id, text=data['text'], parse_mode='html',
                                               disable_web_page_preview=True), user.user_id])
        else:
            for user in UserList:
                tasks.append([send_complete_post(data, bot, user.user_id), user.user_id])
        counter = 0
        for task in tasks:
            counter += 1
            try:
                await task[0]
                await asyncio.sleep(.05)
                available += 1
            except TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)
                await task[0]
                available += 1

            except Exception as e:
                print(f"Error sending message to {task[1]}: {e}")
                await session.execute(delete(User).where(User.user_id == task[1]))
                await session.commit()
                not_available += 1
                await asyncio.sleep(.05)

    await message.answer(f'Рассылка сделана \n'
                         f'Отправлено: {str(available)} \n'
                         f'Заблокировано или не удалось отправить: {str(not_available)} \n'
                         f'Заняло по времени: {time.strftime("%H:%M:%S", time.gmtime(counter * 0.001875))}'
                         )
    async with session_maker() as session:
        stmt = await session.execute(select(Statistics))
        result = stmt.scalar()
        if result is None:
            print('DONE')
            await session.execute(insert(Statistics).values(blocked=not_available, available=available))
            await session.commit()
        else:
            print('DONE2')
            await session.execute(update(Statistics).where(Statistics.id == 1).values(
                blocked=not_available,
                available=available
            ))


async def SendMessageKeyboard(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text='Отправить'),
        KeyboardButton(text='Назад')
    )

    await message.answer(text='Сообщение готово',
                         reply_markup=ReplyKeyboardMarkup(keyboard=builder.export(), resize_keyboard=True))
