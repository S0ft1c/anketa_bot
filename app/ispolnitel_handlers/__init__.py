from aiogram import Router

from app.ispolnitel_handlers.registrate_worker import registrate_worker_router
from .ya_ispolnitel_handler import ya_ispolnitel_router

ispolnotel_router = Router()

ispolnotel_router.include_routers(
    registrate_worker_router,
    ya_ispolnitel_router
)
