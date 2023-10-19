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
from handlers.SendMessageImageText import SendMessageState
from handlers.DoSendMessage import SendMessageCommand, SendMessageKeyboard
from handlers.SendMessageImageText import (send_messages_keyboard, SendMessage_image_send, SendMessage_image_set,
                                           SendMessage_text_set, get_SendMessage)
from handlers.SendMessageImage import (getOnlyImage_Send, SetOnlyImage_Send)
from handlers.SendMessageText import (getOnlyText_Send, SetOnlyText_Send)
from handlers.Statistics import get_statistics_by_user


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

    # NEWS
    router.message.register(send_messages_keyboard, F.text == 'Рассылка')
    router.message.register(SendMessage_image_send, F.text == 'Картинка + Текст', SendMessageState.waiting_for_select)
    router.message.register(SendMessage_image_set, SendMessageState.waiting_for_image)
    router.message.register(SendMessage_text_set, SendMessageState.waiting_for_text)
    router.message.register(get_SendMessage, F.text == 'Текущее сообщение')
    router.message.register(SendMessageCommand, F.text == 'Отправить', SendMessageState.waiting_for_send)
    router.message.register(getOnlyImage_Send, F.text == 'Картинка', SendMessageState.waiting_for_select)
    router.message.register(SetOnlyImage_Send, SendMessageState.waiting_for_only_image)
    router.message.register(getOnlyText_Send, F.text == 'Текст', SendMessageState.waiting_for_select)
    router.message.register(get_statistics_by_user, F.text == 'Cтатистика', SendMessageState.waiting_for_select)
    router.message.register(SetOnlyText_Send, SendMessageState.waiting_for_only_text)
    # Middleware
    # Middlewares Should be in the of all handlers
    router.message.register(AdminCheckMiddleware)
