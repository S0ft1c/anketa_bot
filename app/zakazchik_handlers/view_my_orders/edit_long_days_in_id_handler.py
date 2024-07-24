from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from loguru import logger
from aiogram.fsm.context import FSMContext
from sqlite_database import DB
from .edit_long_days_states import EditLongDaysStates
from utils import validate_long_days

edit_long_days_in_id_router = Router()


async def create_kb(order_id: int | str):
    back_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔙 Назад', callback_data=f'view_order_by_id={order_id}')]
    ])
    return back_kb


@edit_long_days_in_id_router.callback_query(F.data.contains('edit_long_days_in_id'))
async def edit_long_days_in_id_handler(callback: CallbackQuery, state: FSMContext):
    try:
        order_id = callback.data.split('=')[-1]
        await state.clear()
        await state.update_data(order_id=order_id)
        await state.set_state(EditLongDaysStates.long_days)
        await callback.answer('')

        await callback.message.answer(
            text=f'<b>Редактирование количество дней в долгосрочном заказе</b>\n'
                 f'Укажите новое число, которое будет указывать на количество дней в заказе. '
                 f'Вы можете указать 0 и тогда заказ будет активен, пока его не закроет администратор.',
            parse_mode='HTML',
            reply_markup=await create_kb(order_id),
        )

    except Exception as e:
        logger.error(f'Error in edit_long_days_in_id_handler -> {e}')


@edit_long_days_in_id_router.message(EditLongDaysStates.long_days)
async def edit_long_days_in_id_handler_2(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        order_id = data['order_id']
        if not validate_long_days(message.text):
            await message.answer(
                text=f'<b>Редактирование количество дней в долгосрочном заказе</b>\n'
                     f'Введенное вами значение некорректно. Попробуйте еще раз.',
                parse_mode='HTML',
                reply_markup=await create_kb(order_id)
            )
        else:
            await state.clear()
            async with DB() as db:
                await db.update_long_days_in_order_by_id(order_id, int(message.text))

            await message.answer(
                text=f'<b>Редактирование количество дней в долгосрочном заказе завершено!</b>\n'
                     f'Количество дней обновлено.',
                parse_mode='HTML',
                reply_markup=await create_kb(order_id),
            )

    except Exception as e:
        logger.error(f'Error in edit_long_days_in_id_handler_2 -> {e}')
