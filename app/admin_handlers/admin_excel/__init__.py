from aiogram import Router

from .admin_view_options_excel_handler import admin_view_options_excel_router
from .to_excel_all_orders_by_own_data_handler import to_excel_all_orders_by_own_data_router
from .to_excel_all_orders_by_week_handler import to_excel_all_orders_by_week_router
from .to_excel_all_workers_handler import to_excel_all_workers_router
from .to_excel_by_own_data_handler import to_excel_by_own_data_router
from .to_excel_by_week_handler import to_excel_by_week_router

admin_excel_router = Router()

# include
admin_excel_router.include_routers(
    admin_view_options_excel_router,
    to_excel_by_own_data_router,
    to_excel_by_week_router,
    to_excel_all_orders_by_week_router,
    to_excel_all_orders_by_own_data_router,
    to_excel_all_workers_router
)
