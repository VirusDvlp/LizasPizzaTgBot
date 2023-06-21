from aiogram import executor
from create_bot import dp
from register_handlers import register_handlers


async def __on_startup(dp):
    register_handlers(dp)
    print('Бот успешно запущен')


def main():
    executor.start_polling(dispatcher=dp, skip_updates=False, on_startup=__on_startup)
