from settings import TOKEN, ADMINS

from db.main import *

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from aiogram.contrib.fsm_storage.memory import MemoryStorage

import handlers


async def on_startup(_):
    for ADMIN in ADMINS:
        await bot.send_message(ADMIN, '_For admins_\n\nBot is started\!')

    try:
        connect()
    except:
        initialise()

storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot=bot, storage=storage)

if __name__ == '__main__':
    executor.start_polling(handlers.dp, skip_updates=True, on_startup=on_startup)
