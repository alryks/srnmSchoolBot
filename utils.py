from aiogram.types import Message

from db.main import connect
from db.model import Class

import sqlalchemy

content_types = ['audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact']


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
