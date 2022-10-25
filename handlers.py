import main
import langs
from aiogram import types

dp = main.dp


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(langs.en['start'].format(name="@" + str(message.from_user.username) if message.from_user.username else "*" + str(message.from_user.full_name) + "*"), parse_mode='markdown')


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer(langs.en['help'], parse_mode='markdown')
