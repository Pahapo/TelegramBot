from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
import os
# ADMIN_ID = int(os.getenv("ADMIN_ID"))
# SEC_ADMIN = int(os.getenv("SEC_ADMIN"))
# trd = int(os.getenv("trd"))
test = 792501294
admin_list = [test]


class AdminCheckMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if event.from_user.id not in admin_list:
            await event.answer('Вы не администратор')
        else:
            return await handler(event, data)
