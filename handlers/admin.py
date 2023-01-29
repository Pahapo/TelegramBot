from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.future import select
from sqlalchemy import update, insert
from db.model import invite_message_class, User
from sqlalchemy.exc import IntegrityError
from aiogram.utils.keyboard import (ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton)
from sqlalchemy.orm import sessionmaker
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
# TODO




async def write_info(variable, session_maker: sessionmaker):
    async with session_maker() as session:
        await session.execute(update(invite_message_class).where(invite_message_class.id == 1).values(
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
        stmt = await session.execute(select(invite_message_class))
        result = stmt.scalars().first()
        print(result.id)
        caption = result.invite_message
        photo_id = result.invite_picture
        try:
            stm = await session.execute(insert(User).values(user_id=str(chat_member.from_user.id)))
        except IntegrityError:
            print('Already exists: ' + str(chat_member.from_user.id))
        await session.commit()
    print('send photo')
    try:
        if len(photo_id) == 0:
            await bot.send_message(chat_id=chat_member.from_user.id, text=caption)
        else:
            await bot.send_photo(chat_id=chat_member.from_user.id, photo=photo_id, caption=caption)
    except TelegramForbiddenError:
        print('bot blocked')
