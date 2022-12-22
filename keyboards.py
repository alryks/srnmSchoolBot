from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.dispatcher.dispatcher import FSMContext
from langs import langs

from db.main import connect
from db.model import *

from utils import *

import datetime


def create_inline_keyboard(buttons, width=3):
    ikm = InlineKeyboardMarkup(row_width=width)
    for row in buttons:
        ikm.add(*row)

    return ikm


def settings(action, data=None):
    fields = create_button_text(action, 'settings')
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()

    rows.append([
        InlineKeyboardButton(fields['lang'].format(lang=data['lang']), callback_data='settings_lang')
    ])
    rows.append([
        InlineKeyboardButton(cancel, callback_data='settings_cancel')
    ])

    return create_inline_keyboard(rows)


def class_create_name(action, data=None):
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()
    rows.append([
        InlineKeyboardButton(cancel, callback_data='class_create_name_cancel')
    ])

    return create_inline_keyboard(rows)


def class_choose(action, data=None):
    fields = create_button_text(action, 'class_choose')
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()

    rows.append([
        InlineKeyboardButton(fields['add_class'], callback_data='class_choose_add')
    ])
    for i in range(len(data)):
        rows.append([
            InlineKeyboardButton(data[i].name, callback_data=f'class_choose_{data[i].id}')
        ])
    rows.append([
        InlineKeyboardButton(cancel, callback_data='class_choose_cancel')
    ])

    return create_inline_keyboard(rows)


def class_now(action):
    fields = create_button_text(action, 'class_now')
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()

    rows.append([
        InlineKeyboardButton(fields['groups'], callback_data='class_now_groups')
    ])
    rows.append([
        InlineKeyboardButton(fields['name'], callback_data='class_now_name')
    ])
    rows.append([
        InlineKeyboardButton(fields['settings'], callback_data='class_now_settings')
    ])
    rows.append([
        InlineKeyboardButton(fields['delete'], callback_data='class_now_delete')
    ])
    rows.append([
        InlineKeyboardButton(back, callback_data='class_now_back')
    ])

    return create_inline_keyboard(rows)


def class_change_name(action):
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()
    rows.append([
        InlineKeyboardButton(back, callback_data='class_change_name_back')
    ])

    return create_inline_keyboard(rows)


def class_settings(action, data):
    fields = create_button_text(action, 'class_settings')
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()

    rows.append([
        InlineKeyboardButton(fields['admins'], callback_data='class_settings_admins')
    ])
    rows.append([
        InlineKeyboardButton(fields['lang'].format(lang=data.lang), callback_data='class_settings_lang')
    ])
    rows.append([
        InlineKeyboardButton(fields['notify'].format(notify="✅" if data.notify else "❌"), callback_data='class_settings_notify')
    ])
    rows.append([
        InlineKeyboardButton(fields['time'], callback_data='class_settings_time')
    ])
    rows.append([
        InlineKeyboardButton(fields['tz'].format(tz="+" + str(data.tz) if data.tz >= 0 else str(data.tz)), callback_data='class_settings_tz')
    ])
    rows.append([
        InlineKeyboardButton(back, callback_data='class_settings_back')
    ])

    return create_inline_keyboard(rows)


def class_delete(action):
    fields = create_button_text(action, 'class_delete')
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()

    rows.append([
        InlineKeyboardButton(fields['yes'], callback_data='class_delete_yes'),
        InlineKeyboardButton(fields['no'], callback_data='class_delete_no'),
    ])

    return create_inline_keyboard(rows)


def class_admins(action, data):
    fields = create_button_text(action, 'class_admins')
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()

    rows.append(
        [InlineKeyboardButton(back, callback_data='class_admins_back')]
    )

    rows.append(
        [InlineKeyboardButton(action.from_user.id, callback_data=f'none_class_admin_{action.from_user.id}')]
    )

    for admin in data:
        if int(admin) != action.from_user.id:
            rows.append([
                InlineKeyboardButton(admin, callback_data=f'none_class_admin_{admin}'),
                InlineKeyboardButton('❌', callback_data=f'class_admin_{admin}'),
            ])

    rows.append(
        [InlineKeyboardButton(fields['add_admin'], callback_data='class_add_admin')]
    )

    return create_inline_keyboard(rows)


