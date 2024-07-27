from aiogram import Router

from .admin_hours_commit_list_handler import admin_hours_commit_list_router
from .admin_minus_worker_handler import admin_minus_worker_router
from .admin_self_hours_commit_handler import admin_self_hours_commit_router
from .admin_submit_hours_commit_handler import admin_submit_hours_commit_router
from .view_review_id_handler import view_review_id_router

admin_hours_commit_router = Router()

# include
admin_hours_commit_router.include_routers(
    admin_hours_commit_list_router,
    view_review_id_router,
    admin_submit_hours_commit_router,
    admin_self_hours_commit_router,
    admin_minus_worker_router

)
