import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config.config import BotConfig
from logger_config import get_logger
from db_handler import db_class
from cash_memory.cash_manager import GlobalCacheManager


logger = get_logger(__name__)


config = BotConfig.from_command_line()
bot = Bot(token=config.TELEGRAM_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

db = db_class.Database(config.PG_LINK)

from bitrix_api.bitrix import BitrixAPI

print("loool", config.BITRIX_TOKEN)
bitrix = BitrixAPI(config.BITRIX_TOKEN)

cache_manager = GlobalCacheManager(db, bitrix)






async def main():
    try:


        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Бот запущен в режиме polling")

        await dp.start_polling(bot)


    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
