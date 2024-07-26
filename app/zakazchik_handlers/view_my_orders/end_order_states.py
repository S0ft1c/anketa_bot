from aiogram.fsm.state import StatesGroup, State


class EndOrderStates(StatesGroup):
    order_id = State()
    report = State()
