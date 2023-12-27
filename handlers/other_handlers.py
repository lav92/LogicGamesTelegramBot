from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def other_update(message: Message):
    await message.answer(f'repeat{message.text}')
