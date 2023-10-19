from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from typing import Callable, Dict, Any, Awaitable
import os

ADMIN_ID = int(os.getenv("ADMIN_ID"))
SEC_ADMIN = int(os.getenv("SEC_ADMIN"))
trd = int(os.getenv("trd"))

admin_list = [ADMIN_ID, SEC_ADMIN, trd]


class AdminCheckMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if event.from_user.id not in admin_list:
            try:
                await event.answer('Вы не администратор')
            except TelegramBadRequest:
                print('Невозможно связаться с:', event.from_user.id)
        else:
            return await handler(event, data)
