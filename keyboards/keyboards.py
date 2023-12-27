from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.db_functions import get_all_tasks, get_task_by_lvl
from database.base import Task
from services.services import get_num_of_last_page
from environs import Env

env = Env()
env.read_env()
ADMINS = env.list('ADMIN_LIST')


def paginate(builder: InlineKeyboardBuilder, query_list: list[InlineKeyboardButton],
             prefix: int | str = None, page=1, callback_for_btn: str = 'back'):
    if len(query_list) > 10:
        last_page = get_num_of_last_page(len(query_list))
        prev_page = page - 1 if page > 1 else 1
        next_page = page + 1 if page < last_page else last_page
        print(f'page={page}prev page={prev_page}next page={next_page}last page={last_page}')
        builder.row(*query_list[page * 10 - 10:page * 10], width=1)
        pagination = [
            InlineKeyboardButton(text='<<' if page > 1 else '❌',
                                 callback_data=f'{prefix}?page={prev_page}' if page > 1 else 'None'),
            InlineKeyboardButton(text=f'page {page}', callback_data='None'),
            InlineKeyboardButton(text='>>' if page < last_page else '❌',
                                 callback_data=f'{prefix}?page={next_page}' if page < last_page else 'None'),
        ]

        builder.row(*pagination)
        builder.row(InlineKeyboardButton(text='Назад', callback_data=callback_for_btn))
    else:
        builder.row(*query_list, width=1)
        builder.row(InlineKeyboardButton(text='Назад', callback_data=callback_for_btn))
    return builder.as_markup()


def get_levels_brain_task() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    button_list = [
        InlineKeyboardButton(text='Легкий уровень 🧠', callback_data='1'),
        InlineKeyboardButton(text='Средний уровень 🧠🧠', callback_data='2'),
        InlineKeyboardButton(text='Сложный уровень 🧠🧠🧠', callback_data='3'),
        InlineKeyboardButton(text='Все задачи', callback_data='all')
    ]

    builder.row(*button_list, width=1)

    return builder.as_markup()


def get_keyboard_by_lvl(resolved_list: list[Task], prefix: int, page=1) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    all_list = get_task_by_lvl(prefix)

    button_list = [InlineKeyboardButton(text=f'✅{task.text[:30]}... - Решено', callback_data=f'task_{task.id}')
                   if task in resolved_list else InlineKeyboardButton(text=task.text, callback_data=f'task_{task.id}')
                   for task in all_list]

    return paginate(builder, button_list, prefix, page)


def get_all_tasks_keyboard(resolved_task: list[Task], prefix: str, page=1) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    print(f'in kb builder all task{resolved_task}')
    button_list = [InlineKeyboardButton(text=f'✅{task.text[:30]}... - Решено', callback_data=f'task_{task.id}')
                   if task in resolved_task else InlineKeyboardButton(text=task.text, callback_data=f'task_{task.id}')
                   for task in get_all_tasks()]

    return paginate(builder, button_list, prefix, page)


def get_keyboard_for_task(pk: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    button_list = [
        InlineKeyboardButton(text='Показать ответ', callback_data=f'get_answer_{pk}'),
        InlineKeyboardButton(text='Назад', callback_data='back')
    ]
    builder.row(*button_list, width=1)
    return builder.as_markup()


def get_back_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Назад', callback_data='back'))
    return builder.as_markup()


def get_go_button(user_pk) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Перейти к выбору задачи', callback_data='back'))
    if user_pk in map(lambda member: int(member), ADMINS):
        builder.add(InlineKeyboardButton(text='ADMIN PANEL', callback_data='admin'))
    return builder.as_markup()
