import os
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from dotenv import load_dotenv
from keyboards import auth_menu, edit_menu

load_dotenv()
start_router = Router()

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📧 Email", callback_data="contact:email"),
         InlineKeyboardButton(text="📞 Телефон", callback_data="contact:phone")]
    ]
)

@start_router.message(F.text == "Попробовать снова")
@start_router.message(F.text == "/start")
async def cmd_start(message: Message) -> None:
    """
    Начало работы с ботом. Запуск бота.
    """
    if str(message.chat.id) != os.getenv('OWNER_CHAT_ID'):
        await message.answer("Для начала работы поделитесь своим номером.", reply_markup=auth_menu())
    else:
        await message.answer("Здравствуйте, давайте настроим вашего бота.", reply_markup=edit_menu())
        await message.answer("Выберите тип контактной информации для авторизации пользователся:", reply_markup=keyboard)



