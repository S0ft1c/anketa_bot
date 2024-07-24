from aiogram.fsm.state import State, StatesGroup


class CreateOrderStates(StatesGroup):
    date = State()
    how_many_ppl = State()
    address = State()
    work_desc = State()
    payment = State()
    help_phone = State()
    FULL_address = State()
    FULL_work_desc = State()
    FULL_phones = State()
    FULL_additional_info = State()
    long_time = State()
    long_days = State()
