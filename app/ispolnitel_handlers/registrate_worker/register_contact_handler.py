from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from loguru import logger

from app.ispolnitel_handlers.registrate_worker.registrate_worker_states import RegistrateWorkerStates

register_contact_router = Router()


@register_contact_router.message(F.contact, RegistrateWorkerStates.contact_number)
async def register_contact_handler(message: Message, state: FSMContext):
    try:

        await state.update_data(contact_number=message.contact.phone_number)
        await state.set_state(RegistrateWorkerStates.date_of_birth)

        await message.answer(
            text=f'<b>Регистрация нового исполнителя</b>\n'
                 f'Ваш номер телефона принят! Теперь введите свою дату рождения в формате:\n'
                 f'<pre>день.месяц.год</pre>\nНапример: 01.04.2022',
            parse_mode='HTML',
            reply_markup=ReplyKeyboardRemove(),
        )

    except Exception as e:
        logger.error(f'Error in register_contact_handler -> {e}')
