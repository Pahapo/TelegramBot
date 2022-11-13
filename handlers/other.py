from create_bot import dp, bot
from aiogram import Dispatcher, types
from aiogram import types
import asyncio
from aiogram.utils.exceptions import BotBlocked, CantInitiateConversation
# @dp.chat_join_request_handler()
async def inviteApplyMessage(chat_member: types.ChatJoinRequest):
    try:
        await bot.send_photo(chat_id= chat_member.from_user.id,photo=open("inputfile.txt","r").read() , caption=open("inputtext.txt","r").read())
    except BotBlocked:
        asyncio.sleep(0.1)
        print('Bot Blocked:'+str(chat_member.from_user.id))
    except CantInitiateConversation:
        asyncio.sleep(0.1)
        print('Cant Initiate Dialog:'+str(chat_member.from_user.id))

def reg_handlers_other(dp : Dispatcher):
    dp.register_chat_join_request_handler(inviteApplyMessage)


