from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from app.ispolnitel_handlers.registrate_worker.registrate_worker_states import RegistrateWorkerStates
from .add_worker_to_db import add_worker_to_db

registrate_area_router = Router()


@registrate_area_router.message(RegistrateWorkerStates.area_of_residence)
async def registrate_area_handler(message: Message, state: FSMContext):
    try:
        await state.update_data(area_of_residence=message.text)
        await message.answer(
            text=f'<b>Прекрасно! Теперь вы зарегистрированы!</b> Можете перейти в свой аккаунт.',
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='В аккаунт исполнителя',
                                      callback_data='ya_ispolnitel')],
            ])
        )

        await add_worker_to_db(
            message.from_user.id,
            message.from_user.username,
            await state.get_data(),
        )
        await state.clear()
    except Exception as e:
        logger.error(f'Error on registrate_area -> {e}')
