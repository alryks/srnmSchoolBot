from aiogram.types import Message, CallbackQuery

from typing import Union

import settings
from langs import langs

import main

from models import *

from db.main import connect
from db.model import *

from sqlalchemy.sql.functions import func

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger

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


def create_text(action, key, **replace):
    if type(action) != str:
        lang = choose_language(action)
    else:
        lang = action
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


async def send_lesson_notification(lesson_id):
    s = connect()
    lesson = s.query(Lessons).filter(Lessons.id == lesson_id).one()
    group = s.query(Groups).filter(Groups.id == lesson.group_id).one()
    clas = s.query(Classes).filter(Classes.id == group.class_id).one()

    date = datetime.datetime.utcnow()
    if (lesson.start + datetime.timedelta(hours=clas.tz)).date() != date.date():
        week = (date.date() - lesson.start.date()).days // 7
        weekly_lesson = s.query(WeeklyLessons).filter(WeeklyLessons.lesson_id == lesson.id, WeeklyLessons.week == week)
        if weekly_lesson.count() > 0:
            weekly_lesson = weekly_lesson.one()
            lesson.name = weekly_lesson.name
            lesson.homework = weekly_lesson.homework
            lesson.place = weekly_lesson.place

    info = f"\n📚 {lesson.name}\n⏰ {lesson.start.hour}:{lesson.start.minute if lesson.start.minute > 9 else '0' + str(lesson.start.minute)} — {lesson.length}'"

    if lesson.place:
        info += f"\n📍 {lesson.place}"
    if lesson.homework:
        info += f"\n📝 {lesson.homework}"

    await main.bot.send_message(clas.chat_id, create_text(clas.lang, 'lesson_notification', clas=clas.name, group=group.name, start=clas.notify_before_lesson) + markdownv2(info))


async def send_daily_notification(class_id):
    s = connect()
    clas = s.query(Classes).filter(Classes.id == class_id).one()
    groups = sorted(s.query(Groups).filter(Groups.class_id == class_id).all(), key=lambda group: group.name)
    for group in groups:
        start = (datetime.datetime.utcnow() + datetime.timedelta(hours=clas.tz, days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        finish = start.replace(hour=23, minute=59)
        lessons = []
        lessons_daily = s.query(Lessons).filter(Lessons.group_id == group.id, Lessons.start < finish, Lessons.start >= start, Lessons.weekly == 0).all()
        lessons += lessons_daily
        lessons_weekly = s.query(Lessons).filter(Lessons.group_id == group.id, Lessons.start < start, Lessons.weekly == 1, func.dayofweek(Lessons.start) == (start.weekday() + 1) % 7 + 1).all()
        for lesson_weekly in lessons_weekly:
            existing_lesson = s.query(WeeklyLessons).filter(WeeklyLessons.lesson_id == lesson_weekly.id)
            if existing_lesson.count() > 0:
                existing_lesson = existing_lesson.one()
                lesson_weekly.name = existing_lesson.name
                lesson_weekly.homework = existing_lesson.homework
                lesson_weekly.place = existing_lesson.place
            lessons.append(lesson_weekly)

        if len(lessons) != 0:
            info = ''
            for i, lesson in enumerate(lessons):
                info += f"\n_*{i + 1}. {lesson.name}*_ — {lesson.start.hour}:{lesson.start.minute if lesson.start.minute > 9 else '0' + str(lesson.start.minute)}, {lesson.length}'\n"

            await main.bot.send_message(clas.chat_id, create_text(clas.lang, 'daily_notification', clas=clas.name, group=group.name) + markdownv2(info))
        else:
            await main.bot.send_message(clas.chat_id, create_text(clas.lang, 'no_lessons', clas=clas.name, group=group.name))


def schedule_notifications(schedule: AsyncIOScheduler):
    s = connect()
    lessons = s.query(Lessons)

    if lessons.count() > 0:
        lessons = lessons.all()
        for lesson in lessons:
            schedule = lesson_notify(schedule, lesson)

    classes = s.query(Classes)

    if classes.count() > 0:
        classes = classes.all()
        for clas in classes:
            schedule = class_notify(schedule, clas)
    return schedule


def lesson_notify(schedule, lesson):
    s = connect()
    group = s.query(Groups).filter(Groups.id == lesson.group_id).one()
    clas = s.query(Classes).filter(Classes.id == group.class_id).one()
    if clas.notify:
        lesson.start -= datetime.timedelta(minutes=clas.notify_before_lesson)
        if lesson.weekly:
            trigger = CronTrigger(day_of_week=lesson.start.weekday(), hour=lesson.start.hour, minute=lesson.start.minute, timezone=datetime.timezone(datetime.timedelta(hours=clas.tz)))
        else:
            trigger = DateTrigger(lesson.start, timezone=datetime.timezone(datetime.timedelta(hours=clas.tz)))
        if schedule.get_job(f'lesson_{lesson.id}'):
            schedule.modify_job(f'lesson_{lesson.id}', trigger=trigger)
        else:
            schedule.add_job(send_lesson_notification, trigger, args=[lesson.id], id=f'lesson_{lesson.id}')
    return schedule


def class_notify(schedule, clas):
    s = connect()
    groups = s.query(Groups).filter(Groups.class_id == clas.id)
    if clas.notify:
        trigger = CronTrigger(hour=clas.notify_day_before.hour, minute=clas.notify_day_before.minute, timezone=datetime.timezone(datetime.timedelta(hours=clas.tz)))
        if schedule.get_job(f'daily_{clas.id}'):
            schedule.modify_job(f'daily_{clas.id}', trigger=trigger)
        else:
            schedule.add_job(send_daily_notification, trigger, args=[clas.id], id=f'daily_{clas.id}')
    return schedule
