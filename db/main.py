import sqlalchemy.exc
from sqlalchemy import create_engine, Table, Column, INTEGER, VARCHAR, BOOLEAN, DATETIME, MetaData, ForeignKey
from sqlalchemy.orm import mapper, Session

from db.model import *

from settings import DB


def initialise():
    meta = MetaData()

    classes = Table('class', meta,
                    Column('id', INTEGER, primary_key=True, autoincrement=True, unique=True, nullable=False),
                    Column('chat_id', INTEGER, primary_key=False, autoincrement=False, unique=True, nullable=False),
                    Column('admin_id', VARCHAR(64), primary_key=False, autoincrement=False, unique=False, nullable=False),
                    Column('name', VARCHAR(64), primary_key=False, autoincrement=False, unique=False, nullable=False),

                    Column('lang', VARCHAR(2), primary_key=False, autoincrement=False, unique=False, nullable=False, default='en'),
                    Column('notify', BOOLEAN, primary_key=False, autoincrement=False, unique=False, nullable=False, default=True),
                    Column('lesson', INTEGER, primary_key=False, autoincrement=False, unique=False, nullable=False, default=5),
                    Column('tomorrow', DATETIME, primary_key=False, autoincrement=False, unique=False, nullable=False),
                    Column('timezone', INTEGER, primary_key=False, autoincrement=False, unique=False, nullable=False, default=3)
                    )

    group = Table('group', meta,
                  Column('id', INTEGER, primary_key=True, autoincrement=True, unique=True, nullable=False),
                  Column('class_id', INTEGER, ForeignKey('class.id'), primary_key=False, autoincrement=False, unique=False, nullable=False),
                  Column('name', VARCHAR(64), primary_key=False, autoincrement=False, unique=False, nullable=False)
                  )

    lesson = Table('lesson', meta,
                   Column('id', INTEGER, primary_key=True, autoincrement=True, unique=True, nullable=False),
                   Column('group_id', INTEGER, ForeignKey('group.id'), primary_key=False, autoincrement=False, unique=False, nullable=False),

                   Column('name', VARCHAR(64), primary_key=False, autoincrement=False, unique=False, nullable=False),
                   Column('start', DATETIME, primary_key=False, autoincrement=False, unique=False, nullable=False),
                   Column('length', INTEGER, primary_key=False, autoincrement=False, unique=False, nullable=False, default=45),
                   Column('homework', VARCHAR(1024), primary_key=False, autoincrement=False, unique=False, nullable=True),
                   Column('place', VARCHAR(256), primary_key=False, autoincrement=False, unique=False, nullable=True),
                   Column('weekly', BOOLEAN, primary_key=False, autoincrement=False, unique=False, nullable=False, default=False)
                   )

    engine = create_engine(f'mysql+pymysql://{DB["user"]}:{DB["password"]}@{DB["host"]}/{DB["name"]}', echo=True)
    meta.create_all(engine)


def connect():
    engine = create_engine(f'mysql+pymysql://{DB["user"]}:{DB["password"]}@{DB["host"]}/{DB["name"]}', echo=False)
    meta = MetaData(engine)

    classes = Table('class', meta, autoload=True)
    group = Table('group', meta, autoload=True)
    lesson = Table('lesson', meta, autoload=True)

    try:
        mapper(Class, classes)
        mapper(Group, group)
        mapper(Lesson, lesson)
    except sqlalchemy.exc.ArgumentError:
        pass

    session = Session(bind=engine)
    return session