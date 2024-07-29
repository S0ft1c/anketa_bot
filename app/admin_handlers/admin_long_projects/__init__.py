from aiogram import Router

from .admin_end_long_project_handler import admin_end_long_project_router
from .admin_long_projects_list_handler import admin_long_projects_list_router
from .admin_view_long_project_handler import admin_view_long_project_router

admin_long_projects_router = Router()

# include all

admin_long_projects_router.include_routers(
    admin_long_projects_list_router,
    admin_view_long_project_router,
    admin_end_long_project_router
)
