from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from langs import langs


def create_inline_keyboard(buttons, width=3):
    ikm = InlineKeyboardMarkup(row_width=width)
    for row in buttons:
        ikm.add(*row)

    return ikm


def edit_class(message: Message, lang):
    rows = list()

    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['edit_class']['name'], callback_data='name')])
    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['edit_class']['delete'], callback_data='delete')])
    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['edit_class']['cancel'], callback_data='cancel')])

    return create_inline_keyboard(rows)


def class_name(message: Message, lang):
    rows = list()

    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['new_class']['cancel'], callback_data='cancel')])

    return create_inline_keyboard(rows)


def delete_class(message: Message, lang):
    rows = list()

    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['delete_class']['yes'], callback_data='yes'),
                 InlineKeyboardButton(langs[lang]['keyboards']['delete_class']['no'], callback_data='no')])

    return create_inline_keyboard(rows)


def sure_delete_class(message: Message, lang):
    rows = list()

    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['sure_delete_class']['yes'], callback_data='yes')])
    rows.append([InlineKeyboardButton(langs[lang]['keyboards']['sure_delete_class']['no'], callback_data='no')])

    return create_inline_keyboard(rows)
