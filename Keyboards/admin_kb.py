from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import db


def get_choice_change_kb() -> ReplyKeyboardMarkup:
    choice_change_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    add_pizza_bt = KeyboardButton('ДОБАВИТЬ\tПИЦЦУ➕')
    change_pizza_bt = KeyboardButton('ИЗМЕНИТЬ\tПАРАМЕТРЫ\tПИЦЦЫ📝')
    mailing_bt = KeyboardButton('СОЗДАТЬ\tРАССЫЛКУ\tПОЛЬЗОВАТЕЛЯМ✉️')
    exit_bt = KeyboardButton('ВЫЙТИ\tИЗ\tРЕЖИМА\tАДМИНИСТРТАТОРА🔙')
    return choice_change_kb.add(add_pizza_bt, change_pizza_bt, mailing_bt, exit_bt)


def get_pizza_list_kb() -> InlineKeyboardMarkup:
    pizza_list_kb = InlineKeyboardMarkup(row_width=2)
    for pizza in db.get_pizza_names():
        pizza_list_kb.add(InlineKeyboardButton(pizza[1], callback_data=pizza[0]))
    return pizza_list_kb


def get_what_change_kb() -> InlineKeyboardMarkup:
    what_change_kb = InlineKeyboardMarkup(1)
    name_bt = InlineKeyboardButton('НАЗВАНИЕ', callback_data='name')
    price_bt = InlineKeyboardButton('ЦЕНА', callback_data='price')
    descr_bt = InlineKeyboardButton('ОПИСАНИЕ', callback_data='descr')
    image_bt = InlineKeyboardButton('ИЗОБРАЖЕНИЕ', callback_data='image')
    return what_change_kb.add(name_bt, price_bt, descr_bt, image_bt)


def get_cancel_kb(input_data: str) -> ReplyKeyboardMarkup:
    cancel_bt = KeyboardButton(f'ОТМЕНИТЬ\t{input_data}✖️')
    mailing_kb = ReplyKeyboardMarkup().add(cancel_bt)
    return mailing_kb   


def get_add_bt_kb() -> InlineKeyboardMarkup:
    add_bt = InlineKeyboardButton('ДОБАВИТЬ КНОПКУ', callback_data='add_bt')
    send_bt = InlineKeyboardButton('ОТПРАВИТЬ РАССЫЛКУ', callback_data='send')
    return InlineKeyboardMarkup(1).add(add_bt, send_bt)
