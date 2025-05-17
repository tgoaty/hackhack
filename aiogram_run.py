import asyncio


from logger_config import get_logger
from cash_memory.cash_manager import GlobalCacheManager
from config_global import config, db, dp, bot
from bitrix_api.bitrix import BitrixAPI

from handlers import *


logger = get_logger(__name__)


bitrix = BitrixAPI(config.BITRIX_TOKEN)

cache_manager = GlobalCacheManager(db, bitrix)


async def main():
    try:
        dp.include_routers(
            auth_router,
            orderList_router,
            order_router,
            profile_router,
            start_router,
            help_router,
            manager_router,
            public_link_router,
            setting_router,
        )


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
