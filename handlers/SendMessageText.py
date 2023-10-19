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
from .admin import start, write_info
from .InviteMessageImageText import back_to_start
from .SendMessageImageText import writeMessageForSendMessage, SendMessageState
from .DoSendMessage import SendMessageKeyboard


async def getOnlyText_Send(message: types.Message, state: FSMContext):
    await message.reply('Отправь мне текст')
    await state.set_state(SendMessageState.waiting_for_only_text)


async def SetOnlyText_Send(message: types.Message, state: FSMContext, session_maker: sessionmaker, bot: Bot):
    await state.update_data(image='', text=message.html_text)
    data = await state.get_data()
    await writeMessageForSendMessage(variable=data, model_class=SendMessage, session_maker=session_maker)
    await bot.send_message(message.from_user.id, text=data['text'], parse_mode='html', disable_web_page_preview=True)
    await state.set_state(SendMessageState.waiting_for_send)
    await SendMessageKeyboard(message)
