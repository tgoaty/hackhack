from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def edit_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Изменить настройки")],
        ],
        resize_keyboard=True
    )