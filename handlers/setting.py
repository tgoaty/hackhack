from aiogram import Router, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext

from create_bot import bitrix
from utils.storage import load_toggle_state, save_toggle_state

setting_router = Router()

STAGES = ["notifications", "fields", "order_fields", "funnels", "docs", "done"]

def notif_keyboard(selected: list[str] = None) -> InlineKeyboardMarkup:
    selected = selected or []
    buttons = [
        InlineKeyboardButton(text=("✅ " if cb in selected else "") + text, callback_data=cb)
        for cb, text in [("email", "Email"), ("phone", "Телефон"), ("telegram", "Telegram")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=[[btn] for btn in buttons])

async def fields_keyboard(selected: list[str] = None, with_next: bool = True, fields_arr=None) -> InlineKeyboardMarkup:
    selected = selected or []
    fields_arr = fields_arr or await bitrix.get_company_fields_as_buttons()
    buttons = [
        InlineKeyboardButton(text=("✅ " if cb in selected else "") + text, callback_data=cb)
        for cb, text in fields_arr
    ]
    if with_next:
        buttons.append(InlineKeyboardButton(text="Далее ▶️", callback_data="next"))
    return InlineKeyboardMarkup(inline_keyboard=[[btn] for btn in buttons])

async def order_fields_keyboard(selected: list[str] = None, with_next: bool = True, orders_arr=None) -> InlineKeyboardMarkup:
    selected = selected or []
    orders_arr = orders_arr or await bitrix.get_deal_fields_as_buttons()
    buttons = [
        InlineKeyboardButton(text=("✅ " if cb in selected else "") + text, callback_data=cb)
        for cb, text in orders_arr
    ]
    if with_next:
        buttons.append(InlineKeyboardButton(text="Далее ▶️", callback_data="next"))
    return InlineKeyboardMarkup(inline_keyboard=[buttons])

async def funnels_keyboard(selected: list[str] = None, with_next: bool = True, funnels_arr=None) -> InlineKeyboardMarkup:
    selected = selected or []
    funnels_arr = funnels_arr or await bitrix.get_deal_categories_as_buttons()
    buttons = [
        InlineKeyboardButton(text=("✅ " if cb in selected else "") + text, callback_data=cb)
        for cb, text in funnels_arr
    ]
    if with_next:
        buttons.append(InlineKeyboardButton(text="Далее ▶️", callback_data="next"))
    return InlineKeyboardMarkup(inline_keyboard=[[btn] for btn in buttons])

def docs_keyboard(selected: str | None = None) -> InlineKeyboardMarkup:
    buttons = []
    for cb, text in [("yes", "Да"), ("no", "Нет")]:
        prefix = "✅ " if cb == selected else ""
        buttons.append(InlineKeyboardButton(text=prefix + text, callback_data=cb))
    return InlineKeyboardMarkup(inline_keyboard=[buttons])

@setting_router.message(F.text == "Изменить настройки")
async def cmd_test(message: types.Message, state: FSMContext):
    # Один запрос к Bitrix — сразу все данные
    company_fields = await bitrix.get_company_fields_as_buttons()
    deal_fields = await bitrix.get_deal_fields_as_buttons()
    deal_categories = await bitrix.get_deal_categories_as_buttons()

    # Загружаем сохранённые настройки из хранилища
    notifications = load_toggle_state("notifications") or []
    fields = load_toggle_state("fields") or []
    order_fields = load_toggle_state("order_fields") or []
    funnels = load_toggle_state("funnels") or []
    docs = load_toggle_state("docs") or []

    # Сохраняем всё в состояние
    await state.update_data(
        company_fields=company_fields,
        deal_fields=deal_fields,
        deal_categories=deal_categories,
        notifications=notifications,
        fields=fields,
        order_fields=order_fields,
        funnels=funnels,
        docs=docs,
    )

    await message.answer("Оповещение через:", reply_markup=notif_keyboard(notifications))

@setting_router.callback_query()
async def cb_handler(callback: CallbackQuery, state: FSMContext):
    data = callback.data
    msg_text = callback.message.text or ""

    user_data = await state.get_data()

    company_fields = user_data.get("company_fields", [])
    deal_fields = user_data.get("deal_fields", [])
    deal_categories = user_data.get("deal_categories", [])

    notifications = user_data.get("notifications", [])
    fields = user_data.get("fields", [])
    order_fields = user_data.get("order_fields", [])
    funnels = user_data.get("funnels", [])
    docs = user_data.get("docs", [])

    # Определяем текущий этап по тексту сообщения
    if "Оповещение через" in msg_text:
        current_stage = "notifications"
    elif "Отображать поля:" in msg_text:
        current_stage = "fields"
    elif "Отображаемые поля в заказе:" in msg_text:
        current_stage = "order_fields"
    elif "Выбор воронок:" in msg_text:
        current_stage = "funnels"
    elif "Давать доступ к документам:" in msg_text:
        current_stage = "docs"
    else:
        current_stage = "done"

    if current_stage == "notifications":
        if data in ["email", "phone", "telegram"]:
            notifications = [data]
            save_toggle_state("notifications", notifications)
            await state.update_data(notifications=notifications)
            await callback.message.edit_text("Отображать поля:", reply_markup=await fields_keyboard(fields, fields_arr=company_fields))
            await callback.answer()
        else:
            await callback.answer("Пожалуйста, выберите способ оповещения")

    elif current_stage == "fields":
        selected = set(fields)
        if data == "next":
            await callback.message.edit_text("Отображаемые поля в заказе:", reply_markup=await order_fields_keyboard(order_fields, orders_arr=deal_categories))
            await callback.answer()
            return

        if data in [cb for cb, _ in company_fields]:
            if data in selected:
                selected.remove(data)
            else:
                selected.add(data)
            fields = list(selected)
            save_toggle_state("fields", fields)
            await state.update_data(fields=fields)
            await callback.message.edit_reply_markup(reply_markup=await fields_keyboard(fields, fields_arr=company_fields))
            await callback.answer()
        else:
            await callback.answer("Пожалуйста, выберите поле или 'Далее'")

    elif current_stage == "order_fields":
        selected = set(order_fields)
        if data == "next":
            await callback.message.edit_text("Выбор воронок:", reply_markup=await funnels_keyboard(funnels, funnels_arr=deal_fields))
            await callback.answer()
            return

        if data in [cb for cb, _ in deal_categories]:
            if data in selected:
                selected.remove(data)
            else:
                selected.add(data)
            order_fields = list(selected)
            save_toggle_state("order_fields", order_fields)
            await state.update_data(order_fields=order_fields)
            await callback.message.edit_reply_markup(reply_markup=await order_fields_keyboard(order_fields, orders_arr=deal_categories))
            await callback.answer()
        else:
            await callback.answer("Пожалуйста, выберите поле или 'Далее'")

    elif current_stage == "funnels":
        selected = set(funnels)
        if data == "next":
            await callback.message.edit_text("Давать доступ к документам:", reply_markup=docs_keyboard(docs[0] if docs else None))
            await callback.answer()
            return

        if data in [cb for cb, _ in deal_fields]:
            if data in selected:
                selected.remove(data)
            else:
                selected.add(data)
            funnels = list(selected)
            save_toggle_state("funnels", funnels)
            await state.update_data(funnels=funnels)
            await callback.message.edit_reply_markup(reply_markup=await funnels_keyboard(funnels, funnels_arr=deal_fields))
            await callback.answer()
        else:
            await callback.answer("Пожалуйста, выберите воронку или 'Далее'")

    elif current_stage == "docs":
        if data in ["yes", "no"]:
            save_toggle_state("docs", [data])
            await state.update_data(docs=[data])
            await callback.message.edit_text("Поздравляем, вы молодец!")
            await callback.answer()
        else:
            await callback.answer("Пожалуйста, выберите доступ к документам")

    else:
        await callback.answer("Процесс завершён")
