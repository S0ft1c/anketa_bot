from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from .to_excel_all_workers_func import to_excel_all_workers_func

to_excel_all_workers_router = Router()


@to_excel_all_workers_router.callback_query(F.data.contains('to_excel_all_workers'))
async def to_excel_all_workers_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer()

        await to_excel_all_workers_func(
            bot=callback.bot,
            chat_id=callback.from_user.id,
        )

    except Exception as e:
        logger.error(f'Error in to_excel_all_workers: {e}')
