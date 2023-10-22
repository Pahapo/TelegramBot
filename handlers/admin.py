import asyncio

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.future import select
from sqlalchemy import update, insert
from db.model import invite_message_class, User
from sqlalchemy.exc import IntegrityError
from aiogram.utils.keyboard import (ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton)
from sqlalchemy.orm import sessionmaker
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from typing import Optional
import os


# TODO
async def set_state_file_id(message: types.Message, state: FSMContext):
    if message.photo:
        await state.update_data(image=message.photo[0].file_id, text='')
    elif message.animation:
        await state.update_data(image=message.animation.file_id, text='')
    elif message.video:
        await state.update_data(image=message.video.file_id, text='')


async def send_complete_post(data, bot: Bot, receiver: int):
    file = await bot.get_file(data['image'])
    file_path = file.file_path
    file_ext = os.path.splitext(file_path)[1]
    if file_ext in ['.jpg', '.jpeg', '.png']:
        return await bot.send_photo(chat_id=receiver, photo=data['image'], caption=data['text'],
                                    parse_mode='html')
    elif file_ext in ['.gif']:
        return await bot.send_animation(chat_id=receiver, animation=data['image'], caption=data['text'],
                                        parse_mode='html')
    elif file_ext in ['.mp4']:
        return await bot.send_video(chat_id=receiver, video=data['image'], caption=data['text'],
                                    parse_mode='html')


async def write_info(variable, model_class, session_maker: sessionmaker):
    '''Write info to model'''
    async with session_maker() as session:
        SendMessageTuple: ChunkedIteratorResult
        SendMessageTuple = await session.execute(select(model_class).where(model_class.id == 1))
        SendMessageTuple = SendMessageTuple.scalar()
        if SendMessageTuple is None:
            await  session.execute(
                insert(model_class).values(invite_message=variable['text'], invite_picture=variable['image']))
            await session.commit()
        else:
            await session.execute(update(model_class).where(model_class.id == 1).values(
                invite_message=variable['text'],
                invite_picture=variable['image']))
            await session.commit()


# Begin keyboard
async def start(message: types.Message) -> None:
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text='Пригласительное'),
        KeyboardButton(text='Рассылка')
    )
    await message.answer(
        text='Функции',
        reply_markup=ReplyKeyboardMarkup(keyboard=builder.export(), resize_keyboard=True)
    )


async def inviteApplyMessage(chat_member: types.ChatJoinRequest, session_maker: sessionmaker, bot: Bot):
    async with session_maker() as session:
        stmt = await session.execute(select(invite_message_class).where(invite_message_class.id == 1))
        result = stmt.scalars().first()
        print(result.id)
        data = {
            'image': result.invite_picture,
            'text': result.invite_message
        }

        try:
            stm = await session.execute(
                insert(User).values(user_id=str(chat_member.from_user.id), bot_token=str(os.getenv('token'))))
        except IntegrityError:
            print('Already exists: ' + str(chat_member.from_user.id))
        await session.commit()
    print(f'sleep: {chat_member.from_user.id}')
    await asyncio.sleep(10)
    print('send photo')
    try:
        if len(data['text']) == 0:
            await bot.send_message(chat_id=chat_member.from_user.id, text=data['text'], parse_mode='html',
                                   disable_web_page_preview=True)
        else:
            await send_complete_post(data, bot, chat_member.from_user.id)
    except Exception as e:
        print(e)
