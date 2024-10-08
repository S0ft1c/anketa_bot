from aiogram import Router

from .delete_order_by_id_handler import delete_order_by_id_router
from .edit_long_days_in_id_handler import edit_long_days_in_id_router
from .end_order_by_id_handler import end_order_by_id_router
from .list_my_orders_handler import list_my_orders_router
from .report_end_order_handler import report_end_order_router
from .send_to_exact_person_handler import send_to_exact_person_router
from .view_order_by_id_handler import view_order_by_id_router

view_my_orders_router = Router()

# include
view_my_orders_router.include_routers(
    list_my_orders_router,
    view_order_by_id_router,
    edit_long_days_in_id_router,
    delete_order_by_id_router,
    end_order_by_id_router,
    report_end_order_router,
    send_to_exact_person_router,

)
