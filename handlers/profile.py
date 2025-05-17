from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatAction
from keyboards import profile_menu
from aiogram_run import bitrix, cache_manager, bot

profile_router = Router()


@profile_router.message(F.text == "Профиль")
async def show_profile(message: Message) -> None:
    """
    Вывод общей информации о клиенте.
    """
    chat_id = message.from_user.id

    await bot.send_chat_action(chat_id, ChatAction.TYPING)

    company_id = await cache_manager.get_company_id(chat_id)
    orders = await cache_manager.get_orders(company_id)
    contact_id = await bitrix.get_contact_id_by_company_id(company_id)
    if contact_id:
        full_name = await bitrix.get_full_name_by_contact_id(contact_id)
    else:
        full_name = ''
    manager_id = await bitrix.get_assigned_by_id(company_id)
    if manager_id:
        manager_name = await bitrix.get_responsible_name(manager_id)
    else:
        manager_name = ''
    company_info = await bitrix.get_company_title_and_inn_by_id(company_id)

    orders = orders or []
    total_orders_amount = sum(float(order.get("amount", 0)) for order in orders)

    profile_text = (
        f"{full_name}\n"
        f"Организация: {company_info["company_title"]}\n"
        f"ИНН: {company_info["inn"]}\n"
        f"Заказы в работе: {len(orders)}\n"
        f"Сумма заказов: {total_orders_amount}₽\n"
        f"Менеджер: {manager_name}\n"
    )

    await message.answer(profile_text, reply_markup=profile_menu())
