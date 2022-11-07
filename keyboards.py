from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.dispatcher.dispatcher import FSMContext
from langs import langs

from db.main import connect
from db.model import *

from utils import choose_language


def create_inline_keyboard(buttons, width=3):
    ikm = InlineKeyboardMarkup(row_width=width)
    for row in buttons:
        ikm.add(*row)

    return ikm


async def edit_class(message: Message, state: FSMContext):
    lang = choose_language(message)

    rows = list()

    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['edit_class']['name'], callback_data='name_edit_class')])
    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['edit_class']['delete'], callback_data='delete_edit_class')])
    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['edit_class']['cancel'], callback_data='cancel_edit_class')])

    return create_inline_keyboard(rows)


async def class_name(message: Message, state: FSMContext):
    lang = choose_language(message)

    rows = list()

    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['new_class']['cancel'], callback_data='cancel_edit_class_name')])

    return create_inline_keyboard(rows)


async def delete_class(message: Message, state: FSMContext):
    lang = choose_language(message)

    rows = list()

    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['delete_class']['yes'], callback_data='yes_delete_class'),
                 InlineKeyboardButton(langs[lang]['keyboards']['delete_class']['no'], callback_data='no_delete_class')])

    return create_inline_keyboard(rows)


async def sure_delete_class(message: Message, state: FSMContext):
    lang = choose_language(message)

    rows = list()

    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['sure_delete_class']['yes'], callback_data='yes_sure_delete_class')])
    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['sure_delete_class']['no'], callback_data='no_sure_delete_class')])

    return create_inline_keyboard(rows)


async def settings(message: Message, state: FSMContext):
    lang = choose_language(message)

    rows = list()

    s = connect()
    editclass = s.query(Class).filter(Class.chat_id == message.chat.id).one()

    current_timezone = str(editclass.timezone) if editclass.timezone < 0 else '+' + str(editclass.timezone)

    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['settings']['lang'].format(lang=editclass.lang), callback_data='lang')])
    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['settings']['notify'].format(notify='✅' if editclass.notify else '❌'), callback_data='notify')])
    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['settings']['timezone'].format(timezone=current_timezone), callback_data='timezone')])
    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['settings']['time'], callback_data='time_settings')])
    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['settings']['cancel'], callback_data='cancel_settings')])

    return create_inline_keyboard(rows)


async def timezone(message: Message, state: FSMContext):
    lang = choose_language(message)

    rows = list()

    s = connect()
    editclass = s.query(Class).filter(Class.chat_id == message.chat.id).one()
    current_timezone = editclass.timezone

    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['timezone']['back'], callback_data='back_timezone')])
    for i in range(-12, 15):
        text = langs[lang]['keyboards']['timezone'][str(i) if i < 0 else '+' + str(i)]
        if i == current_timezone:
             text += " ✅"
        rows.append([InlineKeyboardButton(text, callback_data=str(i))])

    return create_inline_keyboard(rows)


async def time_settings(message: Message, state: FSMContext):
    lang = choose_language(message)

    async with state.proxy() as data:
        before = data['before']
        hrs = data['hrs']
        mins = data['mins']

    rows = list()

    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['time_settings']['save'], callback_data='save_time_settings')])
    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['time_settings']['lesson'], callback_data='none_time_settings_1')])
    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['time_settings']['left'], callback_data='left_before'),
                 InlineKeyboardButton(langs[lang]['keyboards']['time_settings']['before'].format(mins=before), callback_data='none_time_settings_2'),
                 InlineKeyboardButton(langs[lang]['keyboards']['time_settings']['right'], callback_data='right_before')])
    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['time_settings']['day'], callback_data='none_time_settings_3')])
    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['time_settings']['left'], callback_data='left_hrs'),
                 InlineKeyboardButton(langs[lang]['keyboards']['time_settings']['hours'].format(hours=hrs), callback_data='none_time_settings_4'),
                 InlineKeyboardButton(langs[lang]['keyboards']['time_settings']['right'], callback_data='right_hrs')])
    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['time_settings']['left'], callback_data='left_mins'),
                 InlineKeyboardButton(langs[lang]['keyboards']['time_settings']['minutes'].format(mins=mins), callback_data='none_time_settings_5'),
                 InlineKeyboardButton(langs[lang]['keyboards']['time_settings']['right'], callback_data='right_mins')])
    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['time_settings']['back'], callback_data='back_time_settings')])

    return create_inline_keyboard(rows)