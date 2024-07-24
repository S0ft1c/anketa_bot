from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from .create_order_states import CreateOrderStates
from loguru import logger

after_address_handler_router = Router()


@after_address_handler_router.message(CreateOrderStates.address)
async def after_address_handler(message: Message, state: FSMContext):
    try:
        # update data
        await state.update_data(address=message.text)
        # set new state
        await state.set_state(CreateOrderStates.work_desc)

        # answer
        await message.answer(
            text='<b>Создание нового заказа</b>\n\n'
                 'Указанный вами адрес сохранен! Теперь введите описание специфики работы.',
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error(f'Error in after_address_handler_router -> {e}')
