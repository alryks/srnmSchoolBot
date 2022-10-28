import sqlalchemy.exc

import main
from langs import langs
import keyboards
from models import *
from utils import *

from db.main import connect
from db.model import *

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.dispatcher import FSMContext

import datetime

dp = main.dp
bot = main.bot


@dp.message_handler(commands=['start'],
                    state=[
                        *ClassStates.all_states,
                        *GroupStates.all_states,
                        *LessonStates.all_states,
                        None
                    ])
async def start(message: Message, state: FSMContext):
    lang = choose_language(message)

    await state.finish()
    if message.from_user.username:
        name = "@" + str(message.from_user.username)
    else:
        name = "*" + str(message.from_user.full_name) + "*"
    await message.answer(markdownv2(langs[lang]['start'].format(name=name)))


@dp.message_handler(commands=['help'],
                    state=[
                        *ClassStates.all_states,
                        *GroupStates.all_states,
                        *LessonStates.all_states,
                        None
                    ])
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


async def only_admin_message(message: Message, state: FSMContext):
    lang = choose_language(message)

    async with state.proxy() as data:
        admin_id = data['admin_id']
    if message.from_user.id != admin_id:
        await message.answer(markdownv2(langs[lang]['only_admin']))
        await message.delete()
        return False
    return True


async def only_admin_callback(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    async with state.proxy() as data:
        admin_id = data['admin_id']
    if callback.from_user.id != admin_id:
        await callback.answer(langs[lang]['only_admin'], show_alert=True)
        return False
    return True


@dp.message_handler(commands=['class'],
                    state=[
                        *ClassStates.all_states,
                        *GroupStates.all_states,
                        *LessonStates.all_states,
                        None
                    ])
async def edit_class(message: Message, state: FSMContext, callback=None):
    lang = choose_language(message)

    s = connect()
    try:
        editclass = s.query(Class).filter(Class.chat_id == message.chat.id).one()
    except sqlalchemy.exc.NoResultFound:
        editclass = False
    s.close()
    if editclass:
        user_action = callback if callback else message
        if int(editclass.admin_id) == user_action.from_user.id:
            async with state.proxy() as data:
                data['admin_id'] = user_action.from_user.id
            await ClassStates.edit_class.set()
            await message.answer(markdownv2(langs[lang]['edit_class'].format(name=editclass.name)), reply_markup=keyboards.edit_class(message, lang))
        else:
            await only_admin_message(message, state)
    else:
        async with state.proxy() as data:
            data['admin_id'] = message.from_user.id
        await ClassStates.new_class.set()
        await message.answer(markdownv2(langs[lang]['new_class']), reply_markup=keyboards.class_name(message, lang))


@dp.message_handler(content_types=['text'], state=ClassStates.new_class)
async def new_class(message: Message, state: FSMContext):
    lang = choose_language(message)

    if await only_admin_message(message, state):
        new_class_obj = Class(message.chat.id, message.from_user.id, message.text, 'en', True, 10, datetime.datetime(year=2005, month=9, day=9, hour=18), 3)
        s = connect()
        s.add(new_class_obj)
        s.commit()
        await message.answer(markdownv2(langs[lang]['new_class_created'].format(name=new_class_obj.name)))
        await edit_class(message, state)


@dp.callback_query_handler(state=ClassStates.new_class)
async def callback_new_class(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    if await only_admin_callback(callback, state):
        if callback.data == 'cancel':
            await state.finish()
            await callback.message.delete()


@dp.callback_query_handler(state=ClassStates.edit_class)
async def callback_edit_class(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    if await only_admin_callback(callback, state):
        if callback.data == 'cancel':
            await state.finish()
        elif callback.data == 'delete':
            await ClassStates.delete_class.set()
            s = connect()
            name = s.query(Class.name).filter(Class.chat_id == callback.message.chat.id).one()[0]
            await callback.message.answer(markdownv2(langs[lang]['delete_class'].format(name=name)), reply_markup=keyboards.delete_class(callback.message, lang))
        elif callback.data == 'name':
            await ClassStates.edit_class_name.set()
            await callback.message.answer(markdownv2(langs[lang]['edit_class_name']), reply_markup=keyboards.class_name(callback.message, lang))
        await callback.message.delete()


@dp.callback_query_handler(state=ClassStates.edit_class_name)
async def callback_edit_class_name(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    if await only_admin_callback(callback, state):
        if callback.data == 'cancel':
            await edit_class(callback.message, state, callback)


@dp.callback_query_handler(state=ClassStates.delete_class)
async def callback_delete_class(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    if await only_admin_callback(callback, state):
        if callback.data == 'no':
            await edit_class(callback.message, state, callback)
        elif callback.data == 'yes':
            await ClassStates.sure_delete_class.set()
            await callback.message.answer(markdownv2(langs[lang]['sure_delete_class']), reply_markup=keyboards.sure_delete_class(callback.message, lang))
        await callback.message.delete()


@dp.callback_query_handler(state=ClassStates.sure_delete_class)
async def callback_sure_delete_class(callback: CallbackQuery, state: FSMContext):
    lang = choose_language(callback.message)

    if await only_admin_callback(callback, state):
        if callback.data == 'no':
            await edit_class(callback.message, state, callback)
        elif callback.data == 'yes':
            s = connect()
            class_query = s.query(Class).filter(Class.chat_id == callback.message.chat.id)
            class_id = class_query[0].id
            class_query.delete()
            # groups_query = s.query(Group).filter(Group.class_id == class_id)
            # groups = [i.id for i in groups_query]
            # groups_query.delete()
            # s.query(Lesson).filter(Lesson.group.id in groups).delete()
            s.commit()
            await callback.message.answer(markdownv2(langs[lang]['sure_delete_class_deleted']))
        await callback.message.delete()


@dp.message_handler(content_types=['text'], state=ClassStates.edit_class_name)
async def edit_class_name(message: Message, state: FSMContext):
    lang = choose_language(message)

    if await only_admin_message(message, state):
        s = connect()
        s.query(Class).update({Class.name: message.text})
        s.commit()
        s.close()
        await message.answer(markdownv2(langs[lang]['edit_class_name_changed'].format(name=message.text)))
        await edit_class(message, state)
