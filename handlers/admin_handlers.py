from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext

from keyboards.admin_keyboard import admin_keyboard, delete_keyboard, choice_lvl, cancel_btn
from database.db_functions import delete, add_task_in_db

router = Router()


class FSMFillForm(StatesGroup):
    fill_text = State()
    fill_answer = State()
    fill_lvl = State()


@router.callback_query(F.data == 'admin')
async def get_admin_commands(callback: CallbackQuery):
    await callback.message.edit_text(text='Выберите действие', reply_markup=admin_keyboard())


@router.callback_query(F.data.startswith('delete'))
async def delete_task_list(callback: CallbackQuery):
    page = 1
    if 'page' in callback.data:
        page = int(callback.data.split('=')[-1])
    await callback.message.edit_text(text='Выберите задачу', reply_markup=delete_keyboard(page))


@router.callback_query(F.data.startswith('del_task_'))
async def delete_task(callback: CallbackQuery):
    print('in delete handler')
    task_pk = int(callback.data.split('_')[-1])
    print(task_pk)
    delete(task_pk)
    print(f'delete {task_pk}')
    await callback.message.edit_text(text='Выберите задачу', reply_markup=delete_keyboard(page=1))


@router.callback_query(StateFilter(default_state), F.data == 'create')
async def create_task(callback: CallbackQuery):
    await callback.message.edit_text(text='Для добавлния задачи введите команду /create_task',
                                     reply_markup=cancel_btn())


@router.message(Command(commands='create_task'), StateFilter(default_state))
async def start_create(message: Message, state: FSMContext):
    print('start create')
    await message.answer(text='Введите текст задачи', reply_markup=cancel_btn())
    await state.set_state(FSMFillForm.fill_text)


@router.message(StateFilter(FSMFillForm.fill_text))
async def process_text_sent(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    a = await state.get_data()
    print(a)
    await message.answer(text='Теперь введите ответ задачи', reply_markup=cancel_btn())
    await state.set_state(FSMFillForm.fill_answer)


@router.message(StateFilter(FSMFillForm.fill_answer))
async def process_answer_sent(message: Message, state: FSMContext):
    await state.update_data(answer=message.text)
    a = await state.get_data()
    print(a)
    await message.answer(text='Теперь выберите сложность задачи', reply_markup=choice_lvl())
    await state.set_state(FSMFillForm.fill_lvl)


@router.callback_query(StateFilter(FSMFillForm.fill_lvl), F.data.startswith('create_'))
async def set_lvl(callback: CallbackQuery, state: FSMContext):
    await state.update_data(lvl=int(callback.data.split('_')[-1]))
    data = await state.get_data()
    print(data)
    add_task_in_db(data['text'], data['answer'], data['lvl'])
    await state.clear()
    await callback.message.edit_text('Задача добавлена')
    st = await state.get_state()
    print(st)


@router.callback_query(~StateFilter(default_state), F.data == 'cancel')
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text('Вы отменили создание задачи')


@router.callback_query(~StateFilter(default_state), Command(commands='fsm_reset'))
async def fsm_reset(state: FSMContext):
    await state.clear()
    print('fsm reset')
