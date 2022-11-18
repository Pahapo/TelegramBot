from create_bot import dp, bot, session
from aiogram import Dispatcher, types
from aiogram import types
import asyncio
from aiogram.utils.exceptions import BotBlocked, CantInitiateConversation
from model import invite_message_class
from .admin import photo_id, caption_message
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
        
def reg_handlers_other(dp : Dispatcher):
    dp.register_chat_join_request_handler(inviteApplyMessage)


