from aiogram import Router
from app.start_commands import start_commands_router
from app.zakazchik_handlers import zakazchik_handlers_router
from app.ispolnitel_handlers import ispolnotel_router

router = Router()

# adding all the routers
router.include_routers(
    start_commands_router,
    zakazchik_handlers_router,
    ispolnotel_router
)
