import sqlalchemy.exc

import main
from langs import langs
import keyboards
from models import *
from utils import *
import settings

from typing import Union

from db.main import connect
from db.model import *

from aiogram.types import Message, CallbackQuery, Update
from aiogram.dispatcher.dispatcher import FSMContext
from aiogram.utils.exceptions import RetryAfter, MessageNotModified

import datetime

dp = main.dp
bot = main.bot


async def max_lim(action, symbols):
    await text_message(action, create_text(action, 'max_lim', symbols=symbols))


@dp.errors_handler()
async def error(update: Update, err):
    msg = update.callback_query.message if update.callback_query else update.message
    if msg.chat.type == 'private':
        name = msg.chat.username if msg.chat.username else msg.chat.first_name
    else:
        name = msg.chat.title
    text = f"<b><i>Error occurred!</i></b> It was in <i>{msg.chat.type}</i> chat. Name of chat: <i>{name}</i>. Message text:\n\n<i>{msg.text}</i> \n\n{type(err).__name__}: {err}"

    for ADMIN in settings.ADMINS:
        await bot.send_message(ADMIN, text, parse_mode='HTML')


"""
BASE COMMANDS
"""


@dp.message_handler(lambda message: message.chat.type == 'private', commands='start', state=all_states)
async def start(action: Union[Message, CallbackQuery], state: FSMContext):
    s = connect()
    user = s.query(Users).filter(Users.telegram_id == action.from_user.id)
    if user.count() == 0:
        new_user = Users(telegram_id=str(action.from_user.id), lang=choose_language(action))
        s.add(new_user)
        s.commit()
    await state.finish()
    await action.answer(create_text(action, 'start', name=get_user_name(action)))


@dp.message_handler(lambda message: message.chat.type == 'group', commands='start', state=all_states)
async def start(action: Union[Message, CallbackQuery], state: FSMContext):
    await state.finish()
    await action.answer(create_text(action, 'start', name=get_user_name(action)))


@dp.message_handler(commands='help', state=all_states)
async def help_cmd(action: Union[Message, CallbackQuery], state: FSMContext):
    await state.finish()
    await action.answer(create_text(action, 'help'))


"""
MESSAGE HANDLERS
"""


@dp.message_handler(lambda message: message.chat.type == 'group', commands='verify', state=all_states)
async def class_verify(action: Union[Message, CallbackQuery], state: FSMContext):
    await state.finish()

    user_admin = False
    for admin in await action.chat.get_administrators():
        if admin['user']['id'] == action.from_user.id and (admin['status'] == 'creator' or admin['status'] == 'administrator'):
            user_admin = True
            break
    if user_admin:
        s = connect()
        if s.query(Classes).filter(Classes.chat_id == action.chat.id).count() == 0:
            if s.query(Users).filter(Users.telegram_id == action.from_user.id).count() > 0:
                bad_classes = s.query(Classes).filter(Classes.chat_id == -1).all()
                for clas in bad_classes:
                    user_class = s.query(UserClasses).filter(UserClasses.class_id == clas.id).filter(UserClasses.user_id == s.query(Users).filter(Users.telegram_id == action.from_user.id).one().id)
                    if user_class.count() > 0:
                        s.query(Classes).filter(Classes.id == clas.id).update({'chat_id': action.chat.id})
                        s.commit()
                        await bot.send_message(action.from_user.id, create_text(action, 'class_added'))
        else:
            await text_message(action, create_text(action, 'class_exists'))
    else:
        await text_message(action, create_text(action, 'not_admin'))


@dp.message_handler(lambda message: message.chat.type == 'private', commands='settings', state=all_states)
async def settings_cmd(action: Union[Message, CallbackQuery], state: FSMContext):
    await state.finish()

    s = connect()
    user = s.query(Users).filter(Users.telegram_id == action.from_user.id).one()

    await PrivateStates.settings.set()
    await text_message(action, create_text(action, 'settings'), keyboard=keyboards.settings(action, {'lang': user.lang}))


