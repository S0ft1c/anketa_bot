from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from loguru import logger

from sqlite_database import DB

send_to_exact_person_router = Router()


class SendToExactPerson(StatesGroup):
    order_id = State()
    entity = State()


@send_to_exact_person_router.callback_query(F.data.contains('send_to_exact_person'))
async def send_to_exact_person_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await state.clear()
        order_id = callback.data.split('=')[-1]
        await state.update_data(order_id=order_id)
        await state.set_state(SendToExactPerson.entity)

        await callback.message.answer(
            text='Чтобы человек получил приглашение быстрее остальных введите его никнейм в формате\n'
                 '<pre>@username</pre>\n'
                 'Или вы можете отправить id пользователя:\n'
                 '<pre>11111111</pre>',
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='🔙 Назад', callback_data=f'view_order_by_id={order_id}')]
            ])
        )

    except Exception as e:
        logger.error(f'Error in send_to_exact_person_handler: {e}')


@send_to_exact_person_router.message(SendToExactPerson.entity)
async def send_to_exact_person_handler_2(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        order_id = data['order_id']
        try:
            if message.text.startswith('@'):

                async with DB() as db:
                    order = await db.select_order_by_id(order_id=order_id)
                    worker = await db.select_worker_by_username(message.text.replace('@', ''))

            elif message.text[0].isdigit():
                async with DB() as db:
                    order = await db.select_order_by_id(order_id=order_id)
                    worker = {'telegram_id': message.text}

            else:
                await message.answer(
                    text='Видимо вы указали неправильный никнейм (или id) или этого пользователя нет в базе данных.\n'
                         'Попробуйте еще раз.',
                    parse_mode=ParseMode.HTML,
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text='🔙 Назад', callback_data=f'view_order_by_id={order_id}')]
                    ])
                )
                return

            if order['long_time'] and order['long_days'] > 0:
                ll_txt = (f'<u>Это долгосрочный заказ. Его длительность = {order['long_time']}</u>\n'
                          f'Учитывайте дату, когда создавался заказ, чтобы понять до какого он числа.')
            elif order['long_time'] and order['long_days'] == 0:
                ll_txt = f'<u>Это долгосрочный заказ. Его длительность не была определена заказчиком.</u>'
            else:
                ll_txt = f'<u>Это не долгосрочный заказ.</u>'

            await message.bot.send_message(
                chat_id=worker['telegram_id'],
                text=f'<b>Вам доступен новый заказ!</b>\n'
                     f'📅 <b>Дата заказа: {order['date']}</b>\n--------------\n'
                     f'👥 <i>Людей надо</i>:\n{order['how_many_ppl']}\n--------------\n'
                     f'🏠 <i>Адрес</i>:\n{order['address']}\n--------------\n'
                     f'🔧 <i>Описание работы</i>\n{order['work_desc']}\n--------------\n'
                     f'💵 <i>Оплата (руб/час)</i>\n{order['payment']}\n--------------\n'
                     f'📞 <i>Телефон для справок</i>\n{order['help_phone']}\n--------------\n\n' + ll_txt,
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Я приду!',
                                          callback_data=f'join_to_order_request={order['id']}')],
                ])
            )
            await message.answer(
                text='Сообщение успешно отправлено!'
            )

        except Exception as e:
            logger.warning(f'Cannot send message to exact person: {e}')
            await message.answer(
                text='Видимо вы указали неправильный никнейм (или id) или этого пользователя нет в базе данных.\n'
                     'Попробуйте еще раз.',
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='🔙 Назад', callback_data=f'view_order_by_id={order_id}')]
                ])
            )

    except Exception as e:
        logger.error(f'Error in send_to_exact_person_handler_2: {e}')
