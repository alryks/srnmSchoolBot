import datetime


class Class():
    def __init__(
            self,

            chat_id,
            admin_id,
            name,

            lang,
            notify,
            lesson,
            tomorrow,
            timezone
    ):
        self.chat_id = chat_id
        self.admin_id = admin_id
        self.name = name

        self.lang = lang
        self.notify = notify
        self.lesson = lesson
        self.tomorrow = tomorrow
        self.timezone = timezone


class Group():
    def __init__(
            self,

            class_id,
            name
    ):
        self.class_id = class_id
        self.name = name


class Lesson():
    def __init__(
            self,

            group_id,

            name,
            start,
            length,
            homework,
            place,
            weekly
    ):
        self.group_id = group_id

        self.name = name
        self.start = start
        self.length = length
        self.homework = homework
        self.place = place
        self.weekly = weekly
