import datetime


class Users:
    def __init__(self,
                 telegram_id,
                 lang='en'
                 ):
        self.telegram_id = telegram_id
        self.lang = lang


class Classes:
    def __init__(self,
                 name,
                 chat_id=-1,

                 lang='en',
                 notify=True,
                 notify_day_before=datetime.datetime(year=2005, month=9, day=9, hour=18),
                 notify_before_lesson=10,
                 tz=3
                 ):
        self.chat_id = chat_id

        self.name = name
        self.lang = lang
        self.notify = notify
        self.notify_day_before = notify_day_before
        self.notify_before_lesson = notify_before_lesson
        self.tz = tz


class UserClasses:
    def __init__(self,
                 user_id,
                 class_id
                 ):
        self.user_id = user_id
        self.class_id = class_id


class Groups:
    def __init__(self,
                 class_id,
                 name
                 ):
        self.class_id = class_id
        self.name = name


class Lessons:
    def __init__(self,
                 group_id,

                 name,
                 start,
                 homework,
                 place,
                 length=45,
                 weekly=False
                 ):
        self.group_id = group_id

        self.name = name
        self.start = start
        self.length = length
        self.homework = homework
        self.place = place
        self.weekly = weekly


class WeeklyLessons:
    def __init__(self,
                 lesson_id,
                 week,

                 name,
                 homework,
                 place
                 ):
        self.lesson_id = lesson_id
        self.week = week

        self.name = name
        self.homework = homework
        self.place = place