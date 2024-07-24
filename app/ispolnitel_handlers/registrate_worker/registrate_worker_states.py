from aiogram.fsm.state import State, StatesGroup


class RegistrateWorkerStates(StatesGroup):
    fio = State()
    contact_number = State()
    date_of_birth = State()
    area_of_residence = State()
