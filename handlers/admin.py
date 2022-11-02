from aiogram import Dispatcher, types
from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from sec_func import write_info

class FSMAdmin(StatesGroup):
    photo = State()
    invite = State()


async def change_invite_start(message : types.Message):
    await FSMAdmin.photo.set()
    await message.reply('Загрузи фото')

async def load_invite_photo(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Введи пригласительное сообщение')

async def load_invite_message(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['invite'] = message.text
        await write_info(data)
    
    
    await state.finish()


async def invite_message(message: types.Message):
    await bot.send_message(message.from_user.id,"Привет")

def reg_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(change_invite_start, commands= ['Пригласительное'], state=None)
    dp.register_message_handler(invite_message, commands=['йоу'])
    dp.register_message_handler(load_invite_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_invite_message, state=FSMAdmin.invite)
