from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from loguru import logger

from app.ispolnitel_handlers.registrate_worker.registrate_worker_states import RegistrateWorkerStates

register_fio_router = Router()


@register_fio_router.message(RegistrateWorkerStates.fio)
async def register_fio_handler(message: Message, state: FSMContext):
    try:
        await state.update_data(fio=message.text)
        await state.set_state(RegistrateWorkerStates.contact_number)

        await message.answer(
            text=f'<b>Регистрация нового исполнителя</b>\n'
                 f'Замечательно! Внизу есть кнопка. Вам необходимо нажать ее для того чтобы мы могли получить ваш '
                 f'номер телефона.',
            parse_mode='HTML',
            reply_markup=ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text='Поделиться контактами', request_contact=True)]
            ],
                resize_keyboard=True,
                is_persistent=True,
            )
        )

    except Exception as e:
        logger.error(f'Error in register_fio -> {e}')
