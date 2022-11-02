from operator import inv
from create_bot import dp, bot, photo_id, invite_ms
from aiogram import Dispatcher, types


# @dp.chat_join_request_handler()
async def inviteApplyMessage(chat_member: types.ChatJoinRequest):
    await chat_member.approve()
    await bot.send_photo(chat_id= chat_member.from_user.id,photo=open("inputfile.txt","r").read() , caption=open("inputtext.txt","r").read())



def reg_handlers_other(dp : Dispatcher):
    dp.register_chat_join_request_handler(inviteApplyMessage)


