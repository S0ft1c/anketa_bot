from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from .create_order_states import CreateOrderStates
from loguru import logger
from .back_to_zakazhick_btn import back_to_zakazhick_btn

after_full_work_desc_router = Router()


@after_full_work_desc_router.message(CreateOrderStates.FULL_work_desc)
async def after_full_work_desc_handler(message: Message, state: FSMContext):
    try:
        await state.update_data(FULL_work_desc=message.text)
        await state.set_state(CreateOrderStates.FULL_phones)

        await message.answer(
            text='<b>Указанное вами описание работы сохранено в подробную информацию!</b> '
                 '<i>Теперь укажите все контактные лица</i>\n\n'
                 'Все люди, с которыми исполнителю надо будет связаться для выполнения заказа, должны быть указаны '
                 'тут.',
            parse_mode='HTML',
            reply_markup=back_to_zakazhick_btn
        )

    except Exception as e:
        logger.error(f'Error in after_full_work_desc -> {e}')
