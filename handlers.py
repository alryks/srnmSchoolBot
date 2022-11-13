import sqlalchemy.exc

import main
from langs import langs
import keyboards
from models import *
from utils import *
import settings

from db.main import connect
from db.model import *

from aiogram.types import Message, CallbackQuery, Update
from aiogram.dispatcher.dispatcher import FSMContext
from aiogram.utils.exceptions import RetryAfter, MessageNotModified

import datetime

dp = main.dp
bot = main.bot


async def only_admin_message(message: Message, state: FSMContext):
    lang = choose_language(message)

    async with state.proxy() as data:
        admin_id = data['admin_id']
    # print(admin_id, message.from_user.id)
    if message.from_user.id in admin_id:
        await message.answer(markdownv2(langs[lang]['only_admin']))
        return False
    else:
        return True


async def only_admin_callback(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    async with state.proxy() as data:
        admin_id = data['admin_id']
    if callback.from_user.id in admin_id:
        await callback.answer(langs[lang]['only_admin'], show_alert=True)
        return False
    else:
        return True


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


@dp.message_handler(commands=['start'], state=all_states)
async def start(message: Message, state: FSMContext):
    lang = choose_language(message)

    await state.finish()
    if message.from_user.username:
        name = "@" + str(message.from_user.username)
    else:
        name = "*" + str(message.from_user.full_name) + "*"
    await message.answer(markdownv2(langs[lang]['start'].format(name=name)))


@dp.message_handler(commands=['help'], state=all_states)
async def help_cmd(message: Message, state: FSMContext):
    lang = choose_language(message)

    await state.finish()
    await message.answer(markdownv2(langs[lang]['help']))


@dp.message_handler(lambda x: x.chat.type == 'private')
async def not_group(message: Message):
    lang = choose_language(message)

    await message.answer(markdownv2(langs[lang]['not_group']))
    await message.delete()


@dp.message_handler(content_types=content_types,
                    state=[
                        ClassStates.new_class,
                        ClassStates.edit_class_name,
                        GroupStates.add_group,
                        GroupStates.edit_group_name,
                        LessonStates.lesson_name,
                        LessonStates.homework,
                        LessonStates.place
                    ])
async def not_text(message: Message, state: FSMContext):
    lang = choose_language(message)

    await message.answer(markdownv2(langs[lang]['not_text']))


@dp.message_handler(commands=['class'], state=all_states)
async def edit_class(message: Message, state: FSMContext, callback=None):
    lang = choose_language(message)

    s = connect()
    try:
        editclass = s.query(Class).filter(Class.chat_id == message.chat.id).one()
    except sqlalchemy.exc.NoResultFound:
        editclass = False

    if editclass:
        user_action = callback if callback else message
        async with state.proxy() as data:
            data['admin_id'] = editclass.admin_id.split()
        if str(user_action.from_user.id) in data['admin_id']:
            await ClassStates.edit_class.set()
            await message.answer(markdownv2(langs[lang]['edit_class'].format(name=editclass.name)), reply_markup=await keyboards.edit_class(message, state))
        else:
            await only_admin_message(message, state)
    else:
        async with state.proxy() as data:
            data['admin_id'] = [str(message.from_user.id)]
        await ClassStates.new_class.set()
        await message.answer(markdownv2(langs[lang]['new_class']), reply_markup=await keyboards.class_name(message, state))


@dp.message_handler(commands=['settings'], state=all_states)
async def settings_cmd(message: Message, state: FSMContext, callback=None):
    lang = choose_language(message)

    s = connect()
    try:
        editclass = s.query(Class).filter(Class.chat_id == message.chat.id).one()
    except sqlalchemy.exc.NoResultFound:
        editclass = False

    if editclass:
        user_action = callback if callback else message
        async with state.proxy() as data:
            data['admin_id'] = editclass.admin_id.split()
        if str(user_action.from_user.id) in data['admin_id']:
            await SettingsStates.settings.set()
            await message.answer(markdownv2(langs[lang]['settings'].format(name=editclass.name)), reply_markup=await keyboards.settings(message, state))
        else:
            await only_admin_message(message, state)
    else:
        await message.answer(markdownv2(langs[lang]['no_class']))


@dp.message_handler(commands=['groups'], state=all_states)
async def groups(message: Message, state: FSMContext, callback=None):
    lang = choose_language(message)

    s = connect()
    try:
        editclass = s.query(Class).filter(Class.chat_id == message.chat.id).one()
    except sqlalchemy.exc.NoResultFound:
        editclass = False

    if editclass:
        user_action = callback if callback else message
        async with state.proxy() as data:
            data['admin_id'] = editclass.admin_id.split()
        if str(user_action.from_user.id) in data['admin_id']:
            await GroupStates.groups.set()
            await message.answer(markdownv2(langs[lang]['groups'].format(name=editclass.name)), reply_markup=await keyboards.groups(message, state))
        else:
            await only_admin_message(message, state)
    else:
        await message.answer(markdownv2(langs[lang]['no_class']))


@dp.message_handler(content_types=['text'], state=ClassStates.new_class)
async def new_class(message: Message, state: FSMContext):
    lang = choose_language(message)

    if await only_admin_message(message, state):
        new_class_obj = Class(message.chat.id, str(message.from_user.id), message.text, 'en', True, 10, datetime.datetime(year=2005, month=9, day=9, hour=18), 3)
        s = connect()
        s.add(new_class_obj)
        s.commit()
        await message.answer(markdownv2(langs[lang]['new_class_created'].format(name=new_class_obj.name)))
        await edit_class(message, state)


@dp.message_handler(content_types=['text'], state=GroupStates.add_group)
async def add_group(message: Message, state: FSMContext):
    lang = choose_language(message)

    if await only_admin_message(message, state):
        s = connect()
        editclass = s.query(Class).filter(Class.chat_id == message.chat.id).one()
        new_group_obj = Group(class_id=editclass.id, name=message.text)
        s.add(new_group_obj)
        s.commit()
        await message.answer(markdownv2(langs[lang]['added_group'].format(class_name=editclass.name, group=new_group_obj.name)))
        await groups(message, state)


@dp.message_handler(content_types=['text'], state=GroupStates.edit_group_name)
async def edit_group_name(message: Message, state: FSMContext):
    lang = choose_language(message)

    if await only_admin_message(message, state):
        async with state.proxy() as data:
            group_id = data['group_id']
        s = connect()
        group = s.query(Group).filter(Group.id == group_id)
        group.update({Group.name: message.text})
        s.commit()
        await message.answer(markdownv2(langs[lang]['edit_group_name_changed']))
        await groups(message, state)


@dp.callback_query_handler(state=ClassStates.new_class)
async def callback_new_class(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    if await only_admin_callback(callback, state):
        if callback.data == 'cancel_edit_class_name':
            await state.finish()
            await callback.message.delete()


@dp.message_handler(content_types=['text'], state=ClassStates.edit_class_name)
async def edit_class_name(message: Message, state: FSMContext):
    lang = choose_language(message)

    if await only_admin_message(message, state):
        s = connect()
        s.query(Class).update({Class.name: message.text})
        s.commit()
        await message.answer(markdownv2(langs[lang]['edit_class_name_changed'].format(name=message.text)))
        await edit_class(message, state)


@dp.message_handler(content_types=['text'], state=SettingsStates.add_admin)
async def add_admin(message: Message, state: FSMContext):
    lang = choose_language(message)

    if await only_admin_message(message, state):
        if len(message.text) > 10:
            await message.answer(markdownv2(langs[lang]['incorrect_admin']))
        else:
            s = connect()
            editclass = s.query(Class).filter(Class.chat_id == message.chat.id)
            admins = editclass.one().admin_id.split()
            admins.append(message.text)
            new_admins = ' '.join(admins)
            editclass.update({Class.admin_id: new_admins})
            s.commit()
            await settings_cmd(message, state)


@dp.callback_query_handler(state=ClassStates.edit_class)
async def callback_edit_class(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    if await only_admin_callback(callback, state):
        if callback.data == 'cancel_edit_class':
            await state.finish()
        elif callback.data == 'delete_edit_class':
            await ClassStates.delete_class.set()
            s = connect()
            name = s.query(Class.name).filter(Class.chat_id == callback.message.chat.id).one()[0]
            await callback.message.answer(markdownv2(langs[lang]['delete_class'].format(name=name)), reply_markup=await keyboards.delete_class(callback.message, state))
        elif callback.data == 'name_edit_class':
            await ClassStates.edit_class_name.set()
            await callback.message.answer(markdownv2(langs[lang]['edit_class_name']), reply_markup=await keyboards.class_name(callback.message, state))
        await callback.message.delete()


@dp.callback_query_handler(state=ClassStates.edit_class_name)
async def callback_edit_class_name(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    if await only_admin_callback(callback, state):
        if callback.data == 'cancel_edit_class_name':
            await edit_class(callback.message, state, callback)
            await callback.message.delete()


@dp.callback_query_handler(state=ClassStates.delete_class)
async def callback_delete_class(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    if await only_admin_callback(callback, state):
        if callback.data == 'no_delete_class':
            await edit_class(callback.message, state, callback)
        elif callback.data == 'yes_delete_class':
            await ClassStates.sure_delete_class.set()
            await callback.message.answer(markdownv2(langs[lang]['sure_delete_class']), reply_markup=await keyboards.sure_delete_class(callback.message, state))
        await callback.message.delete()


@dp.callback_query_handler(state=ClassStates.sure_delete_class)
async def callback_sure_delete_class(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    if await only_admin_callback(callback, state):
        if callback.data == 'no_sure_delete_class':
            await edit_class(callback.message, state, callback)
        elif callback.data == 'yes_sure_delete_class':
            await state.finish()
            s = connect()
            editclass = s.query(Class).filter(Class.chat_id == callback.message.chat.id)
            groups = s.query(Group).filter(Group.class_id == editclass.one().id)
            for group in groups:
                s.query(Lesson).filter(Lesson.group_id == group.id).delete()
            groups.delete()
            editclass.delete()
            s.commit()
            await callback.message.answer(markdownv2(langs[lang]['sure_delete_class_deleted']))
        await callback.message.delete()


@dp.callback_query_handler(state=SettingsStates.settings)
async def callback_settings(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    try:
        if await only_admin_callback(callback, state):
            s = connect()
            editclass = s.query(Class).filter(Class.chat_id == callback.message.chat.id)

            if callback.data == 'admins':
                await SettingsStates.admins.set()
                await callback.message.answer(markdownv2(langs[lang]['admins'].format(name=editclass.one().name)), reply_markup=await keyboards.admins(callback, state))
                await callback.message.delete()
            elif callback.data == 'lang':
                if len(settings.LANGS) > 1:
                    new_lang = settings.LANGS[(settings.LANGS.index(editclass[0].lang) + 1) % len(settings.LANGS)]
                    editclass.update({Class.lang: new_lang})
                    s.commit()
                    await callback.message.answer(markdownv2(langs[lang]['settings'].format(name=editclass[0].name)), reply_markup=await keyboards.settings(callback.message, state))
                    await callback.message.delete()
                else:
                    await alert(callback)
            elif callback.data == 'notify':
                new_notify = (editclass[0].notify + 1) % 2
                editclass.update({Class.notify: new_notify})
                s.commit()
                try:
                    await callback.message.edit_reply_markup(await keyboards.settings(callback.message, state))
                except MessageNotModified:
                    pass
            elif callback.data == 'timezone':
                await SettingsStates.timezone.set()
                await callback.message.answer(markdownv2(langs[lang]['timezone'].format(name=editclass[0].name)), reply_markup=await keyboards.timezone(callback.message, state))
                await callback.message.delete()
            elif callback.data == 'time_settings':
                await SettingsStates.time.set()
                async with state.proxy() as data:
                    data['before'] = editclass[0].lesson
                    data['hrs'] = editclass[0].tomorrow.hour
                    data['mins'] = editclass[0].tomorrow.minute
                await callback.message.answer(markdownv2(langs[lang]['time_settings'].format(name=editclass[0].name)), reply_markup=await keyboards.time_settings(callback.message, state))
                await callback.message.delete()
            elif callback.data == 'cancel_settings':
                await state.finish()
                await callback.message.delete()
    except RetryAfter as e:
        left, right = str(e).split('Flood control exceeded. Retry in ')
        seconds, right = right.split(' seconds')
        seconds = int(seconds)
        await too_fast(callback, seconds, show_alert=True)


@dp.callback_query_handler(state=SettingsStates.timezone)
async def callback_timezone(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    if await only_admin_callback(callback, state):
        if is_int(callback.data):
            s = connect()
            s.query(Class).filter(Class.chat_id == callback.message.chat.id).update({Class.timezone: int(callback.data)})
            s.commit()
            await settings_cmd(callback.message, state, callback=callback)
            await callback.message.delete()
        elif callback.data == 'back_timezone':
            await settings_cmd(callback.message, state, callback=callback)
            await callback.message.delete()


@dp.callback_query_handler(state=SettingsStates.time)
async def callback_time_settings(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    s = connect()
    editclass = s.query(Class).filter(Class.chat_id == callback.message.chat.id)
    async with state.proxy() as data:
        new_before = data['before']
        new_hrs = data['hrs']
        new_mins = data['mins']

    if await only_admin_callback(callback, state):
        if callback.data.startswith('none'):
            await alert(callback)
        elif callback.data == 'save_time_settings':
            editclass.update({Class.lesson: new_before, Class.tomorrow: datetime.datetime(year=2005, month=9, day=9, hour=new_hrs, minute=new_mins)})
            s.commit()
            await settings_cmd(callback.message, state, callback=callback)
            await callback.message.delete()
            return
        elif callback.data == 'back_time_settings':
            await settings_cmd(callback.message, state, callback=callback)
            await callback.message.delete()
            return
        elif callback.data == 'left_before':
            new_before = new_before - 5 if new_before > 0 else new_before
        elif callback.data == 'right_before':
            new_before = new_before + 5
        elif callback.data == 'left_hrs':
            new_hrs = (new_hrs - 1) % 24
        elif callback.data == 'right_hrs':
            new_hrs = (new_hrs + 1) % 24
        elif callback.data == 'left_mins':
            new_mins = (new_mins - 5) % 60
        elif callback.data == 'right_mins':
            new_mins = (new_mins + 5) % 60

        async with state.proxy() as data:
            data['before'] = new_before
            data['hrs'] = new_hrs
            data['mins'] = new_mins

        try:
            await callback.message.edit_reply_markup(await keyboards.time_settings(callback.message, state))
        except MessageNotModified:
            pass


@dp.callback_query_handler(state=SettingsStates.admins)
async def callback_admins(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    s = connect()
    editclass = s.query(Class).filter(Class.chat_id == callback.message.chat.id)

    if await only_admin_callback(callback, state):
        if callback.data.startswith('none_'):
            await alert(callback)
        elif callback.data.startswith('delete_admin_'):
            admins = editclass.one().admin_id.split()
            admins.remove(callback.data.split('delete_admin_')[1])
            new_admins = ' '.join(admins)
            editclass.update({Class.admin_id: new_admins})
            s.commit()

            callback.data = 'admins'
            await callback_settings(callback, state)
        elif callback.data == 'add_admin':
            await SettingsStates.add_admin.set()
            await callback.message.answer(markdownv2(langs[lang]['add_admin']), reply_markup=await keyboards.add_admin(callback.message, state))
            await callback.message.delete()
        elif callback.data == 'back_admins':
            await settings_cmd(callback.message, state, callback)
            await callback.message.delete()


@dp.callback_query_handler(state=SettingsStates.add_admin)
async def callback_add_admin(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    if await only_admin_callback(callback, state):
        if callback.data == 'back_add_admin':
            callback.data = 'admins'
            await callback_settings(callback, state)


@dp.callback_query_handler(state=GroupStates.groups)
async def callback_groups(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    if await only_admin_callback(callback, state):
        if callback.data.startswith('group_'):
            await GroupStates.group.set()
            s = connect()
            editclass = s.query(Class).filter(Class.chat_id == callback.message.chat.id).one()
            group = s.query(Group).filter(Group.id == int(callback.data.split('group_')[1])).one()
            async with state.proxy() as data:
                data['group_id'] = group.id
            await callback.message.answer(markdownv2(langs[lang]['group'].format(class_name=editclass.name, group=group.name)), reply_markup=await keyboards.group(callback.message, state))
            await callback.message.delete()
        elif callback.data == 'cancel_groups':
            await state.finish()
            await callback.message.delete()
        elif callback.data == 'add_groups':
            await GroupStates.add_group.set()
            await callback.message.answer(markdownv2(langs[lang]['add_group']), reply_markup=await keyboards.add_group(callback.message, state))
            await callback.message.delete()


@dp.callback_query_handler(state=GroupStates.add_group)
async def callback_add_group(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    if await only_admin_callback(callback, state):
        if callback.data == 'back_add_group':
            await groups(callback.message, state, callback)
            await callback.message.delete()


@dp.callback_query_handler(state=GroupStates.group)
async def callback_group(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    async with state.proxy() as data:
        group_id = data['group_id']

    s = connect()
    group = s.query(Group).filter(Group.id == group_id).one()
    editclass = s.query(Class).filter(Class.id == Group.class_id).one()
    if await only_admin_callback(callback, state):
        if callback.data == 'name_group':
            await GroupStates.edit_group_name.set()
            await callback.message.answer(markdownv2(langs[lang]['edit_group_name'].format(class_name=editclass.name, group=group.name)), reply_markup=await keyboards.edit_group_name(callback.message, state))
            await callback.message.delete()
        elif callback.data == 'delete_group':
            await GroupStates.delete_group.set()
            await callback.message.answer(markdownv2(langs[lang]['delete_group'].format(class_name=editclass.name, group=group.name)), reply_markup=await keyboards.delete_group(callback.message, state))
            await callback.message.delete()
        elif callback.data == 'back_group':
            await group(callback.message, state, callback)
            await callback.message.delete()


@dp.callback_query_handler(state=GroupStates.edit_group_name)
async def callback_edit_group_name(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    async with state.proxy() as data:
        group_id = data['group_id']

    if await only_admin_callback(callback, state):
        if callback.data == 'cancel_edit_group_name':
            callback.data = f'group_{group_id}'
            await callback_groups(callback, state)


@dp.callback_query_handler(state=GroupStates.delete_group)
async def callback_delete_group(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    async with state.proxy() as data:
        group_id = data['group_id']

    if await only_admin_callback(callback, state):
        if callback.data == 'yes_delete_group':
            s = connect()
            group = s.query(Group).filter(Group.id == group_id)
            s.query(Lesson).filter(Lesson.group_id == group.one().id).delete()
            group.delete()
            s.commit()
            await callback.message.answer(markdownv2(langs[lang]['deleted_group']))
            await groups(callback.message, state, callback)
            await callback.message.delete()
        elif callback.data == 'no_delete_group':
            callback.data = f'group_{group_id}'
            await callback_groups(callback, state)
