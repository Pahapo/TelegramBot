import asyncio

from aiogram import Dispatcher, types
from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import os
from sqlalchemy.future import select
from model import invite_message_class, User
from create_bot import session_maker
from psycopg2.errors import UniqueViolation
from aiogram.utils.exceptions import BotBlocked, CantInitiateConversation
from sqlalchemy.exc import IntegrityError

ADMIN_ID = int(os.getenv("ADMIN_ID"))
SEC_ADMIN = int(os.getenv("SEC_ADMIN"))
trd = int(os.getenv("trd"))

# engine_session = session()
# t = engine_session.query(invite_message_class).filter(invite_message_class.id == 1).all()
# photo_id = t[0].invite_picture
# caption_message = t[0].invite_message
# engine_session.commit()

photo_id = ''
caption = ''


async def get_invite_message():
    async with session_maker() as session:
        async with session.begin():
            stmt = await session.execute(select(invite_message_class))
            result = stmt.first()
            print(result)
            global caption
            caption = result.invite_message
            global photo_id
            photo_id = result.invite_picture


asyncio.run(get_invite_message())


class FSMAdmin(StatesGroup):
    photo = State()
    invite = State()


async def block_bot(message: types.Message):
    if message.from_user.id == ADMIN_ID or message.from_user.id == SEC_ADMIN or message.from_user.id == trd:
        await bot.send_message(message.from_user.id, 'Welcome')
    else:
        await bot.send_message(message.from_user.id, 'Not Enough Permissions')


# async def register_new_admin(message: types.ChatMemberOwner):
#     global ID
#     member = await bot.get_chat_member(message.chat.id, message.from_user.id)
#     if (member.is_chat_member()):
#         ID = message.from_user.id

#     await message.delete()
#     print(ID)

async def change_invite_start(message: types.Message):
    if message.from_user.id == ADMIN_ID or message.from_user.id == SEC_ADMIN or message.from_user.id == trd:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')
    else:
        await bot.send_message(message.from_user.id, 'Not Enough Permissions')


async def load_invite_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Введи пригласительное сообщение')


async def load_invite_message(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['invite'] = message.text
        global photo_id
        photo_id = data['photo']
        print(photo_id)
        global caption_message
        caption_message = data['invite']
        print(caption_message)
        await write_info(data)
        print(caption_message)
        await bot.send_photo(chat_id=message.from_user.id, photo=data['photo'], caption=data['invite'])
        await state.finish()


async def print_invite(chat_member: types.Message):
    if chat_member.from_user.id == ADMIN_ID or chat_member.from_user.id == SEC_ADMIN or chat_member.from_user.id == trd:
        await bot.send_photo(chat_member.from_user.id, photo=photo_id, caption=caption_message)


async def inviteApplyMessage(chat_member: types.ChatJoinRequest):
    try:
        await bot.send_photo(chat_id=chat_member.from_user.id, photo=photo_id, caption=caption_message)
    except BotBlocked:
        print('Bot Blocked:' + str(chat_member.from_user.id))
    except CantInitiateConversation:
        print('Cant Initiate Dialog:' + str(chat_member.from_user.id))


async def error_command(message: types.Message):
    if message.from_user.id == ADMIN_ID or message.from_user.id == SEC_ADMIN or message.from_user.id == trd:
        await bot.send_message(message.from_user.id, "Нет такой комманды")
    else:
        await bot.send_message(message.from_user.id, 'Not Enough permissions')


# async def invite_message(message: types.Message):
#     await bot.send_message(message.from_user.id,open("inputtext.txt","r").read())

def reg_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(change_invite_start, commands=['Пригласительное'], state=None)
    dp.register_message_handler(load_invite_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_invite_message, state=FSMAdmin.invite)
    dp.register_message_handler(block_bot, commands='start')
    dp.register_message_handler(print_invite, commands=['invite'])
    dp.register_chat_join_request_handler(inviteApplyMessage)
    dp.register_message_handler(error_command)
    # dp.register_message_handler(invite_message, commands=['йоу'])
    # dp.register_message_handler(register_new_admin, commands=['register'])


async def write_info(variable):
    session_engine = session()
    session_engine.query(invite_message_class).filter(invite_message_class.id == 1).update(
        {"invite_message": variable['invite'], "invite_picture": variable['photo']})
    session_engine.commit()
