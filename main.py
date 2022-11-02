from aiogram import executor
from create_bot import dp


from handlers import admin, client, other

admin.reg_handlers_admin(dp)
# client.reg_handlers_client(dp)
other.reg_handlers_other(dp)


executor.start_polling(dp, skip_updates=True)