@dp.message_handler(lambda message: message.chat.type == 'private', commands='class', state=all_states)
async def class_cmd(action: Union[Message, CallbackQuery], state: FSMContext):
    await state.finish()

    s = connect()
    bad_classes = s.query(Classes).filter(Classes.chat_id == -1).all()
    for clas in bad_classes:
        user_class = s.query(UserClasses).filter(UserClasses.class_id == clas.id and UserClasses.user_id == s.query(Users).filter(Users.telegram_id == action.from_user.id).one().id)
        if user_class.count() > 0:
            user_class.delete()
            s.query(Classes).filter(Classes.id == clas.id).delete()
            s.commit()
    user_classes = s.query(UserClasses).filter(UserClasses.user_id == s.query(Users).filter(Users.telegram_id == action.from_user.id).one().id)
    if user_classes.count() > 0:
        await PrivateStates.class_choose.set()
        classes = list()
        for user_class in user_classes.all():
            clas = s.query(Classes).filter(Classes.id == user_class.class_id).one()
            classes.append(clas)
        await text_message(action, create_text(action, 'class_choose'), keyboard=keyboards.class_choose(action, classes))
    else:
        await class_create(action, state)


async def class_create(action: Union[Message, CallbackQuery], state: FSMContext):
    await PrivateStates.class_create_name.set()
    await text_message(action, create_text(action, 'class_create_name'), keyboard=keyboards.class_create_name(action))


@dp.message_handler(lambda message: message.chat.type == 'private', state=PrivateStates.class_create_name)
async def class_create_name(action: Union[Message, CallbackQuery], state: FSMContext):
    symbols = 64
    if len(action.text) > symbols:
        await max_lim(action, symbols)
    else:
        s = connect()
        new_class = Classes(action.text)
        s.add(new_class)
        s.commit()
        new_user_class = UserClasses(s.query(Users).filter(Users.telegram_id == action.from_user.id).one().id, s.query(Classes).filter(Classes.name == action.text).all()[-1].id)
        s.add(new_user_class)
        s.commit()

        await PrivateStates.class_verify.set()
        await text_message(action, create_text(action, 'class_verify', name=action.text))


@dp.message_handler(lambda message: message.chat.type == 'private', state=PrivateStates.class_change_name)
async def class_change_name(action: Union[Message, CallbackQuery], state: FSMContext):
    symbols = 64
    if len(action.text) > symbols:
        await max_lim(action, symbols)
    else:
        async with state.proxy() as data:
            class_id = data['class_id']
        s = connect()
        s.query(Classes).filter(Classes.id == class_id).update({'name': action.text})
        s.commit()

        await PrivateStates.class_now.set()
        name = s.query(Classes).filter(Classes.id == class_id).one().name
        await text_message(action, create_text(action, 'class_now', name=name), keyboard=keyboards.class_now(action))


@dp.message_handler(lambda message: message.chat.type == 'private', state=PrivateStates.group_create_name)
async def group_create_name(action: Union[Message, CallbackQuery], state: FSMContext):
    symbols = 64
    if len(action.text) > symbols:
        await max_lim(action, symbols)
    else:
        async with state.proxy() as data:
            class_id = data['class_id']
        s = connect()
        new_group = Groups(class_id, action.text)
        s.add(new_group)
        s.commit()

        clas = s.query(Classes).filter(Classes.id == class_id).one()
        groups = s.query(Groups).filter(Groups.class_id == class_id).all()

        await PrivateStates.group_choose.set()
        await text_message(action, create_text(action, 'group_choose', name=clas.name), keyboard=keyboards.group_choose(action, groups))


@dp.message_handler(lambda message: message.chat.type == 'private', state=PrivateStates.class_add_admin)
async def class_add_admin(action: Union[Message, CallbackQuery], state: FSMContext):
    symbols = 10
    if len(action.text) > symbols:
        await max_lim(action, symbols)
    else:
        async with state.proxy() as data:
            class_id = data['class_id']
        s = connect()
        user = s.query(Users).filter(Users.telegram_id == action.text)
        if user.count() == 0:
            user = Users(action.text)
            s.add(user)
            s.commit()
        user = s.query(Users).filter(Users.telegram_id == action.text).one()
        user_classes = s.query(UserClasses).filter(UserClasses.user_id == user.id and UserClasses.class_id == class_id)
        if user_classes.count() == 0:
            user_classes = UserClasses(user.id, class_id)
            s.add(user_classes)
            s.commit()

        admin_ids = s.query(UserClasses).filter(UserClasses.class_id == class_id).all()
        admins = [s.query(Users).filter(Users.id == admin_id.user_id).one().telegram_id for admin_id in admin_ids]
        await PrivateStates.class_admins.set()
        await text_message(action, create_text(action, 'class_admins'), keyboard=keyboards.class_admins(action, admins))


