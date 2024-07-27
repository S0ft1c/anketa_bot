from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from sqlite_database import DB

delete_order_by_id_router = Router()


@delete_order_by_id_router.callback_query(F.data.contains('delete_order_by_id'))
async def delete_order_by_id_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()

        order_id = callback.data.split('=')[-1]
        async with DB() as db:
            await db.delete_order_by_order_id(order_id)

        await callback.answer('')
        await callback.message.answer(
            text='Заказ был успешно удален!',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='🔙 Назад', callback_data='view_my_orders')]
            ])
        )
    except Exception as e:
        logger.error(f'Error in delete_order_by_id -> {e}')
