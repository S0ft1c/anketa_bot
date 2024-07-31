from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from .create_order_states import CreateOrderStates
from loguru import logger
from .back_to_zakazhick_btn import back_to_zakazhick_btn

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
            text='<b>Указанный вами адрес сохранен!</b> '
                 '<i>🔨 Теперь введите описание работы</i>\n\n'
                 'Опять же, вы можете указывать краткое содержание, так как позднее вам будет предложено указать '
                 'более подробную информацию про работу.',
            parse_mode='HTML',
            reply_markup=back_to_zakazhick_btn
        )
    except Exception as e:
        logger.error(f'Error in after_address_handler_router -> {e}')
