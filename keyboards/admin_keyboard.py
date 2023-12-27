from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.db_functions import get_all_tasks
from keyboards.keyboards import paginate

LVL_LIST = {1: '🧠', 2: '🧠🧠', 3: '🧠🧠🧠'}


def admin_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text='Создать задачу', callback_data='create'),
        InlineKeyboardButton(text='Удалить задачу', callback_data='delete'),
        InlineKeyboardButton(text='Reset FSM state', callback_data='cancel'),
    ]
    builder.row(*buttons)
    return builder.as_markup()


def delete_keyboard(page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    button_list = [InlineKeyboardButton(text=f'🚫 id={task.id} {task.text}', callback_data=f'del_task_{task.id}')
                   for task in get_all_tasks()]
    return paginate(builder, button_list, 'delete', page=page, callback_for_btn='admin')


def choice_lvl() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    button_list = [InlineKeyboardButton(text=value, callback_data=f'create_{key}') for key, value in LVL_LIST.items()]
    button_list.append(InlineKeyboardButton(text='Отмена', callback_data='cancel'))
    builder.row(*button_list, width=1)
    return builder.as_markup()


def cancel_btn() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Отмена', callback_data='cancel'))
    return builder.as_markup()
