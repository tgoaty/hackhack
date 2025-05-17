from aiogram import Router, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from create_bot import bitrix


setting_router = Router()

CONFIG_PATH = "config/field_preferences.json"


@setting_router.message(F.text == "Изменить настройки")
async def ask_contact_type(message: types.Message):
    a = await bitrix.get_deal_fields_as_buttons()
    b = await bitrix.get_company_fields_as_buttons()
    c = await bitrix.get_deal_categories_as_buttons()

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📧 Email", callback_data="contact:email"),
                InlineKeyboardButton(text="📞 Телефон", callback_data="contact:phone")
            ]
        ]
    )
    await message.answer("Какой тип контакта использовать по умолчанию?", reply_markup=kb)


