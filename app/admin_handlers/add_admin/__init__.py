from aiogram import Router

from .add_admin_to_admins_handler import add_admin_to_admins_router

add_admin_router = Router()

# include all routers
add_admin_router.include_routers(
    add_admin_to_admins_router
)
