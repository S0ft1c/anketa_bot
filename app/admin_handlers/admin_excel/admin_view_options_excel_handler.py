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
                [InlineKeyboardButton(text='Выгрузить по своим датам.',
                                      callback_data='to_excel_by_own_data')]
            ])
        )

    except Exception as e:
        logger.error(f'Error in admin_view_options_excel: {e}')
