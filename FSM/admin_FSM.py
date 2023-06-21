from aiogram.dispatcher.filters.state import State, StatesGroup

class NewPizzaFSM(StatesGroup):
    name_state = State()
    descr_state = State()
    price_state = State()
    image_state = State()


class RedactPizzaFSM(StatesGroup):
    pizza_state = State()
    what_state = State()
    change_state = State()


class MailingFSM(StatesGroup):
    photo_state = State()
    text_state = State()
    add_button_state = State()
    button_text_state = State()
    button_url_state = State()


class MainAdminFSM(StatesGroup):
    admin_state = State()
