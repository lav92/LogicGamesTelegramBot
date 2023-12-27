from aiogram import Bot
from aiogram.types import BotCommand


async def main_menu(bot: Bot):
    menu_commands = [
        BotCommand(command='/start', description='Привет! Это бот в котором есть задачи на логику!'),
        BotCommand(command='/help', description='Справка как работает бот'),
        BotCommand(command='/break_brain', description='Начать решать логические задачи'),
    ]
    await bot.set_my_commands(menu_commands)
