from aiogram import Router
from .pure_start_handler import pure_start_router

start_commands_router = Router()

# including
start_commands_router.include_routers(
    pure_start_router,
)
