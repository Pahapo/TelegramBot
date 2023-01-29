__all__ = ['register_commands']

from aiogram import Router
from aiogram.filters import Command
from handlers.admin import inviteApplyMessage, start
from handlers.InviteMessageImageText import (InviteMessage, invite_message_menu, set_image_text_message,
                                             imageText_image_set,
                                             imageText_text_set, back_to_start, send_post)

from handlers.InviteMessageImage import get_only_image, set_only_image
from handlers.InviteMessageText import get_only_text, set_only_text
from aiogram import F
from middlewares.admin_check import AdminCheckMiddleware

def register_commands(router: Router) -> None:
    router.message.register(start, Command(commands=['start']))
    router.chat_join_request.register(inviteApplyMessage)
    router.message.register(back_to_start, F.text == 'Назад')

    # Invite Message State
    router.message.register(send_post, F.text == 'Текущий пост')
    # TEXT + IMAGE
    router.message.register(invite_message_menu, F.text == 'Пригласительное')
    router.message.register(set_image_text_message, F.text == 'Картинка + Текст', InviteMessage.waiting_for_select)
    router.message.register(imageText_image_set, InviteMessage.waiting_for_image)
    router.message.register(imageText_text_set, InviteMessage.waiting_for_text)
    # ONLY IMAGE
    router.message.register(get_only_image, InviteMessage.waiting_for_select, F.text == 'Картинка')
    router.message.register(set_only_image, InviteMessage.waiting_for_only_image)
    # ONLY TEXT
    router.message.register(get_only_text, InviteMessage.waiting_for_select, F.text == 'Текст')
    router.message.register(set_only_text, InviteMessage.waiting_for_only_text)
    # router.mesage.register(image_image_set, F.text == 'Картинка', InviteMessage.waiting_for_select)
    # router.mesage.register(text, F.text == 'Текст', InviteMessage.waiting_for_select)
    router.message.register(AdminCheckMiddleware)