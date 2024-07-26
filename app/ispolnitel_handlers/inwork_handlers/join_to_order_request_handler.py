from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from sqlite_database import DB

join_order_router = Router()


@join_order_router.callback_query(F.data.contains('join_to_order_request'))
async def join_to_order_request_handler(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer('')
        order_id = callback.data.split('=')[-1]
        async with DB() as db:
            order_info = await db.select_order_by_id(order_id)
            needed_ppl_in_order = order_info['how_many_ppl']
            candidates = await db.select_all_inwork_by_order_id(order_id)

            if len(candidates) < needed_ppl_in_order:  # not enough ppl in order
                lastrowid = await db.insert_inwork(
                    order_id=order_id,
                    worker_id=callback.from_user.id,
                )
                await callback.message.answer(
                    text=f'Вы успешно откликнулись на заказ! Теперь вы можете его найти в меню "Активные заказы".'
                )
            else:  # all ppl founded
                await callback.message.answer(
                    text=f'К сожалению, необходимое количество людей уже нашлось... Спасибо за заинтересованность! '
                         f'Обязательно попробуйте откликнуться на другие заказы!',
                    parse_mode='HTML',
                )

    except Exception as e:
        logger.error(f'Error in join_to_order_request_handler: {e}')
