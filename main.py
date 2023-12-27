from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import URL
from sqlalchemy.orm import Session
import random

from database.base import *
from database.db_functions import get_all_tasks
from config.config import load_config
from environs import Env


# строка подключения
POSTGRES_URL = URL.create(
    "postgresql",
    username='postgres',
    host='127.0.0.1',
    database='tgbot',
    port=5432,
    password='1234',
)
# создаем движок SqlAlchemy
engine = create_engine(POSTGRES_URL)

Base.metadata.create_all(bind=engine)

# with Session(autoflush=False, bind=engine) as ses:
#     user = User(user_id=2344)
#     ses.add(user)
#     ses.commit()

# with Session(autoflush=False, bind=engine) as session:
#     user = session.get(User, 35225)
#     new_user = User(
#         user_id=35225
#     )
#     session.add(new_user)
#     session.commit()

logic_task_list = {
    'task1': {'text': 'Сколько месяцев в году имеют 28 дней?', 'answer': 'Все месяцы', 'level': random.randint(1, 3)},
    'task2': {'text': 'Как спрыгнуть с десятиметровой лестницы и не ушибиться?',
              'answer': 'Нужно прыгать с нижней ступени', 'level': random.randint(1, 3)},
    'task3': {'text': 'Что можно видеть с закрытыми глазами?', 'answer': 'Сны', 'level': random.randint(1, 3)},
    'task4': {'text': 'Что нужно делать, когда видишь зелёного человечка?', 'answer': 'Переходить улицу',
              'level': random.randint(1, 3)},
    'task5': {'text': 'Можно ли зажечь обычную спичку под водой, чтобы она догорела до конца?',
              'answer': 'Да, в подводной лодке', 'level': random.randint(1, 3)},
    'task6': {'text': 'Из какой посуды нельзя ничего поесть?', 'answer': 'Из пустой', 'level': random.randint(1, 3)},
    'task7': {'text': 'В каком месяце болтливая Светочка говорит меньше всего?',
              'answer': 'В феврале – самом коротком месяце', 'level': random.randint(1, 3)},
}


def create_task(obj: dict):
    with Session(autoflush=False, bind=engine) as session:
        task = Task(text=obj['text'], answer=obj['answer'], level=obj['level'])
        session.add(task)
        session.commit()

#
# for element, value in logic_task_list.items():
#     create_task(value)

# with Session(autoflush=False, bind=engine) as session:
#     user = User(user_id=5555)
#     session.add(user)
#     session.commit()

# with Session(bind=engine) as session:
#     task_list = session.query(Task).all()
#     for el in task_list:
#         print(el.id, el.text)


# env = Env()
# env.read_env()
# admin = env.list('ADMIN_LIST')
# for el in map(lambda x: int(x), admin):
#     print(el, type(el))


def get_session(postgres_url: URL) -> Session:
    with Session(autoflush=False, bind=create_engine(postgres_url)) as session:
        return session


task = Task(text='main task', answer='ans main', level=2)
session = get_session(POSTGRES_URL)
session.add(task)
session.commit()
