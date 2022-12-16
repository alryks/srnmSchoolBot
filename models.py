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
    class_delete_admin = State()
    class_add_admin = State()
    class_notifications = State()
    class_timezone = State()

    group_create_name = State()
    group_choose = State()
    group_change_name = State()
    group_delete = State()

    group_timetable = State()
    group_copy_timetable = State()

    group_lesson_create_name = State()
    group_create_lesson = State()
    group_lesson = State()
    group_lesson_change_name = State()
    group_time = State()
    group_homework = State()
    group_place = State()
