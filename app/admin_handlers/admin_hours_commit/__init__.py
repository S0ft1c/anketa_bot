from aiogram import Router
from .admin_hours_commit_list_handler import admin_hours_commit_list_router

admin_hours_commit_router = Router()

# include
admin_hours_commit_router.include_routers(
    admin_hours_commit_list_router,

)
