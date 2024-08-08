from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from .end_order_states import EndOrderStates

end_order_by_id_router = Router()


@end_order_by_id_router.callback_query(F.data.contains('end_order_by_id'))
async def end_order_by_id_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer('')
        order_id = callback.data.split('=')[-1]

        await state.update_data(order_id=order_id)
        await state.set_state(EndOrderStates.report)

        await callback.message.answer(
            text='<b>Введите отчет по исполнителям</b>\n'
                 'Напишите отчет по исполнителям, который поможет нам определить добросовестность их работы. '
                 'В отчете укажите кто прибыл на работу, а также кто и сколько часов отработали.\n'
                 'Указать отчет можно в свободной форме. Пример:\n'
                 'Иван Пупкин пришел на работу, работал 3 часа. Алексей Папкин пришел на работу, работал 2 часа. '
                 'Павел Пакин не пришел на работу, плохой работник.',
            parse_mode='HTML',
        )

    except Exception as e:
        logger.error(f'Error in end_order_by_id_handler: {e}')
