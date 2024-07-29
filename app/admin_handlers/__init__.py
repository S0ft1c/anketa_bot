from aiogram import Router

from app.admin_handlers.admin_hours_commit import admin_hours_commit_router
from .admin_command_handler import admin_command_router
from .admin_long_projects import admin_long_projects_router

admin_router: Router = Router()

# include stuff
admin_router.include_routers(
    admin_command_router,
    admin_hours_commit_router,
    admin_long_projects_router

)