@dp.message_handler(lambda message: message.chat.type == 'private', state=PrivateStates.group_change_name)
async def group_change_name(action: Union[Message, CallbackQuery], state: FSMContext):
    symbols = 64
    if len(action.text) > symbols:
        await max_lim(action, symbols)
    else:
        async with state.proxy() as data:
            class_id = data['class_id']
            group_id = data['group_id']
        s = connect()
        s.query(Groups).filter(Groups.id == group_id).update({'name': action.text})
        s.commit()

        group = s.query(Groups).filter(Groups.id == group_id).one()
        clas = s.query(Classes).filter(Classes.id == class_id).one()
        await PrivateStates.group_now.set()
        await text_message(action, create_text(action, 'group_now', clas=clas.name, group=group.name), keyboard=keyboards.group_now(action))



"""
CALLBACK HANDLERS
"""


@dp.callback_query_handler(state=PrivateStates.settings)
async def callback_settings(callback: CallbackQuery, state: FSMContext):
    s = connect()
    user = s.query(Users).filter(Users.telegram_id == callback.from_user.id).one()

    if callback.data == 'settings_lang':
        new_lang = settings.LANGS[(settings.LANGS.index(user.lang) + 1) % len(settings.LANGS)]
        s.query(Users).filter(Users.telegram_id == callback.from_user.id).update({'lang': new_lang})
        s.commit()
        await text_message(callback, keyboard=keyboards.settings(callback, {'lang': new_lang}))
    elif callback.data == 'settings_cancel':
        await state.finish()
        await callback.message.delete()


