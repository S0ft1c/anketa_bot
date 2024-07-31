from aiogram import Router
from aiogram.types import Message
from loguru import logger
from .create_order_states import CreateOrderStates
from utils import validate_how_many_ppl
from aiogram.fsm.context import FSMContext
from .back_to_zakazhick_btn import back_to_zakazhick_btn

after_how_many_ppl_router = Router()


@after_how_many_ppl_router.message(CreateOrderStates.how_many_ppl)
async def after_how_many_ppl_handler(message: Message, state: FSMContext):
    try:
        if not validate_how_many_ppl(message.text):
            await message.answer(
                text='<b>🧑‍🏭 Указание количества людей</b>\n\n'
                     '❌ Введенное вами количество людей некорректно! Введите значение еще раз.',
                parse_mode='HTML',
                reply_markup=back_to_zakazhick_btn
            )
        else:
            # update data
            await state.update_data(how_many_ppl=message.text)
            # update the state
            await state.set_state(CreateOrderStates.address)

            # answer
            await message.answer(
                text='<b>Введенное вами количество людей сохранено!</b> '
                     '<i>🏘 Теперь введите адрес места!</i>\n\n'
                     'Можно указать не весь адрес, а просто район или примерное место.\n'
                     'Позднее вам будет предложено указать точный адрес для тех, кто откликнулся на заказ.',
                parse_mode='HTML',
                reply_markup=back_to_zakazhick_btn
            )

    except Exception as e:
        logger.error(f'Error in after_how_many_ppl_handler -> {e}')
