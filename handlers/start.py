from aiogram import Router, F
from aiogram.types import Message
from keyboards import auth_menu, edit_menu
from aiogram_run import config

start_router = Router()


@start_router.message(F.text == "Попробовать снова")
@start_router.message(F.text == "/start")
async def cmd_start(message: Message) -> None:
    """
    Начало работы с ботом. Запуск бота.
    """
    if str(message.chat.id) != config.OWNER_CHAT_ID:
        await message.answer("Для начала работы поделитесь своим номером.", reply_markup=auth_menu())
    else:
        await message.answer("Здравствуйте, давайте настроим вашего бота.", reply_markup=edit_menu())



