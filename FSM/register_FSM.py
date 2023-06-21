from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterStates(StatesGroup):
    email_state = State()
    date_state = State()
    location_state = State()


class UserSettingsFSM(StatesGroup):
    what_state = State()
    email_state = State()
    location_state = State()