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

        if order_info['long_time'] and order_info['long_days'] > 0:
            ll_txt = (f'<u>Это долгосрочный заказ. Его длительность = {order_info['long_time']}</u>\n'
                      f'Учитывайте дату, когда создавался заказ, чтобы понять до какого он числа.')
        elif order_info['long_time'] and order_info['long_days'] == 0:
            ll_txt = f'<u>Это долгосрочный заказ. Его длительность не была определена заказчиком.</u>'
        else:
            ll_txt = f'<u>Это не долгосрочный заказ.</u>'

        await callback.message.answer(
            text=f'📅 <b>Дата заказа: {order_info['date']}</b>\n--------------\n'
                 f'👥 <i>Людей надо</i>:\n{order_info['how_many_ppl']}\n--------------\n'
                 f'🏠 <i>Адрес</i>:\n{order_info['address']}\n--------------\n'
                 f'🔧 <i>Описание работы</i>\n{order_info['work_desc']}\n--------------\n'
                 f'💵 <i>Оплата (руб/час)</i>\n{order_info['payment']}\n--------------\n'
                 f'📞 <i>Телефон для справок</i>\n{order_info['help_phone']}\n--------------\n\n'
                 f'ℹ️ <b>Подробная информация</b>\n'
                 f'🏠 <i>Адрес</i>:\n{order_info['FULL_address']}\n--------------\n'
                 f'🔧 <i>Описание работы</i>:\n{order_info['FULL_work_desc']}\n--------------\n'
                 f'📞 <i>Контактные лица</i>:\n{order_info['FULL_phones']}\n--------------\n'
                 f'📝<i>Доп. информация</i>:\n{order_info['FULL_additional_info']}\n--------------\n\n' + ll_txt,
            parse_mode='HTML',
            reply_markup=await create_kb(order_id, order_info['long_time'])
        )

    except Exception as e:
        logger.error(f'Error in view_order_by_id_handler -> {e}')
