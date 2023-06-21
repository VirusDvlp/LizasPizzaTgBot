from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def get_order_type_kb() -> InlineKeyboardMarkup:
    order_type_kb = InlineKeyboardMarkup(1)
    home_bt = InlineKeyboardButton('ДОСТАВКА\tНА\tДОМ', callback_data='1')
    shop_bt = InlineKeyboardButton('В\tЗАВЕДЕНИИ', callback_data='2')
    order_type_kb.add(home_bt, shop_bt)
    return order_type_kb

def get_spec_adress_kb() -> InlineKeyboardMarkup:
    spec_adress_kb = InlineKeyboardMarkup(1)
    this_bt = InlineKeyboardButton('ЭТОТ\tАДРЕС', callback_data='1')
    another_bt = InlineKeyboardButton('ДРУГОЙ', callback_data='2')
    spec_adress_kb.add(this_bt, another_bt)
    return spec_adress_kb


def get_shop_adress_kb() -> InlineKeyboardMarkup:
    shop_adress_kb = InlineKeyboardMarkup(1)
    shop_bt_1 = InlineKeyboardButton('Шашлычная\t23б', callback_data='1')
    shop_bt_2 = InlineKeyboardButton('Бархатная\t10', callback_data='2')
    shop_adress_kb.add(shop_bt_1, shop_bt_2)
    return shop_adress_kb


def get_payment_type_kb(order_type: int) -> InlineKeyboardMarkup:
    payment_type_kb = InlineKeyboardMarkup(1)
    online_pay_bt = InlineKeyboardButton('ОПЛАТА\tОНЛАЙН', callback_data='1')
    payment_type_kb.add(online_pay_bt)
    if order_type == 1:
        cour_pay_bt = InlineKeyboardButton('ОПЛАТА\tКУРЬЕРУ', callback_data='2')
        payment_type_kb.add(cour_pay_bt)
    else:
        shop_pay_bt = InlineKeyboardButton('ОПЛАТА\tВ\tЗАВЕДЕНИИ', callback_data='3')
        payment_type_kb.add(shop_pay_bt)
    return payment_type_kb


def get_online_payments_kb() -> InlineKeyboardMarkup:
    online_payments_kb = InlineKeyboardMarkup(1)
    sber_bt = InlineKeyboardButton('СБЕРБАНК', callback_data='sber')
    paymaster_bt = InlineKeyboardButton('PAYMASTER', callback_data='paymaster')
    online_payments_kb.add(sber_bt, paymaster_bt)
    return online_payments_kb

def get_finish_order_kb() -> ReplyKeyboardMarkup:
    finish_bt = KeyboardButton('ВЫЙТИ\tИЗ\tКОРЗИНЫ🔙')
    finish_order_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(finish_bt)
    return finish_order_kb
