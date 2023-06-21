from aiogram import Bot, Dispatcher
from DataBase import DataBase
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
db = DataBase()