from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from .create_order_states import CreateOrderStates
from loguru import logger
from utils import validate_long_days
from .add_order_to_db import add_order_to_db

long_day_router = Router()


@long_day_router.message(CreateOrderStates.long_days)
async def yes_long_time(message: Message, state: FSMContext):
    try:
        if not validate_long_days(message.text):
            await message.answer(
                text='<b>Создание долгосрочного заказа заказа.</b>'
                     'Введенное ваши число некорректно. Попробуйте еще раз.',
                parse_mode='HTML',
            )
        else:
            await state.update_data(long_days=int(message.text))
            await message.answer(
                text='<b>Создание долгосрочного заказа завершено!</b>'
                     'Вы можете увидеть его в разделе "Мои заказы"',
                parse_mode='HTML',
            )

            await add_order_to_db(
                str(message.from_user.id),
                await state.get_data()
            )
            await state.clear()
    except Exception as e:
        logger.error(f'Error in yes_long_time -> {e}')
