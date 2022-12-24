from aiogram.dispatcher.filters.state import State, StatesGroup


class GroupStates(StatesGroup):
    choose_group = State()
    timetable = State()
    lesson = State()


class PrivateStates(StatesGroup):
    settings = State()
    class_verify = State()
    class_create_name = State()
    class_choose = State()
    class_now = State()
    class_delete = State()
    class_change_name = State()

    class_settings = State()
    class_admins = State()
    class_add_admin = State()
    class_notifications = State()
    class_timezone = State()

    group_create_name = State()
    group_choose = State()
    group_now = State()
    group_change_name = State()
    group_delete = State()

    group_timetable = State()
    group_copy_timetable = State()

    lesson_create = State()
    lesson_create_name = State()
    lesson_create_time = State()
    lesson_create_homework = State()
    lesson_create_place = State()

    lesson = State()
    lesson_name = State()
    lesson_time = State()
    lesson_homework = State()
    lesson_place = State()
