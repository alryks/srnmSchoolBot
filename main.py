from settings import TOKEN

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import handlers

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

if __name__ == '__main__':
    executor.start_polling(handlers.dp, skip_updates=True)
