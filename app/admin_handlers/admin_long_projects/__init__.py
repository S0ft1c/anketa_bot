from aiogram import Router
from .admin_long_projects_list_handler import admin_long_projects_list_router

admin_long_projects_router = Router()

# include all

admin_long_projects_router.include_routers(
    admin_long_projects_list_router,
)
