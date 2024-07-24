from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger

ya_zakazchik_router = Router()


@ya_zakazchik_router.callback_query(F.data.contains('ya_zakazchik'))
async def ya_zakazchik_callback_handler(callback: CallbackQuery):
    try:
        await callback.answer('')
        await callback.message.answer(
            text='<b>Вы - заказчик.</b>\n'
                 'Выберите действие, которое вас интересует.',
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Создать заказ', callback_data='create_order'),
                 InlineKeyboardButton(text='Посмотреть свои заказы', callback_data='view_my_orders')]
            ])
        )
    except Exception as e:
        logger.error(f'Error in ya_zakazchik_callback_handler! -> {e}')
