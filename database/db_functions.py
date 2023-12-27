from sqlalchemy.orm import Session
from database.base import User, Task
from sqlalchemy import create_engine, URL

POSTGRES_URL = URL.create(
    "postgresql",
    username='postgres',
    host='127.0.0.1',
    database='tgbot',
    port=5432,
    password='1234'
)


def get_session(postgres_url: URL) -> Session:
    with Session(autoflush=False, bind=create_engine(postgres_url)) as session:
        return session


session = get_session(POSTGRES_URL)


def check_user_and_create(user_pk: int):
    user = session.get(User, user_pk)
    if user:
        print(f'{user} exist')
    else:
        session.add(User(user_id=user_pk))
        session.commit()


def get_all_tasks() -> list[Task]:
    return list(session.query(Task).all())


def get_task_from_db(pk: int):
    task = session.get(Task, pk)
    print('in get task func')
    print(task)
    return task


def get_resolved_tasks(user_pk: int) -> list[Task]:
    user = session.get(User, user_pk)
    return user.tasks


def append_to_resolve_list(user_pk: int, task: Task):
    user = session.get(User, user_pk)
    if task not in user.tasks:
        user.tasks.append(task)
        session.commit()


def get_task_by_lvl(lvl: int):
    result = list(session.query(Task).filter_by(level=lvl))
    return result


def delete(pk: int):
    task = session.get(Task, pk)
    session.delete(task)
    session.commit()


def add_task_in_db(text: str, answer: str, level: int):
    task = Task(text=text, answer=answer, level=level)
    session.add(task)
    session.commit()
