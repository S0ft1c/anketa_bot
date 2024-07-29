from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from sqlite_database import DB

admin_view_long_project_router = Router()


@admin_view_long_project_router.callback_query(F.data.contains('admin_view_long_project'))
async def admin_view_long_project_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer()

        order_id = callback.data.split('=')[-1]
        async with DB() as db:
            order_info = await db.select_order_by_id(order_id)
            await callback.message.answer(
                text=f'📅 <b>Заказ от {order_info['date']}</b>\n'
                     f'👥 <i>Людей надо</i>:\n{order_info['how_many_ppl']}\n'
                     f'🏠 <i>Адрес</i>:\n{order_info['address']}\n'
                     f'🔧 <i>Описание работы</i>\n{order_info['work_desc']}\n'
                     f'💵 <i>Оплата (руб/час)</i>\n{order_info['payment']}\n'
                     f'📞 <i>Телефон для справок</i>\n{order_info['help_phone']}\n\n'
                     f'ℹ️ <b>Подробная информация</b>\n'
                     f'🏠 <i>Адрес</i>:\n{order_info['FULL_address']}\n'
                     f'🔧 <i>Описание работы</i>:\n{order_info['FULL_work_desc']}\n'
                     f'📞 <i>Контактные лица</i>:\n{order_info['FULL_phones']}\n'
                     f'📝<i>Доп. информация</i>:\n{order_info['FULL_additional_info']}\n\n'
                     f'{f'<u>Это долгосрочный заказ. => Сроки {order_info['long_days']} дн.</u>' if order_info['long_time']
                     else f'Это не долгосрочный заказ.'}',
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Завершить работу проекта сегодня.',
                                          callback_data=f'admin_end_long_project={order_info['id']}')],
                ])
            )
    except Exception as e:
        logger.error(f'Error in admin_view_long_project_handler: {e}')
