from aiogram import Router
from .list_my_orders_handler import list_my_orders_router
from .view_order_by_id_handler import view_order_by_id_router

view_my_orders_router = Router()

# include
view_my_orders_router.include_routers(
    list_my_orders_router,
    view_order_by_id_router,

)
