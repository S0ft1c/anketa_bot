from aiogram import Router
from .list_my_orders import list_my_orders_router

view_my_orders_router = Router()

# include
view_my_orders_router.include_routers(
    list_my_orders_router,
)
