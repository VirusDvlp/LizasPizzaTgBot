from aiogram.dispatcher.filters.state import StatesGroup, State

class MenuFSM(StatesGroup):
    size_state = State()
    finish_state = State()