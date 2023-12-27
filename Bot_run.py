import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import Redis, RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage

from config.config import load_config
from handlers import user_handlers, admin_handlers, other_handlers
from keyboards.main_menu import main_menu
from database.base import *
from sqlalchemy import URL, create_engine


async def main():
    config = load_config()
    postgres_url = URL.create(
        "postgresql",
        username='postgres',
        host='127.0.0.1',
        database='tgbot',
        port=5432,
        password='1234'
    )

    storage = RedisStorage(redis=Redis(host='localhost'))
    # storage = MemoryStorage()

    bot = Bot(token=config.token_for_bot)
    dispatcher = Dispatcher(storage=storage)

    engine = create_engine(postgres_url, echo=True)
    Base.metadata.create_all(bind=engine)
    # print('Db created')
    # with Session(autoflush=False, bind=engine) as session:

    await main_menu(bot)

    dispatcher.include_router(user_handlers.router)
    dispatcher.include_router(admin_handlers.router)
    dispatcher.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
