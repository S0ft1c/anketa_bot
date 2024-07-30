from aiogram import Router

from .group_callback_start_handler import callback_start_router
from .pure_start_handler import pure_start_router

start_commands_router = Router()

# including
start_commands_router.include_routers(
    callback_start_router,
    pure_start_router,
)
