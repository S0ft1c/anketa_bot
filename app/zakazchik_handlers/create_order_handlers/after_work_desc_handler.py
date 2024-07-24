from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from .create_order_states import CreateOrderStates
from loguru import logger

after_work_desc_router = Router()


@after_work_desc_router.message(CreateOrderStates.work_desc)
async def after_work_desc_handler(message: Message, state: FSMContext):
    try:
        # update data
        await state.update_data(work_desc=message.text)
        # set the state
        await state.set_state(CreateOrderStates.payment)

        # answer
        await message.answer(
            text='<b>Создание нового заказа</b>\n\n'
                 'Специфика работы сохранена! Теперь введите какую оплату (в руб.) получат исполнители.',
            parse_mode='HTML',
        )
    except Exception as e:
        logger.error(f'Error in after_work_desc_handler -> {e}')
