import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InputFile

api_file = open('api.txt', 'r')
API = api_file.read()
api_file.close

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)