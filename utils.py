from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext

from langs import langs

from models import *

from db.main import connect
from db.model import Class

import sqlalchemy

content_types = ['audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact']
all_states = [*ClassStates.all_states,
              *GroupStates.all_states,
              *LessonStates.all_states,
              *SettingsStates.all_states,
              None]


def markdownv2(text: str) -> str:
    symbols = ['[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for s in symbols:
        text = text.replace(s, '\\' + s)
    return text


def choose_language(message: Message) -> str:
    s = connect()
    try:
        lang = s.query(Class.lang).filter(Class.chat_id == message.chat.id).one()[0]
    except sqlalchemy.exc.NoResultFound:
        lang = 'en'
    s.close()
    return lang


def is_int(string: str):
    try:
        n = int(string)
    except ValueError:
        return False
    return True


async def alert(callback: CallbackQuery, show_alert=False):
    buts = []
    for i in callback.values['message']['reply_markup']['inline_keyboard']:
        buts += i
    for i in buts:
        if i['callback_data'] == callback.data:
            await callback.answer(i['text'], show_alert=show_alert)
            break


async def too_fast(callback: CallbackQuery, seconds, show_alert=False):
    lang = choose_language(callback.message)

    await callback.answer(langs[lang]['too_fast'].format(seconds=seconds), show_alert=show_alert)
