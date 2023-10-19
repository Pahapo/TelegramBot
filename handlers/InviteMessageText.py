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
from .admin import start, write_info
from .InviteMessageImageText import InviteMessage, back_to_start


async def get_only_text(message: types.Message, state: FSMContext):
    await message.reply('Отправь мне текст')
    await state.set_state(InviteMessage.waiting_for_only_text)


async def set_only_text(message: types.Message, state: FSMContext, session_maker: sessionmaker, bot: Bot):
    await state.update_data(image='', text=message.html_text)
    data = await state.get_data()
    await write_info(variable=data,model_class=invite_message_class, session_maker=session_maker)
    await bot.send_message(message.from_user.id, text=data['text'], parse_mode='html', disable_web_page_preview=True)
    await state.clear()
    await back_to_start(message)
