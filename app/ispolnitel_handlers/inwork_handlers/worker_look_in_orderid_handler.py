from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from sqlite_database import DB

worker_look_in_orderid_router = Router()


async def create_kb(worker_id: str | int, order_id: str | int) -> InlineKeyboardMarkup | None:
    async with DB() as db:
        inwork = await db.select_inwork_by_worker_n_order_id(worker_id, order_id)

        if inwork['start_date'] is None and inwork['end_date'] is None:
            return InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Я приступаю к работе',
                                      callback_data=f'start_work_on_order={order_id}')],
            ])
        elif inwork['start_date'] is not None and inwork['end_date'] is None:
            return InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Я завершил работу',
                                      callback_data=f'end_work_on_order={order_id}')],
            ])
        else:
            return None


@worker_look_in_orderid_router.callback_query(F.data.contains('worker_look_in_orderid'))
async def worker_look_in_orderid_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer('')
        order_id = callback.data.split('=')[-1]

        async with DB() as db:
            order_info = await db.select_order_by_id(order_id)

            if order_info['long_time'] and order_info['long_days'] > 0:
                ll_txt = (f'<u>Это долгосрочный заказ. Его длительность = {order_info['long_days']}</u>\n'
                          f'Учитывайте дату, когда создавался заказ, чтобы понять до какого он числа.')
            elif order_info['long_time'] and order_info['long_days'] == 0:
                ll_txt = f'<u>Это долгосрочный заказ. Его длительность не была определена заказчиком.</u>'
            else:
                ll_txt = f'<u>Это не долгосрочный заказ.</u>'

            await callback.message.answer(
                text=f'📅 <b>Дата заказа: {order_info['date'].replace('.20', '.')}</b>\n--------------\n'
                     f'👥 <i>Людей надо</i>: {order_info['how_many_ppl']}\n--------------\n'
                     f'🏠 <i>Адрес</i>: {order_info['address']}\n--------------\n'
                     f'🔧 <i>Описание работы</i>\n{order_info['work_desc']}\n--------------\n'
                     f'💵 <i>Оплата (руб/час)</i> {order_info['payment']}\n--------------\n'
                     f'📞 <i>Телефон для справок</i>\n{order_info['help_phone']}\n--------------\n\n'
                     f'ℹ️ <b>Подробная информация</b>\n'
                     f'🏠 <i>Адрес</i>:\n{order_info['FULL_address']}\n--------------\n'
                     f'🔧 <i>Описание работы</i>:\n{order_info['FULL_work_desc']}\n--------------\n'
                     f'📞 <i>Контактные лица</i>:\n{order_info['FULL_phones']}\n--------------\n'
                     f'📝<i>Доп. информация</i>:\n{order_info['FULL_additional_info']}\n--------------\n\n' + ll_txt,
                parse_mode='HTML',
                reply_markup=await create_kb(callback.from_user.id, order_id),
            )

    except Exception as e:
        logger.error(f'Error in worker_look_in_orderid_handler: {e}')
