import os

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
from .InviteMessageImageText import InviteMessage, back_to_start


async def get_only_image(message: types.Message, state: FSMContext):
    await message.reply('Отправь мне картинку/видео/гифку')
    await state.set_state(InviteMessage.waiting_for_only_image)


async def set_only_image(message: types.Message, state: FSMContext, session_maker: sessionmaker, bot: Bot):
    text = ''
    await set_state_file_id(message, state)
    data = await state.get_data()
    await write_info(variable=data, model_class=invite_message_class, session_maker=session_maker)
    await send_complete_post(data, bot, message.from_user.id)
    await state.clear()
    await back_to_start(message, state)
