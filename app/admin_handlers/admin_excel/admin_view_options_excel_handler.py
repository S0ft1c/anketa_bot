from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

admin_view_options_excel_router = Router()


@admin_view_options_excel_router.callback_query(F.data.contains('admin_view_options_excel'))
async def admin_view_options_excel_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await state.clear()

        await callback.message.answer(
            text='Выберите, какие данные вы хотите получить',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Выгрузить исполнителей по своим датам',
                                      callback_data='to_excel_by_own_data')],
                [InlineKeyboardButton(text='Выгрузить исполнителей по неделе',
                                      callback_data='to_excel_by_week')],
                [InlineKeyboardButton(text='Выгрузить заказы по своим датам',
                                      callback_data='to_excel_all_orders_by_own_data')],
                [InlineKeyboardButton(text='Выгрузить заказы по неделе',
                                      callback_data='to_excel_all_orders_by_week')],
                [InlineKeyboardButton(text='Выгрузить информацию по исполнителям',
                                      callback_data='to_excel_all_workers')],
            ])
        )

    except Exception as e:
        logger.error(f'Error in admin_view_options_excel: {e}')
