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
from .admin import start, write_info, set_state_file_id, send_complete_post


# Send Present Post
async def send_post(message: types.Message, bot: Bot, session_maker: sessionmaker):
    async with session_maker() as session:
        stmt = await session.execute(select(invite_message_class).where(invite_message_class.id==1))
        result = stmt.scalars().first()
        print(result.id)
        caption = result.invite_message
        photo_id = result.invite_picture
        data = {
            'image': photo_id,
            'text': caption
        }
        print('Photo: ', photo_id)
        await session.commit()
    if len(photo_id) == 0:
        await bot.send_message(chat_id=message.from_user.id, text=caption, parse_mode='html',
                               disable_web_page_preview=True)
    else:
        await send_complete_post(data, bot, message.from_user.id)


# Invite Message State Class
class InviteMessage(StatesGroup):
    waiting_for_select = State()
    # State Image + Text
    waiting_for_image = State()
    waiting_for_text = State()
    # State Only Text Message
    waiting_for_only_text = State()
    # State Only Image Message
    waiting_for_only_image = State()


async def invite_message_menu(message: types.Message, state: FSMContext) -> None:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text='Картинка + Текст'),
        KeyboardButton(text='Картинка'),
        KeyboardButton(text='Текст')
    )
    builder.row(
        KeyboardButton(text='Назад'),
        KeyboardButton(text='Текущий пост'),
    )
    await message.answer(
        text='Пригласительное',
        reply_markup=ReplyKeyboardMarkup(keyboard=builder.export(), resize_keyboard=True)
    )
    await state.set_state(InviteMessage.waiting_for_select)


async def set_image_text_message(message: types.Message, state: FSMContext):
    await message.reply('Отправь мне картинку')
    await state.set_state(InviteMessage.waiting_for_image)


async def imageText_image_set(message: types.Message, state: FSMContext):
    await set_state_file_id(message, state)
    await message.answer('Введите текст приглашения')
    await state.set_state(InviteMessage.waiting_for_text)


async def imageText_text_set(message: types.Message, state: FSMContext, session_maker: sessionmaker, bot: Bot):
    data = await state.update_data(text=message.html_text)
    await write_info(variable=data, model_class=invite_message_class, session_maker=session_maker)
    await send_complete_post(data, bot, message.from_user.id)
    await state.clear()
    return await back_to_start(message, state)


async def back_to_start(message: types.Message, state: FSMContext):
    await state.clear()
    return await start(message)
