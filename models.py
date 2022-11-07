from aiogram.dispatcher.filters.state import State, StatesGroup


class ClassStates(StatesGroup):
    new_class = State()
    edit_class = State()
    edit_class_name = State()
    delete_class = State()
    sure_delete_class = State()


class GroupStates(StatesGroup):
    groups = State()
    add_group = State()
    group = State()
    edit_group_name = State()
    delete_group = State()


class LessonStates(StatesGroup):
    timetable = State()
    copy_timetable = State()
    lesson = State()
    lesson_name = State()
    time = State()
    start_time = State()
    length = State()
    homework = State()
    place = State()


class SettingsStates(StatesGroup):
    settings = State()
    timezone = State()
    time = State()