def class_add_admin(action):
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()
    rows.append([
        InlineKeyboardButton(back, callback_data='class_add_admin_back')
    ])

    return create_inline_keyboard(rows)


def class_settings_tz(action, data):
    fields = create_button_text(action, 'class_settings_tz')
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()

    rows.append([
        InlineKeyboardButton(back, callback_data='class_settings_tz_back'),
    ])

    for key in fields.keys():
        if int(key) == data.tz:
            rows.append([InlineKeyboardButton("✅ " + fields[key], callback_data=f'class_settings_tz_{key}')])
        else:
            rows.append([InlineKeyboardButton(fields[key], callback_data=f'class_settings_tz_{key}')])

    return create_inline_keyboard(rows)


def class_settings_time(action, data):
    fields = create_button_text(action, 'class_settings_time')
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()

    rows.append([
        InlineKeyboardButton(back, callback_data='class_settings_time_back'),
    ])

    rows.append([
        InlineKeyboardButton(fields['day'], callback_data='none_class_settings_time_day'),
    ])

    rows.append([
        InlineKeyboardButton('◀', callback_data='class_settings_time_hrs_left'),
        InlineKeyboardButton(fields['hrs'].format(hrs=data['hrs']), callback_data='none_class_settings_time_hrs'),
        InlineKeyboardButton('▶', callback_data='class_settings_time_hrs_right'),
    ])

    rows.append([
        InlineKeyboardButton('◀', callback_data='class_settings_time_mins_left'),
        InlineKeyboardButton(fields['mins'].format(mins=data['mins']), callback_data='none_class_settings_time_mins'),
        InlineKeyboardButton('▶', callback_data='class_settings_time_mins_right'),
    ])

    rows.append([
        InlineKeyboardButton(fields['lesson'], callback_data='none_class_settings_time_lesson'),
    ])

    rows.append([
        InlineKeyboardButton('◀', callback_data='class_settings_time_gap_left'),
        InlineKeyboardButton(fields['gap'].format(gap=data['gap']), callback_data='none_class_settings_time_gap'),
        InlineKeyboardButton('▶', callback_data='class_settings_time_gap_right'),
    ])

    rows.append([
        InlineKeyboardButton(fields['save'], callback_data='class_settings_time_save'),
    ])

    return create_inline_keyboard(rows)


def group_create_name(action):
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()
    rows.append([
        InlineKeyboardButton(back, callback_data='group_create_name_back')
    ])

    return create_inline_keyboard(rows)


def group_choose(action, data):
    fields = create_button_text(action, 'group_choose')
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()

    rows.append([
        InlineKeyboardButton(fields['add'], callback_data='group_choose_add')
    ])

    for group in data:
        rows.append([
        InlineKeyboardButton(group.name, callback_data=f'group_choose_{group.id}')
    ])

    rows.append([
        InlineKeyboardButton(back, callback_data='group_choose_back')
    ])

    return create_inline_keyboard(rows)

def group_now(action):
    fields = create_button_text(action, 'group_now')
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()

    rows.append([
        InlineKeyboardButton(back, callback_data='group_now_back')
    ])

    rows.append([
        InlineKeyboardButton(fields['name'], callback_data='group_now_name')
    ])

    rows.append([
        InlineKeyboardButton(fields['timetable'], callback_data='group_now_timetable')
    ])

    rows.append([
        InlineKeyboardButton(fields['delete'], callback_data='group_now_delete')
    ])

    return create_inline_keyboard(rows)


def group_change_name(action):
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()
    rows.append([
        InlineKeyboardButton(back, callback_data='group_change_name_back')
    ])

    return create_inline_keyboard(rows)


def group_delete(action):
    fields = create_button_text(action, 'group_delete')
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()

    rows.append([
        InlineKeyboardButton(fields['yes'], callback_data='group_delete_yes'),
        InlineKeyboardButton(fields['no'], callback_data='group_delete_no'),
    ])

    return create_inline_keyboard(rows)
