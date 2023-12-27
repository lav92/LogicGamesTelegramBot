from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from environs import Env

from lexicon.lexicon_ru import LEXICON
from keyboards.keyboards import *
from database.db_functions import *

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    check_user_and_create(message.from_user.id)
    await message.answer(LEXICON[message.text], reply_markup=get_go_button(message.from_user.id))


@router.message(Command(commands='help'))
async def help_for_user(message: Message):
    await message.answer(LEXICON[message.text], reply_markup=get_go_button(message.from_user.id))


@router.message(Command(commands='break_brain'))
async def choice_lvl(message: Message):
    await message.answer(text='Выберите уровень', reply_markup=get_levels_brain_task())


@router.callback_query(F.data[0].isdigit())
async def get_task_by_difficult(callback: CallbackQuery):
    page = 1
    if 'page' in callback.data:
        page = int(callback.data.split('=')[-1])
    prefix = int(callback.data[0])
    resolved_task_list = get_resolved_tasks(callback.from_user.id)
    await callback.message.edit_text(text=LEXICON[callback.data[0]],
                                     reply_markup=get_keyboard_by_lvl(resolved_task_list, prefix, page))


@router.callback_query(F.data.startswith('all'))
async def get_all_task(callback: CallbackQuery):
    page = 1
    if 'page' in callback.data:
        page = int(callback.data.split('=')[-1])
    user_pk = int(callback.from_user.id)
    resolved_task = get_resolved_tasks(user_pk)
    await callback.message.edit_text(text='Все задачи',
                                     reply_markup=get_all_tasks_keyboard(resolved_task, prefix='all', page=page))


@router.callback_query(F.data.startswith('task_'))
async def get_task(callback: CallbackQuery):
    pk = int(callback.data[5:])
    task = get_task_from_db(pk)
    await callback.message.edit_text(text=task.text, reply_markup=get_keyboard_for_task(pk))


@router.callback_query(F.data.startswith('get_answer_'))
async def get_answer(callback: CallbackQuery):
    pk = int(callback.data.split('_')[-1])
    task = get_task_from_db(pk)
    text = f'{task.text}\n\nОТВЕТ:\n{task.answer}'
    append_to_resolve_list(callback.from_user.id, task)
    await callback.message.edit_text(text=text, reply_markup=get_back_button())


@router.callback_query(F.data == 'back')
async def return_to_task_choice(callback: CallbackQuery):
    await callback.message.edit_text(text='Выберите уровень', reply_markup=get_levels_brain_task())
