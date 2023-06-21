from aiogram.dispatcher.filters.state import StatesGroup, State

class BasketFSM(StatesGroup):
    edit_basket_state = State()
    adress_state = State()
    home_adress_state = State()
    get_home_adress_state = State()
    get_shop_adress_state = State()
    payment_type_state = State()
    invoice_state = State()