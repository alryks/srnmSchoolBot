import sqlalchemy.exc
from sqlalchemy import create_engine, Table, Column, INTEGER, VARCHAR, BOOLEAN, DATETIME, MetaData, ForeignKey
from sqlalchemy.orm import mapper, Session

from db.model import *

from settings import DB

import datetime


def initialise():
    meta = MetaData()

    users = Table('users', meta,
                  Column('id', INTEGER, primary_key=True, autoincrement=True, unique=True, nullable=False),
                  Column('telegram_id', VARCHAR(10), primary_key=False, autoincrement=False, unique=False, nullable=False),
                  Column('lang', VARCHAR(2), primary_key=False, autoincrement=False, unique=False, nullable=False, default='en'),
                  # mysql_engine='MyISAM'
                  )

    classes = Table('classes', meta,
                    Column('id', INTEGER, primary_key=True, autoincrement=True, unique=True, nullable=False),
                    Column('chat_id', INTEGER, primary_key=False, autoincrement=False, unique=False, nullable=False, default=-1),

                    Column('name', VARCHAR(64), primary_key=False, autoincrement=False, unique=False, nullable=False),
                    Column('lang', VARCHAR(2), primary_key=False, autoincrement=False, unique=False, nullable=False, default='en'),
                    Column('notify', BOOLEAN, primary_key=False, autoincrement=False, unique=False, nullable=False, default=True),
                    Column('notify_day_before', DATETIME, primary_key=False, autoincrement=False, unique=False, nullable=False, default=datetime.datetime(year=2005, month=9, day=9, hour=18)),
                    Column('notify_before_lesson', INTEGER, primary_key=False, autoincrement=False, unique=False, nullable=False, default=10),
                    Column('tz', INTEGER, primary_key=False, autoincrement=False, unique=False, nullable=False, default=3),
                    # mysql_engine='MyISAM'
                    )

    user_classes = Table('user_classes', meta,
                         Column('id', INTEGER, primary_key=True, autoincrement=True, unique=True, nullable=False),
                         Column('user_id', INTEGER, ForeignKey('users.id'), primary_key=False, autoincrement=False, unique=False, nullable=False),
                         Column('class_id', INTEGER, ForeignKey('classes.id'), primary_key=False, autoincrement=False, unique=False, nullable=False),
                         # mysql_engine='MyISAM'
                         )

    groups = Table('groups', meta,
                   Column('id', INTEGER, primary_key=True, autoincrement=True, unique=True, nullable=False),
                   Column('class_id', INTEGER, ForeignKey('classes.id'), primary_key=False, autoincrement=False, unique=False, nullable=False),
                   Column('name', VARCHAR(64), primary_key=False, autoincrement=False, unique=False, nullable=False),
                   # mysql_engine='MyISAM'
                   )

    lessons = Table('lessons', meta,
                    Column('id', INTEGER, primary_key=True, autoincrement=True, unique=True, nullable=False),
                    Column('group_id', INTEGER, ForeignKey('groups.id'), primary_key=False, autoincrement=False, unique=False, nullable=False),

                    Column('name', VARCHAR(64), primary_key=False, autoincrement=False, unique=False, nullable=False),
                    Column('start', DATETIME, primary_key=False, autoincrement=False, unique=False, nullable=False),
                    Column('length', INTEGER, primary_key=False, autoincrement=False, unique=False, nullable=False, default=45),
                    Column('homework', VARCHAR(1024), primary_key=False, autoincrement=False, unique=False, nullable=True),
                    Column('place', VARCHAR(256), primary_key=False, autoincrement=False, unique=False, nullable=True),
                    Column('weekly', BOOLEAN, primary_key=False, autoincrement=False, unique=False, nullable=False, default=False),
                    # mysql_engine='MyISAM'
                    )

    weekly_lessons = Table('weekly_lessons', meta,
                           Column('id', INTEGER, primary_key=True, autoincrement=True, unique=True, nullable=False),
                           Column('lesson_id', INTEGER, primary_key=False, autoincrement=False, unique=False, nullable=False),
                           Column('week', INTEGER, primary_key=False, autoincrement=False, unique=False, nullable=False),

                           Column('name', VARCHAR(64), primary_key=False, autoincrement=False, unique=False, nullable=True),
                           Column('homework', VARCHAR(1024), primary_key=False, autoincrement=False, unique=False, nullable=True),
                           Column('place', VARCHAR(1024), primary_key=False, autoincrement=False, unique=False, nullable=True),
                           # mysql_engine='MyISAM'
                           )

    engine = create_engine(f'mysql+pymysql://{DB["user"]}:{DB["password"]}@{DB["host"]}/{DB["name"]}', echo=True)
    meta.create_all(engine)


def connect():
    engine = create_engine(f'mysql+pymysql://{DB["user"]}:{DB["password"]}@{DB["host"]}/{DB["name"]}', echo=False)
    meta = MetaData(engine)

    users = Table('users', meta, autoload=True)
    classes = Table('classes', meta, autoload=True)
    user_classes = Table('user_classes', meta, autoload=True)
    groups = Table('groups', meta, autoload=True)
    lessons = Table('lessons', meta, autoload=True)
    weekly_lessons = Table('weekly_lessons', meta, autoload=True)

    try:
        mapper(Users, users)
        mapper(Classes, classes)
        mapper(UserClasses, user_classes)
        mapper(Groups, groups)
        mapper(Lessons, lessons)
        mapper(WeeklyLessons, weekly_lessons)
    except sqlalchemy.exc.ArgumentError:
        pass

    session = Session(bind=engine)
    return session
