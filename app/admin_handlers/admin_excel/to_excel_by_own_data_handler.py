from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from loguru import logger

from utils import validate_excel_date
from .get_all_data_to_excel_func import get_all_data_to_excel

to_excel_by_own_data_router = Router()


class MyOwnExcelStates(StatesGroup):
    start_date = State()
    end_date = State()


@to_excel_by_own_data_router.callback_query(F.data.contains('to_excel_by_own_data'))
async def to_excel_by_own_data_handler_1(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer()

        await state.set_state(MyOwnExcelStates.start_date)
        await callback.message.answer(
            text='Введите дату с которой надо начать выгрузку.\n'
                 'Дата должна быть формата: дд.мм.гггг\n'
                 'Например: 01.07.2024',
        )

    except Exception as e:
        logger.error(f'Error in to_excel_by_own_data_handler: {e}')


@to_excel_by_own_data_router.message(MyOwnExcelStates.start_date)
async def to_excel_by_own_data_handler_2(message: Message, state: FSMContext):
    try:
        if validate_excel_date(message.text):
            await state.update_data(start_date=message.text)
            await state.set_state(MyOwnExcelStates.end_date)
            await message.answer(
                text='Прекрасно! Теперь введите дату (такого же формата) до которой надо взять все данные.\n'
                     '<i>Обратите внимание, что дата будет браться НЕ включительно. То есть если вы введете 25.07.2024 '
                     'данных от 25.07.2024 числа в выгрузке <b>не будет</b></i>',
                parse_mode=ParseMode.HTML,
            )
        else:
            await message.answer(
                text='Вы ввели неверный формат даты. Попробуйте еще раз.'
            )
    except Exception as e:
        logger.error(f'Error in to_excel_by_own_data_handler: {e}')


@to_excel_by_own_data_router.message(MyOwnExcelStates.end_date)
async def to_excel_by_own_data_handler_3(message: Message, state: FSMContext):
    try:

        if validate_excel_date(message.text):
            await state.update_data(end_date=message.text)
            data = await state.get_data()
            start_date = data['start_date']
            end_date = data['end_date']

            await get_all_data_to_excel(
                bot=message.bot,
                chat_id=message.from_user.id,
                start_date=start_date,
                end_date=end_date,
            )

        else:
            await message.answer(
                text='Вы ввели неверный формат даты. Попробуйте еще раз.'
            )

    except Exception as e:
        logger.error(f'Error in to_excel_by_own_data_handler: {e}')
