from aiogram import Router

from .add_admin_to_admins_handler import add_admin_to_admins_router
from .delete_admin_from_admins_handler import delete_admin_from_admins_router

add_admin_router = Router()

# include all routers
add_admin_router.include_routers(
    add_admin_to_admins_router,
    delete_admin_from_admins_router
)
