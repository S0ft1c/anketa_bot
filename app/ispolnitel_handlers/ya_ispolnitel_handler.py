from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from app.ispolnitel_handlers.registrate_worker.registrate_worker_states import RegistrateWorkerStates
from sqlite_database import DB

ya_ispolnitel_router = Router()


@ya_ispolnitel_router.callback_query(F.data.contains('ya_ispolnitel'))
async def ya_ispolnitel_menu(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await callback.answer('')
        async with DB() as db:
            worker = await db.get_worker_by_tg_id(callback.from_user.id)

        if not worker:
            await callback.message.answer(
                text=f'<b>Вы новый исполнитель!</b>\n'
                     f'Давайте зарегистрируем вас. Для того чтобы работать с нами надо указать некоторые свои данные.\n'
                     f'Для начала укажите своё ФИО',
                parse_mode='HTML',
            )
            await state.set_state(RegistrateWorkerStates.fio)
        else:
            await callback.message.answer(
                text=f'<b>Вы зашли как исполнитель</b>\n'
                     f'Выберите интересующее вас действие.',
                parse_mode='HTML',
            )

    except Exception as e:
        logger.error(f'Error in ya_ispolnitel_menu -> {e}')
