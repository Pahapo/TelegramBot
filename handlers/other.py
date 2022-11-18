from create_bot import dp, bot, session
from aiogram import Dispatcher, types
from aiogram import types
import asyncio
from aiogram.utils.exceptions import BotBlocked, CantInitiateConversation
from model import invite_message_class
from .admin import photo_id, caption_message
from .admin import ADMIN_ID, SEC_ADMIN, trd
# @dp.chat_join_request_handler()



async def inviteApplyMessage(chat_member: types.ChatJoinRequest):
    try:
        await bot.send_photo(chat_id= chat_member.from_user.id,photo=photo_id , caption=caption_message)
    except BotBlocked:
        asyncio.sleep(0.1)
        print('Bot Blocked:'+str(chat_member.from_user.id))
    except CantInitiateConversation:
        asyncio.sleep(0.1)
        print('Cant Initiate Dialog:'+str(chat_member.from_user.id))


async def print_invite(chat_member: types.Message):
    if chat_member.from_user.id != ADMIN_ID or chat_member.from_user.id != SEC_ADMIN or chat_member.from_user.id != trd:
       await bot.send_photo(chat_member.from_user.id, photo=photo_id, caption=caption_message)
        
def reg_handlers_other(dp : Dispatcher):
    dp.register_chat_join_request_handler(inviteApplyMessage)
    dp.register_message_handler(print_invite, commands='invite')

