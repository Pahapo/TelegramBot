from create_bot import dp, bot, session
from aiogram import Dispatcher, types
from aiogram import types
import asyncio
from aiogram.utils.exceptions import BotBlocked, CantInitiateConversation
from model import invite_message_class
# @dp.chat_join_request_handler()

engine_session = session()
t = engine_session.query(invite_message_class).filter(invite_message_class.id == 1).all()

photo_id = t[0].invite_picture
caption_message = t[0].invite_message


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


