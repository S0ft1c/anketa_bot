from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from sqlite_database import DB
from utils import create_now_time_text
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
                 'В отчете не забудьте указать: кто не пришел, кто опоздал и на сколько, когда работа началась, а '
                 'когда закончилась, какие были нарушения и так далее.',
            parse_mode='HTML',
        )

    except Exception as e:
        logger.error(f'Error in end_order_by_id_handler: {e}')
