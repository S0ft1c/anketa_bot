from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from sqlite_database import DB

admin_end_long_project_router = Router()


@admin_end_long_project_router.callback_query(F.data.contains('admin_end_long_project'))
async def admin_end_long_project_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer()
        order_id = callback.data.split('=')[-1]

        async with DB() as db:
            await db.delete_inwork_by_order_id(order_id)
            await db.delete_order_by_order_id(order_id)

        await callback.message.answer(
            text='Долгосрочный проект завершен. Он пропадет из меню для выполнения у всех исполнителей и заказчика.'
        )
    except Exception as e:
        logger.error(f'Error in admin_end_long_project_handler: {e}')
