from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_pizza_kb(callback) -> InlineKeyboardMarkup:
    basket_bt = InlineKeyboardButton(text='ДОБАВИТЬ\tВ\tКОРЗИНУ', callback_data=callback)
    menu_kb = InlineKeyboardMarkup().add(basket_bt)
    return menu_kb


def get_size_kb() -> InlineKeyboardMarkup:
    small = InlineKeyboardButton(text='Маленькая', callback_data='1')
    medium = InlineKeyboardButton(text='Средняя', callback_data='2')
    big = InlineKeyboardButton(text='Большая', callback_data='3')
    size_kb = InlineKeyboardMarkup().insert(small).insert(medium).insert(big)
    return size_kb
