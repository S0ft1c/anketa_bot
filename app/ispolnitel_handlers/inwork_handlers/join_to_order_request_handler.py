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

            worker = await db.get_worker_by_tg_id(callback.from_user.id)
            if not worker:
                await callback.message.answer(
                    text='Вы не зарегистрированы как исполнитель.\n'
                         'Напишите /start после выберите, что вы исполнитель и пройдите регистрацию.\n'
                         'После регистрации попробуйте еще раз.'
                )
                return

            possible_inwork = await db.select_inwork_by_worker_n_order_id(callback.from_user.id, order_id)
            if possible_inwork:
                await callback.message.answer(
                    text='Вы уже согласились на этот заказ!',
                )
                return

            order_info = await db.select_order_by_id(order_id)

            if str(order_info['customer_id']) == str(callback.from_user.id):
                await callback.message.answer(
                    text='Вы сами создали этот заказ. Вы не можете стать его исполнителем.'
                )
                return

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
