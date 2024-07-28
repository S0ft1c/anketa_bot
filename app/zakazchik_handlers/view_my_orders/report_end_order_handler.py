from datetime import datetime, timedelta
from random import randint

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from apscheduler.triggers.date import DateTrigger
from loguru import logger

from schedulers import scheduler, repeat_long_time_order
from sqlite_database import DB
from utils import create_now_time_text
from .end_order_states import EndOrderStates

report_end_order_router = Router()


def get_next_day_7am():
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    return tomorrow.replace(hour=7, minute=randint(0, 59), second=0, microsecond=0)


@report_end_order_router.message(EndOrderStates.report)
async def report_end_order_handler(message: Message, state: FSMContext):
    try:
        await state.update_data(report=message.text)
        data = await state.get_data()
        order_id, report = data['order_id'], data['report']

        # do all the end dates for all workers in order
        async with DB() as db:
            inworks = await db.select_all_inwork_by_order_id(order_id)
            for inwork in inworks:
                if inwork['end_date'] is None:
                    await db.update_end_date_inwork(
                        inwork['worker_id'],
                        inwork['order_id'],
                        await create_now_time_text()
                    )

        async with DB() as db:
            inworks = await db.select_all_inwork_by_order_id(order_id)
            order_info = await db.select_order_by_id(order_id)
            workers_ids = []
            for inwork in inworks:
                lastrowid = await db.insert_admin_review(
                    customer_id=message.from_user.id,
                    worker_id=inwork['worker_id'],
                    date=order_info['date'],
                    how_many_ppl=order_info['how_many_ppl'],
                    address=order_info['address'],
                    work_desc=order_info['work_desc'],
                    payment=order_info['payment'],
                    help_phone=order_info['help_phone'],
                    full_address=order_info['FULL_address'],
                    full_work_desc=order_info['FULL_work_desc'],
                    full_phones=order_info['FULL_phones'],
                    full_additional_info=order_info['FULL_additional_info'],
                    long_time=order_info['long_time'],
                    long_days=order_info['long_days'],
                    report=report,
                    start_date=inwork['start_date'],
                    end_date=inwork['end_date'],
                )
                if not lastrowid:
                    logger.warning('smth wrong')
                if order_info['long_time'] and \
                        (
                                datetime.date((datetime.strptime(order_info['date'], '%H:%M %d.%m.%Y')
                                               + timedelta(days=order_info['long_days']))) > datetime.now().date() or
                                order_info['long_days'] == 0
                        ):
                    workers_ids.append(inwork['worker_id'])
            if workers_ids:
                scheduler.add_job(
                    func=repeat_long_time_order,
                    trigger=DateTrigger(run_date=get_next_day_7am()),
                    kwargs={
                        'bot': message.bot,
                        'customer_id': message.from_user.id,
                        'workers_ids': workers_ids,
                        'date': order_info['date'],
                        'how_many_ppl': order_info['how_many_ppl'],
                        'address': order_info['address'],
                        'work_desc': order_info['work_desc'],
                        'payment': order_info['payment'],
                        'help_phone': order_info['help_phone'],
                        'full_address': order_info['FULL_address'],
                        'full_work_desc': order_info['FULL_work_desc'],
                        'full_phones': order_info['FULL_phones'],
                        'full_additional_info': order_info['FULL_additional_info'],
                        'long_time': order_info['long_time'],
                        'long_days': order_info['long_days'],
                    }
                )

        # delete all noneeded info
        async with DB() as db:
            await db.delete_inwork_by_order_id(order_id)
            await db.delete_order_by_order_id(order_id)

        await message.answer(
            text='Отчет успешно отправлен! Спасибо!'
        )
        await state.clear()

    except Exception as e:
        logger.error(f'Error in report_end_order_handler: {e}')
