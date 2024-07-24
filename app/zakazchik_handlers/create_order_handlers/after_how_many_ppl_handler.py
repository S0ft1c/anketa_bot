from aiogram import Router
from aiogram.types import Message
from loguru import logger
from .create_order_states import CreateOrderStates
from utils import validate_how_many_ppl
from aiogram.fsm.context import FSMContext

after_how_many_ppl_router = Router()


@after_how_many_ppl_router.message(CreateOrderStates.how_many_ppl)
async def after_how_many_ppl_handler(message: Message, state: FSMContext):
    try:
        if not validate_how_many_ppl(message.text):
            await message.answer(
                text='<b>Создание нового заказа</b>\n\n'
                     'Введенное вами количество людей некорректно! Введите значение еще раз.',
                parse_mode='HTML',
            )
        else:
            # update data
            await state.update_data(how_many_ppl=message.text)
            # update the state
            await state.set_state(CreateOrderStates.address)

            # answer
            await message.answer(
                text='<b>Создание нового заказа</b>\n\n'
                     'Введенное вами количество людей сохранено! Теперь введите адрес места.',
                parse_mode='HTML',
            )

    except Exception as e:
        logger.error(f'Error in after_how_many_ppl_handler -> {e}')
