from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
from loguru import logger

from sqlite_database import DB

view_order_by_id_router = Router()


async def create_kb(order_id: int | str, is_long: bool):
    builder = InlineKeyboardBuilder()
    if is_long:
        builder.add(
            InlineKeyboardButton(text='Редактировать количество дней', callback_data=f'edit_long_days_in_id={order_id}')
        )
    builder.add(
        InlineKeyboardButton(text='Удалить заказ', callback_data=f'delete_order_by_id={order_id}')
    )
    builder.add(
        InlineKeyboardButton(text='Завершить заказ', callback_data=f'end_order_by_id={order_id}')
    )
    builder.add(
        InlineKeyboardButton(text='🔙 Назад', callback_data='view_my_orders')
    )
    return builder.adjust(1).as_markup()


@view_order_by_id_router.callback_query(F.data.contains('view_order_by_id'))
async def view_order_by_id_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer('')

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
            parse_mode='HTML',
            reply_markup=await create_kb(order_id, order_info['long_time'])
        )

    except Exception as e:
        logger.error(f'Error in view_order_by_id_handler -> {e}')
