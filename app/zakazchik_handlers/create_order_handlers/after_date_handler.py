from .create_order_states import CreateOrderStates
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Router
from loguru import logger
from utils import is_valid_datetime

after_date_router = Router()


@after_date_router.message(CreateOrderStates.date)
async def after_date_hander(message: Message, state: FSMContext):
    try:
        if not is_valid_datetime(message.text):
            await message.answer(
                text='<b>Создание нового заказа</b>\n\n'
                     'Введенная вами дата некорректна. Попробуйте еще раз.',
                parse_mode='HTML',
            )
        else:
            # update the info
            await state.update_data(date=message.text)
            # update the StatesGroup
            await state.set_state(CreateOrderStates.how_many_ppl)

            # answer
            await message.answer(
                text='<b>Создание нового заказа</b>\n\n'
                     'Отправленная вами дата сохранена! Теперь введите, сколько людей вам надо для работы',
                parse_mode='HTML',
            )
    except Exception as e:
        logger.error(f'Error in after_date_handler -> {e}')
