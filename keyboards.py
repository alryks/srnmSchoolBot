from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, ReplyKeyboardMarkup
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
            InlineKeyboardButton(remove_markdownv2(data[i].name), callback_data=f'class_choose_{data[i].id}')
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


def group_choose(action, data, group=False):
    fields = create_button_text(action, 'group_choose')
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()

    if not group:
        rows.append([
            InlineKeyboardButton(fields['add'], callback_data='group_choose_add')
        ])

    for g in data:
        rows.append([
        InlineKeyboardButton(remove_markdownv2(g.name), callback_data=f'group_choose_{g.id}')
    ])

    if not group:
        rows.append([
            InlineKeyboardButton(back, callback_data='group_choose_back')
        ])
    else:
        rows.append([
            InlineKeyboardButton(cancel, callback_data='group_choose_cancel')
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


def group_timetable(action, lessons, date, group=False):
    fields = create_button_text(action, 'group_timetable')
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()

    rows.append([
        InlineKeyboardButton('◀', callback_data='group_timetable_month_left'),
        InlineKeyboardButton(f'{fields[months[date.month]]} {date.year}', callback_data='none_group_timetable_month'),
        InlineKeyboardButton('▶', callback_data='group_timetable_month_right'),
    ])

    rows.append([
        InlineKeyboardButton('◀', callback_data='group_timetable_day_left'),
        InlineKeyboardButton(f'{fields[weekdays[date.weekday()]]} {date.day}', callback_data='none_group_timetable_day'),
        InlineKeyboardButton('▶', callback_data='group_timetable_day_right'),
    ])

    for i, lesson in enumerate(lessons):
        rows.append([
            InlineKeyboardButton(f'{i + 1}. {remove_markdownv2(lesson.name)}', callback_data=f'group_timetable_lesson_{lesson.id}')
        ])

    if not group:
        rows.append([
            InlineKeyboardButton(fields['add'], callback_data='group_timetable_add')
        ])

    rows.append([
        InlineKeyboardButton(back, callback_data='group_timetable_back')
    ])

    return create_inline_keyboard(rows)


def lesson_name(action):
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()

    rows.append([
        InlineKeyboardButton(back, callback_data='lesson_name_back')
    ])

    return create_inline_keyboard(rows)


def lesson_create(action, data):
    fields = create_button_text(action, 'lesson')
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()

    rows.append([
        InlineKeyboardButton(back, callback_data='lesson_create_back')
    ])

    rows.append([
        InlineKeyboardButton(fields['name'], callback_data='lesson_create_name')
    ])

    rows.append([
        InlineKeyboardButton(fields['time'], callback_data='lesson_create_time')
    ])

    rows.append([
        InlineKeyboardButton(fields['homework'], callback_data='lesson_create_homework'),
        InlineKeyboardButton("❌", callback_data='lesson_create_homework_delete')
    ])

    rows.append([
        InlineKeyboardButton(fields['place'], callback_data='lesson_create_place'),
        InlineKeyboardButton("❌", callback_data='lesson_create_place_delete')
    ])

    rows.append([
        InlineKeyboardButton(fields['weekly'].format(weekly='✅' if data['lesson_weekly'] else '❌'), callback_data='lesson_create_weekly')
    ])

    rows.append([
        InlineKeyboardButton(fields['all'].format(all='✅' if data['lesson_all'] else '❌'), callback_data='lesson_create_all')
    ])

    rows.append([
        InlineKeyboardButton(fields['create'], callback_data='lesson_create_add')
    ])

    return create_inline_keyboard(rows)


def lesson(action, data, week):
    fields = create_button_text(action, 'lesson')
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()

    rows.append([
        InlineKeyboardButton(back, callback_data='lesson_back')
    ])

    if week is not None:
        rows.append([
            InlineKeyboardButton(fields['original'], callback_data='lesson_original')
        ])
        rows.append([
            InlineKeyboardButton(fields['restore'], callback_data='lesson_restore')
        ])

    rows.append([
        InlineKeyboardButton(fields['name'], callback_data='lesson_name')
    ])

    if week is None:
        rows.append([
            InlineKeyboardButton(fields['time'], callback_data='lesson_time')
        ])

    rows.append([
        InlineKeyboardButton(fields['homework'], callback_data='lesson_homework'),
        InlineKeyboardButton("❌", callback_data='lesson_homework_delete')
    ])

    rows.append([
        InlineKeyboardButton(fields['place'], callback_data='lesson_place'),
        InlineKeyboardButton("❌", callback_data='lesson_place_delete')
    ])

    if week is None:
        rows.append([
            InlineKeyboardButton(fields['weekly'].format(weekly='✅' if data['lesson_weekly'] else '❌'), callback_data='lesson_weekly')
        ])

        rows.append([
            InlineKeyboardButton(fields['delete'], callback_data='lesson_delete')
        ])

    rows.append([
        InlineKeyboardButton(fields['save'], callback_data='lesson_save')
    ])

    return create_inline_keyboard(rows)


def lesson_time(action, data, save=False):
    fields = create_button_text(action, 'lesson_time')
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()

    rows.append([
        InlineKeyboardButton(back, callback_data='lesson_time_back'),
    ])

    rows.append([
        InlineKeyboardButton(fields['start'], callback_data='none_lesson_time_start'),
    ])

    rows.append([
        InlineKeyboardButton('◀', callback_data='lesson_time_hrs_left'),
        InlineKeyboardButton(fields['hrs'].format(hrs=data['date'].hour), callback_data='none_lesson_time_hrs'),
        InlineKeyboardButton('▶', callback_data='lesson_time_hrs_right'),
    ])

    rows.append([
        InlineKeyboardButton('◀', callback_data='lesson_time_mins_left'),
        InlineKeyboardButton(fields['mins'].format(mins=data['date'].minute), callback_data='none_lesson_time_mins'),
        InlineKeyboardButton('▶', callback_data='lesson_time_mins_right'),
    ])

    rows.append([
        InlineKeyboardButton(fields['duration'], callback_data='none_lesson_time_duration'),
    ])

    rows.append([
        InlineKeyboardButton('◀', callback_data='lesson_time_duration_left'),
        InlineKeyboardButton(fields['length'].format(length=data['lesson_length']), callback_data='none_lesson_time_duration'),
        InlineKeyboardButton('▶', callback_data='lesson_time_duration_right'),
    ])

    if save:
        rows.append([
            InlineKeyboardButton(fields['save'], callback_data='lesson_time_save'),
        ])

    return create_inline_keyboard(rows)


def lesson_homework(action):
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()

    rows.append([
        InlineKeyboardButton(back, callback_data='lesson_homework_back')
    ])

    return create_inline_keyboard(rows)


def lesson_place(action):
    cancel = create_button_text(action, 'cancel')
    back = create_button_text(action, 'back')

    rows = list()

    rows.append([
        InlineKeyboardButton(back, callback_data='lesson_place_back')
    ])

    return create_inline_keyboard(rows)