from aiogram.fsm.state import State, StatesGroup


class EditLongDaysStates(StatesGroup):
    order_id = State()
    long_days = State()
