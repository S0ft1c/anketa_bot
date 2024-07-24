from aiogram import Router

from .register_fio import register_fio_router
from .registrate_worker_states import RegistrateWorkerStates
from .register_contact_handler import register_contact_router
from .register_date_of_birth import register_date_of_birth_router
from .registarte_area_of_residence import registrate_area_router

registrate_worker_router = Router()

# include
registrate_worker_router.include_routers(
    register_fio_router,
    register_contact_router,
    register_date_of_birth_router,
    registrate_area_router,

)
