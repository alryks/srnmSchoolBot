from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.storage import FSMContext

from typing import Union

import settings
from langs import langs

from models import *

from db.main import connect
from db.model import *

import sqlalchemy

all_states = [*GroupStates.all_states, *PrivateStates.all_states, None]

months = {
    1: 'jan',
    2: 'feb',
    3: 'mar',
    4: 'apr',
    5: 'may',
    6: 'jun',
    7: 'jul',
    8: 'aug',
    9: 'sep',
    10: 'oct',
    11: 'nov',
    12: 'dec',
}

weekdays = {
    0: 'mon',
    1: 'tue',
    2: 'wed',
    3: 'thi',
    4: 'fri',
    5: 'sat',
    6: 'sun',
}


def markdownv2(text: str) -> str:
    symbols = ['[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for s in symbols:
        text = text.replace(s, '\\' + s)
    return text


def remove_markdownv2(text: str) -> str:
    symbols = ['\\', '*', '_']
    for s in symbols:
        text = text.replace('\\' + s, s)
    return text


def choose_language(action: Union[Message, CallbackQuery]):
    if type(action) == CallbackQuery:
        action_message = action.message
    else:
        action_message = action
    if action_message.chat.type == 'private':
        s = connect()
        user = s.query(Users).filter(Users.telegram_id == action.from_user.id)
        if user.count() > 0:
            lang = user.one().lang
        else:
            lang = action.from_user.language_code
    else:
        s = connect()
        clas = s.query(Classes).filter(Classes.chat_id == action_message.chat.id)
        if clas.count() > 0:
            lang = clas.one().lang
        else:
            lang = action.from_user.language_code

    if lang not in settings.LANGS:
        lang = 'en'

    return lang


def create_text(action: Union[Message, CallbackQuery], key, **replace):
    lang = choose_language(action)
    try:
        s = langs[lang][key]
    except KeyError:
        s = langs['en'][key]
    if replace:
        s = s.format(**replace)
    return markdownv2(s)


def create_button_text(action: Union[Message, CallbackQuery], key):
    lang = choose_language(action)
    try:
        s = langs[lang]['keyboards'][key]
    except KeyError:
        s = langs['en']['keyboards'][key]
    return s


def get_user_name(action: Union[Message, CallbackQuery]):
    if action.from_user.username:
        return '@' + action.from_user.username
    else:
        return action.from_user.full_name


async def text_message(action: Union[Message, CallbackQuery], text=None, keyboard=None):
    if type(action) == CallbackQuery:
        if text and text.replace("*", "").replace("_", "").replace("\\", "").strip() != action.message.text.replace("*", "").replace("_", "").replace("\\", "").strip():
            await action.message.edit_text(text, reply_markup=keyboard)
        else:
            if keyboard and keyboard != action.message.reply_markup:
                await action.message.edit_reply_markup(keyboard)
            else:
                await alert(action)
    else:
        if keyboard:
            await action.answer(text, reply_markup=keyboard)
        else:
            await action.answer(text)


async def alert(callback: CallbackQuery, show=False):
    for row in callback.message.reply_markup['inline_keyboard']:
        for button in row:
            if button['callback_data'] == callback.data:
                await callback.answer(button['text'], show_alert=show)