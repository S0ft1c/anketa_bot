from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from .create_order_states import CreateOrderStates
from loguru import logger
from .back_to_zakazhick_btn import back_to_zakazhick_btn

after_full_address_router = Router()


@after_full_address_router.message(CreateOrderStates.FULL_address)
async def after_full_address_handler(message: Message, state: FSMContext):
    try:
        await state.update_data(FULL_address=message.text)

        await state.set_state(CreateOrderStates.FULL_work_desc)

        await message.answer(
            text='<b>Указанный адрес сохранен в подробную информацию!</b> '
                 '<i>🔨 Теперь укажите подробное описание работы.</i>\n\n'
                 'Оно должно быть настолько подробным, что прочитав его заказчик будет четко знать, что от '
                 'него требуется.',
            parse_mode='HTML',
            reply_markup=back_to_zakazhick_btn
        )
    except Exception as e:
        logger.error(f'Erro in after_full_address_handler -> {e}')
