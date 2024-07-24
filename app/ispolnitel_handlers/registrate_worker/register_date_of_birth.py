from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from app.ispolnitel_handlers.registrate_worker.registrate_worker_states import RegistrateWorkerStates
from utils import validate_birth

register_date_of_birth_router = Router()


@register_date_of_birth_router.message(RegistrateWorkerStates.date_of_birth)
async def register_date_of_birth_handler(message: Message, state: FSMContext):
    try:
        if not validate_birth(message.text):
            await message.answer(
                text=f'<b>Регистрация нового исполнителя</b>\n'
                     f'Дата рождения указана некорректно! Попробуйте еще раз.',
                parse_mode='HTML'
            )
        else:
            await state.update_data(date_of_birth=message.text)
            await state.set_state(RegistrateWorkerStates.area_of_residence)

            await message.answer(
                text=f'<b>Регистрация нового исполнителя</b>\n'
                     f'Дата рождения принята! Теперь введите, где вы живете. Хватит просто района.',
                parse_mode='HTML',
            )
    except Exception as e:
        logger.error(f'Error on register_date_of_birth -> {e}')
