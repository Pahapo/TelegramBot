from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.future import select
from sqlalchemy import update, insert
from db.model import invite_message_class, User, SendMessage
from sqlalchemy.exc import IntegrityError
from aiogram.utils.keyboard import (ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.result import ChunkedIteratorResult
from aiogram import Bot
from .admin import start, write_info, send_complete_post, set_state_file_id
from .InviteMessageImageText import back_to_start
from .SendMessageImageText import writeMessageForSendMessage, SendMessageState
from .DoSendMessage import SendMessageKeyboard


async def getOnlyImage_Send(message: types.Message, state: FSMContext):
    await message.reply('Отправь мне картинку/гифку/видео')
    await state.set_state(SendMessageState.waiting_for_only_image)


async def SetOnlyImage_Send(message: types.Message, state: FSMContext, session_maker: sessionmaker, bot: Bot):
    text = ''
    await set_state_file_id(message, state)
    data = await state.get_data()
    await writeMessageForSendMessage(variable=data, model_class=SendMessage, session_maker=session_maker)
    await send_complete_post(data, bot, message.from_user.id)
    await state.set_state(SendMessageState.waiting_for_send)
    await SendMessageKeyboard(message)
