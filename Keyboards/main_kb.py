from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_ID


def get_main_kb(user_id: int) -> ReplyKeyboardMarkup:
    menu_bt = KeyboardButton(text='МЕНЮ📋')
    order_bt = KeyboardButton(text='СДЕЛАТЬ\tЗАКАЗ🛒')
    setting_bt = KeyboardButton(text='ИЗМЕНИТЬ\tПАРАМЕТРЫ\tПРОФИЛЯ⚙️')

    main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(menu_bt, order_bt).add(setting_bt)
    if user_id == ADMIN_ID:
        main_kb.add(KeyboardButton('АДМИН-ПАНЕЛЬ💻'))
    return main_kb


def get_user_settings_kb() -> InlineKeyboardMarkup:
    email_bt = InlineKeyboardButton('ПОЧТА', callback_data='email')
    address_bt = InlineKeyboardButton('АДРЕС\tДОСТАВКИ', callback_data='address')
    return InlineKeyboardMarkup(1).add(email_bt, address_bt)
