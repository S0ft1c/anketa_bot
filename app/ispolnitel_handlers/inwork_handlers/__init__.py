from aiogram import Router

from .active_work_handler import active_work_router
from .end_work_on_order_handler import end_work_on_order_router
from .join_to_order_request_handler import join_order_router
from .start_work_on_order_handler import start_work_on_order_router
from .worker_look_in_orderid_handler import worker_look_in_orderid_router

inwork_router = Router()

# include all routers
inwork_router.include_routers(
    join_order_router,
    active_work_router,
    worker_look_in_orderid_router,
    start_work_on_order_router,
    end_work_on_order_router,

)
