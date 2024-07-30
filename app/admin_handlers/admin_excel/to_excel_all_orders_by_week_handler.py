from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from .to_excel_by_week_handler import get_previous_friday, get_upcoming_friday
from .to_excel_orders_func import to_excel_orders_func

to_excel_all_orders_by_week_router = Router()


@to_excel_all_orders_by_week_router.callback_query(F.data.contains('to_excel_all_orders_by_week'))
async def to_excel_all_orders_by_week_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer()

        await to_excel_orders_func(
            bot=callback.bot,
            chat_id=callback.from_user.id,
            start_date=get_previous_friday(),
            end_date=get_upcoming_friday(),
        )

    except Exception as e:
        logger.error(f'Error in to_excel_all_orders_by_week_handler: {e}')
