from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from sqlite_database import DB
from utils import create_now_time_text

end_work_on_order_router = Router()


@end_work_on_order_router.callback_query(F.data.contains('end_work_on_order'))
async def end_work_on_order_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer('')

        order_id = callback.data.split('=')[-1]

        async with DB() as db:
            lastrowid = await db.update_end_date_inwork(
                worker_id=callback.from_user.id,
                order_id=order_id,
                end_time=await create_now_time_text(),
            )

        await callback.message.answer(
            text='<b>Вы завершили работу над заказом.</b>\n'
                 'Как только заказчик подтвердит у себя, что его заказ завершен, он пропадет у вас из '
                 '"Активных заказов"',
            parse_mode='HTML',
        )

    except Exception as e:
        logger.error(f'Error in end_work_on_order_handler: {e}')
