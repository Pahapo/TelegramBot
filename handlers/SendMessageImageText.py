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
from .admin import start, write_info, set_state_file_id, send_complete_post
from .InviteMessageImageText import back_to_start
from .DoSendMessage import SendMessageKeyboard


async def get_SendMessage(message: types.Message, bot: Bot, session_maker: sessionmaker):
    async with session_maker() as session:
        stmt = await session.execute(select(SendMessage))
        result = stmt.scalars().first()
        print(result.id)
        data = {
            'image': result.picture,
            'text': result.message
        }
        await session.commit()
    if len(data['image']) == 0:
        await bot.send_message(chat_id=message.from_user.id, text=data['text'], parse_mode='html',
                               disable_web_page_preview=True)
    else:
        await send_complete_post(data, bot, message.from_user.id)


async def writeMessageForSendMessage(variable, model_class, session_maker: sessionmaker):
    async with session_maker() as session:
        SendMessageTuple: ChunkedIteratorResult
        SendMessageTuple = await session.execute(select(model_class))
        SendMessageTuple = SendMessageTuple.scalar()
        if SendMessageTuple is None:
            await session.execute(insert(model_class).values(message=variable['text'], picture=variable['image']))
            await session.commit()
        else:
            await session.execute(update(model_class).where(model_class.id == 1).values(
                message=variable['text'],
                picture=variable['image']))
            await session.commit()


class SendMessageState(StatesGroup):
    waiting_for_select = State()
    # State Image + Text
    waiting_for_image = State()
    waiting_for_text = State()
    # State Only Text Message
    waiting_for_only_text = State()
    # State Only Image Message
    waiting_for_only_image = State()
    # PreSendState
    waiting_for_send = State()


async def send_messages_keyboard(message: types.Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text='Картинка + Текст'),
        KeyboardButton(text='Картинка'),
        KeyboardButton(text='Текст'),

    )
    builder.row(KeyboardButton(text='Cтатистика'))
    builder.row(
        KeyboardButton(text='Назад'),
        KeyboardButton(text='Текущее сообщение'),
    )
    await message.answer(
        text='Рассылка',
        reply_markup=ReplyKeyboardMarkup(keyboard=builder.export(), resize_keyboard=True)
    )
    await state.set_state(SendMessageState.waiting_for_select)


async def SendMessage_image_send(message: types.Message, state: FSMContext):
    await message.reply('Отправь мне картинку/гифку/видео')
    await state.set_state(SendMessageState.waiting_for_image)


async def SendMessage_image_set(message: types.Message, state: FSMContext):
    await set_state_file_id(message, state)
    await message.answer('Введите текст приглашения')
    await state.set_state(SendMessageState.waiting_for_text)


async def SendMessage_text_set(message: types.Message, state: FSMContext, session_maker: sessionmaker, bot: Bot):
    data = await state.update_data(text=message.html_text)
    await writeMessageForSendMessage(variable=data, model_class=SendMessage, session_maker=session_maker)
    await send_complete_post(data, bot, message.from_user.id)
    await state.set_state(SendMessageState.waiting_for_send)
    await SendMessageKeyboard(message)
