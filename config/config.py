from dataclasses import dataclass
from environs import Env


@dataclass
class ConfigBot:
    token_for_bot: str
    admin_list: list[int]


def load_config(path: str | None = None) -> ConfigBot:
    env = Env()
    env.read_env(path)
    return ConfigBot(token_for_bot=env('BOT_TOKEN'), admin_list=env.list('ADMIN_LIST'))
