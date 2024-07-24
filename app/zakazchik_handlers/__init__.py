from aiogram import Router
from .ya_zakazchik_callback_handler import ya_zakazchik_router
from app.zakazchik_handlers.create_order_handlers import create_order_handlers_router
from app.zakazchik_handlers.view_my_orders import view_my_orders_router

zakazchik_handlers_router = Router()

# include routers
zakazchik_handlers_router.include_routers(
    ya_zakazchik_router,
    create_order_handlers_router,
    view_my_orders_router,

)
