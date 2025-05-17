# Пакет с обработчиками сообщений
from .auth import auth_router
from .profile import profile_router
from .order import order_router
from .orderList import orderList_router
from .public_link import public_link_router
from .start import start_router
from .help import help_router
from .manager import manager_router
from .setting import setting_router

from aiogram_run import dp
__all__ = [
    "auth_router",
    "profile_router",
    "order_router",
    "orderList_router",
    "public_link_router",
    "start_router",
    "help_router",
    "manager_router",
    "setting_router"
]


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
