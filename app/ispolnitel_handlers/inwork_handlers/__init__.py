from aiogram import Router

from .active_work_handler import active_work_router
from .join_to_order_request_handler import join_order_router

inwork_router = Router()

# include all routers
inwork_router.include_routers(
    join_order_router,
    active_work_router
)
