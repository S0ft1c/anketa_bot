from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger
from sqlite_database import DB

callback_start_router = Router()


@callback_start_router.message(CommandStart(deep_link=True))
async def group_callback_start_handler(message: Message, command: CommandObject, state: FSMContext):
    try:
        await state.clear()
        order_id = command.args

        async with DB() as db:
            order = await db.select_order_by_id(order_id)

        await message.answer(
            text=f'<b>Вам доступен новый заказ!</b>\n'
                 f'Дата: {order['date']}\n'
                 f'Требуется людей: {order['how_many_ppl']}\n'
                 f'Адрес: {order['address']}\n'
                 f'Описание работы:\n{order['work_desc']}\n'
                 f'Оплата (руб/час): {order['payment']}\n'
                 f'Телефон для справок: {order['help_phone']}\n'
                 f'{f'<u>Это долгосрочный заказ. => Сроки {order['long_days']} дн.</u>' if order['long_time']
                 else f'Это не долгосрочный заказ.'}',
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Я приду!',
                                      callback_data=f'join_to_order_request={order['id']}')],
            ])
        )

    except Exception as e:
        logger.error(f'Error in group_callback_start_handler: {e}')
