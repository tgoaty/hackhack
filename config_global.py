
from config.config import BotConfig
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from db_handler import db_class

config = BotConfig.from_command_line()
bot = Bot(token=config.TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
db = db_class.Database(config.PG_LINK)