@dp.callback_query_handler(state=PrivateStates.class_create_name)
async def callback_class_create_name(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'class_create_name_cancel':
        await state.finish()
        await callback.message.delete()


@dp.callback_query_handler(state=PrivateStates.class_choose)
async def callback_class_choose(callback: CallbackQuery, state: FSMContext):
    if callback.data[-1].isdigit() and callback.data.startswith('class_choose'):
        await PrivateStates.class_now.set()
        class_id = int(callback.data[13:])
        async with state.proxy() as data:
            data['class_id'] = class_id
        s = connect()
        name = s.query(Classes).filter(Classes.id == class_id).one().name
        await text_message(callback, create_text(callback, 'class_now', name=name), keyboard=keyboards.class_now(callback))
    elif callback.data == 'class_choose_add':
        await class_create(callback, state)
    elif callback.data == 'class_choose_cancel':
        await state.finish()
        await callback.message.delete()


@dp.callback_query_handler(state=PrivateStates.class_now)
async def callback_class_now(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        class_id = data['class_id']

    s = connect()
    clas = s.query(Classes).filter(Classes.id == class_id).one()
    if callback.data == 'class_now_name':
        await PrivateStates.class_change_name.set()
        await text_message(callback, create_text(callback, 'class_change_name', name=clas.name), keyboard=keyboards.class_change_name(callback))
    elif callback.data == 'class_now_back':
        await class_cmd(callback, state)
    elif callback.data == 'class_now_settings':
        await PrivateStates.class_settings.set()
        await text_message(callback, create_text(callback, 'class_settings', name=clas.name), keyboard=keyboards.class_settings(callback, clas))
    elif callback.data == 'class_now_groups':
        groups = s.query(Groups).filter(Groups.class_id == class_id)
        if groups.count() > 0:
            await PrivateStates.group_choose.set()
            groups = s.query(Groups).filter(Groups.class_id == class_id).all()
            await text_message(callback, create_text(callback, 'group_choose', name=clas.name), keyboard=keyboards.group_choose(callback, groups))
        else:
            await PrivateStates.group_create_name.set()
            await text_message(callback, create_text(callback, 'group_create_name', name=clas.name), keyboard=keyboards.group_create_name(callback))
    elif callback.data == 'class_now_delete':
        await PrivateStates.class_delete.set()
        await text_message(callback, create_text(callback, 'class_delete', name=clas.name), keyboard=keyboards.class_delete(callback))


@dp.callback_query_handler(state=PrivateStates.class_change_name)
async def callback_class_change_name(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        class_id = data['class_id']

    s = connect()
    clas = s.query(Classes).filter(Classes.id == class_id).one()
    if callback.data == 'class_change_name_back':
        await PrivateStates.class_now.set()
        await text_message(callback, create_text(callback, 'class_now', name=clas.name), keyboard=keyboards.class_now(callback))


@dp.callback_query_handler(state=PrivateStates.class_delete)
async def callback_class_delete(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        class_id = data['class_id']

    s = connect()
    clas = s.query(Classes).filter(Classes.id == class_id).one()
    if callback.data == 'class_delete_no':
        await PrivateStates.class_now.set()
        await text_message(callback, create_text(callback, 'class_now', name=clas.name), keyboard=keyboards.class_now(callback))
    elif callback.data == 'class_delete_yes':
        groups = s.query(Groups).filter(Groups.class_id == class_id)
        if groups.count() > 0:
            for group in groups.all():
                s.query(Lessons).filter(Lessons.group_id == group.id).delete()
        groups.delete()
        s.query(UserClasses).filter(UserClasses.class_id == clas.id).delete()
        s.query(Classes).filter(Classes.id == class_id).delete()
        s.commit()

        await state.finish()

        await text_message(callback, create_text(callback, 'class_deleted', name=clas.name))


@dp.callback_query_handler(state=PrivateStates.class_settings)
async def callback_class_settings(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        class_id = data['class_id']

    s = connect()
    clas = s.query(Classes).filter(Classes.id == class_id).one()
    if callback.data == 'class_settings_admins':
        admin_ids = s.query(UserClasses).filter(UserClasses.class_id == class_id).all()
        admins = [s.query(Users).filter(Users.id == admin_id.user_id).one().telegram_id for admin_id in admin_ids]
        await PrivateStates.class_admins.set()
        await text_message(callback, create_text(callback, 'class_admins', name=clas.name), keyboard=keyboards.class_admins(callback, admins))
    elif callback.data == 'class_settings_lang':
        new_lang = settings.LANGS[(settings.LANGS.index(clas.lang) + 1) % len(settings.LANGS)]
        s.query(Classes).filter(Classes.id == class_id).update({'lang': new_lang})
        s.commit()
        clas.lang = new_lang
        await text_message(callback, keyboard=keyboards.class_settings(callback, clas))
    elif callback.data == 'class_settings_notify':
        clas.notify = (clas.notify + 1) % 2
        s.query(Classes).filter(Classes.id == class_id).update({'notify': clas.notify})
        s.commit()
        await text_message(callback, keyboard=keyboards.class_settings(callback, clas))
    elif callback.data == 'class_settings_tz':
        await PrivateStates.class_timezone.set()
        await text_message(callback, create_text(callback, 'class_settings_tz'), keyboard=keyboards.class_settings_tz(callback, clas))
    elif callback.data == 'class_settings_time':
        await PrivateStates.class_notifications.set()
        async with state.proxy() as data:
            data['hrs'] = clas.notify_day_before.hour
            data['mins'] = clas.notify_day_before.minute
            data['gap'] = clas.notify_before_lesson
        await text_message(callback, create_text(callback, 'class_settings_time', name=clas.name), keyboard=keyboards.class_settings_time(callback, data))
    elif callback.data == 'class_settings_back':
        await PrivateStates.class_now.set()
        await text_message(callback, create_text(callback, 'class_now', name=clas.name), keyboard=keyboards.class_now(callback))


@dp.callback_query_handler(state=PrivateStates.class_admins)
async def callback_class_admins(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        class_id = data['class_id']

    s = connect()
    clas = s.query(Classes).filter(Classes.id == class_id).one()
    if callback.data == 'class_admins_back':
        await PrivateStates.class_now.set()
        await text_message(callback, create_text(callback, 'class_now', name=clas.name), keyboard=keyboards.class_now(callback))
    elif callback.data == 'class_add_admin':
        await PrivateStates.class_add_admin.set()
        await text_message(callback, create_text(callback, 'class_add_admin', name=clas.name), keyboard=keyboards.class_add_admin(callback))
    elif callback.data.startswith('none_class_admin'):
        await alert(callback)
    elif callback.data.startswith('class_admin'):
        admin_ids = s.query(UserClasses).filter(UserClasses.class_id == class_id).all()
        admins = [s.query(Users).filter(Users.id == admin_id.user_id).one().telegram_id for admin_id in admin_ids]
        id = callback.data.split('class_admin_')[1]
        if id in admins:
            user_id = s.query(Users).filter(Users.telegram_id == id).one().id
            s.query(UserClasses).filter(UserClasses.user_id == user_id and UserClasses.class_id == class_id).delete()
            s.commit()
            admin_ids = s.query(UserClasses).filter(UserClasses.class_id == class_id).all()
            admins = [s.query(Users).filter(Users.id == admin_id.user_id).one().telegram_id for admin_id in admin_ids]
        await text_message(callback, create_text(callback, 'class_admins', name=clas.name), keyboard=keyboards.class_admins(callback, admins))


@dp.callback_query_handler(state=PrivateStates.class_add_admin)
async def callback_class_add_admin(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        class_id = data['class_id']

    s = connect()
    clas = s.query(Classes).filter(Classes.id == class_id).one()
    if callback.data == 'class_add_admin_back':
        admin_ids = s.query(UserClasses).filter(UserClasses.class_id == class_id).all()
        admins = [s.query(Users).filter(Users.id == admin_id.user_id).one().telegram_id for admin_id in admin_ids]
        await PrivateStates.class_admins.set()
        await text_message(callback, create_text(callback, 'class_admins', name=clas.name), keyboard=keyboards.class_admins(callback, admins))


@dp.callback_query_handler(state=PrivateStates.class_timezone)
async def callback_class_settings_tz(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        class_id = data['class_id']

    s = connect()
    clas = s.query(Classes).filter(Classes.id == class_id).one()
    if callback.data == 'class_settings_tz_back':
        await PrivateStates.class_settings.set()
        await text_message(callback, keyboard=keyboards.class_settings(callback, clas))
    elif callback.data.startswith('class_settings_tz_'):
        clas.tz = int(callback.data.split('class_settings_tz_')[-1])
        s.query(Classes).filter(Classes.id == class_id).update({'tz': clas.tz})
        s.commit()
        await PrivateStates.class_settings.set()
        await text_message(callback, keyboard=keyboards.class_settings(callback, clas))


@dp.callback_query_handler(state=PrivateStates.class_notifications)
async def callback_class_settings_time(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        class_id = data['class_id']

    s = connect()
    clas = s.query(Classes).filter(Classes.id == class_id).one()
    if callback.data == 'class_settings_time_back':
        await PrivateStates.class_settings.set()
        await text_message(callback, keyboard=keyboards.class_settings(callback, clas))
    elif callback.data.startswith('none_class_settings_time'):
        await alert(callback)
    elif callback.data == 'class_settings_time_save':
        async with state.proxy() as data:
            s.query(Classes).filter(Classes.id == class_id).update({
                'notify_day_before': datetime.datetime(year=2005, month=9, day=9, hour=data['hrs'], minute=data['mins']),
                'notify_before_lesson': data['gap']})
            s.commit()
            await PrivateStates.class_settings.set()
            clas = s.query(Classes).filter(Classes.id == class_id).one()
            await text_message(callback, keyboard=keyboards.class_settings(callback, clas))
    elif callback.data.startswith('class_settings_time'):
        async with state.proxy() as data:
            if callback.data == 'class_settings_time_hrs_left':
                data['hrs'] = (data['hrs'] - 1) % 24
            elif callback.data == 'class_settings_time_hrs_right':
                data['hrs'] = (data['hrs'] + 1) % 24
            elif callback.data == 'class_settings_time_mins_left':
                data['mins'] = (data['mins'] - 10) % 60
            elif callback.data == 'class_settings_time_mins_right':
                data['mins'] = (data['mins'] + 10) % 60
            elif callback.data == 'class_settings_time_gap_left':
                data['gap'] = (data['gap'] - 5) % 60
            elif callback.data == 'class_settings_time_gap_right':
                data['gap'] = (data['gap'] + 5) % 60

            await text_message(callback, keyboard=keyboards.class_settings_time(callback, data))


@dp.callback_query_handler(state=PrivateStates.group_create_name)
async def callback_group_create_name(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        class_id = data['class_id']

    s = connect()
    clas = s.query(Classes).filter(Classes.id == class_id).one()
    if callback.data == 'group_create_name_back':
        await PrivateStates.class_now.set()
        await text_message(callback, create_text(callback, 'class_now', name=clas.name), keyboard=keyboards.class_now(callback))


@dp.callback_query_handler(state=PrivateStates.group_choose)
async def callback_group_choose(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        class_id = data['class_id']

    s = connect()
    clas = s.query(Classes).filter(Classes.id == class_id).one()
    if callback.data == 'group_choose_back':
        await PrivateStates.class_now.set()
        await text_message(callback, create_text(callback, 'class_now', name=clas.name), keyboard=keyboards.class_now(callback))
    elif callback.data == 'group_choose_add':
        await PrivateStates.group_create_name.set()
        await text_message(callback, create_text(callback, 'group_create_name', name=clas.name), keyboard=keyboards.group_create_name(callback))
    elif callback.data.startswith('group_choose'):
        group_id = int(callback.data[13:])
        async with state.proxy() as data:
            data['group_id'] = group_id
        group = s.query(Groups).filter(Groups.id == group_id).one()
        await PrivateStates.group_now.set()
        await text_message(callback, create_text(callback, 'group_now', clas=clas.name, group=group.name), keyboard=keyboards.group_now(callback))


@dp.callback_query_handler(state=PrivateStates.group_now)
async def callback_group_now(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        class_id = data['class_id']
        group_id = data['group_id']

    s = connect()
    clas = s.query(Classes).filter(Classes.id == class_id).one()
    group = s.query(Groups).filter(Groups.id == group_id).one()
    groups = s.query(Groups).filter(Groups.class_id == class_id).all()
    if callback.data == 'group_now_back':
        await PrivateStates.group_choose.set()
        await text_message(callback, create_text(callback, 'group_choose', name=clas.name), keyboard=keyboards.group_choose(callback, groups))
    elif callback.data == 'group_now_name':
        await PrivateStates.group_change_name.set()
        await text_message(callback, create_text(callback, 'group_change_name', clas=clas.name, group=group.name), keyboard=keyboards.group_change_name(callback))
    elif callback.data == 'group_now_timetable':
        pass
    elif callback.data == 'group_now_delete':
        await PrivateStates.group_delete.set()
        await text_message(callback, create_text(callback, 'group_delete', clas=clas.name, group=group.name), keyboard=keyboards.group_delete(callback))


@dp.callback_query_handler(state=PrivateStates.group_delete)
async def callback_group_delete(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        class_id = data['class_id']
        group_id = data['group_id']

    s = connect()
    clas = s.query(Classes).filter(Classes.id == class_id).one()
    group = s.query(Groups).filter(Groups.id == group_id).one()
    groups = s.query(Groups).filter(Groups.class_id == class_id).all()
    if callback.data == 'group_delete_yes':
        await PrivateStates.class_now.set()
        s.query(Lessons).filter(Lessons.group_id == group_id).delete()
        s.query(Groups).filter(Groups.id == group_id).delete()
        s.commit()
        await text_message(callback, create_text(callback, 'class_now', name=clas.name), keyboard=keyboards.class_now(callback))
    elif callback.data == 'group_delete_no':
        await PrivateStates.group_now.set()
        await text_message(callback, create_text(callback, 'group_now', clas=clas.name, group=group.name), keyboard=keyboards.group_now(callback))


@dp.callback_query_handler(state=PrivateStates.group_change_name)
async def callback_group_change_name(callback: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        class_id = data['class_id']
        group_id = data['group_id']

    s = connect()
    clas = s.query(Classes).filter(Classes.id == class_id).one()
    group = s.query(Groups).filter(Groups.id == group_id).one()
    groups = s.query(Groups).filter(Groups.class_id == class_id).all()
    if callback.data == 'group_change_name_back':
        await PrivateStates.group_now.set()
        await text_message(callback, create_text(callback, 'group_now', clas=clas.name, group=group.name), keyboard=keyboards.group_now(callback))

