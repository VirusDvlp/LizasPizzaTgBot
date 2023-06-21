from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import db
from config import pizza_sizes, size_prices


def get_basket_kb(user_id: int, page: int) -> InlineKeyboardMarkup:
    basket_kb = InlineKeyboardMarkup(row_width=5)
    user_pizzas = db.get_basket(user_id)
    if not user_pizzas:         # If basket is empty, bot will show button 'go to menu'
        return(InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton('В\tкорзине\tпусто', callback_data='menu'), 
            InlineKeyboardButton('Просмотреть\tменю', callback_data='menu')
                ))
    user_pizzas = user_pizzas.split(',') 
    uniq_pizzas = list(set(user_pizzas))
    total = 0
    number = len(user_pizzas)
    if len(uniq_pizzas) < 5:
        for item in uniq_pizzas:
            pizza = item.split('*')
            try:
                pizza_name = f"{db.get_pizza_name(pizza[0])} {pizza_sizes[pizza[-1]]}"
            except TypeError:
                 continue
            pizza_n = user_pizzas.count(item)
            price = int(db.get_pizza_price(pizza[0]) * size_prices[pizza[-1]]) * pizza_n
            total += price 
            pizza_bt = InlineKeyboardButton(pizza_name, callback_data=1)
            buttons = (
                InlineKeyboardButton('➕', callback_data=f"add_{item}"),
                InlineKeyboardButton(pizza_n, callback_data=' '),
                InlineKeyboardButton('➖', callback_data=f"del_{item}"),
                InlineKeyboardButton('❌', callback_data=f"kill_{item}"),
                InlineKeyboardButton(f'{price}\tруб', callback_data=price)
            )
            basket_kb.add(pizza_bt)
            basket_kb.add(*buttons)
    else:
        for item in uniq_pizzas[page*5 : page*5 + 5]:
            pizza = item.split('*')
            try:
                pizza_name = f"{db.get_pizza_name(pizza[0])} {pizza_sizes[pizza[-1]]}"
            except TypeError:
                 continue
            pizza_n = user_pizzas.count(item)
            price = int(db.get_pizza_price(pizza[0]) * size_prices[pizza[-1]]) * pizza_n
            total += price
            pizza_bt = InlineKeyboardButton(pizza_name, callback_data=1)
            buttons = (
                InlineKeyboardButton('➕', callback_data=f"add_{item}"),
                InlineKeyboardButton(pizza_n, callback_data=123),
                InlineKeyboardButton('➖', callback_data=f"del_{item}"),
                InlineKeyboardButton('❌', callback_data=f"kill_{item}"),
                InlineKeyboardButton(f'{price}\tруб', callback_data=price)
            )
            basket_kb.add(pizza_bt)
            basket_kb.add(*buttons)
        if page > 0:
            previous_bt = InlineKeyboardButton('⬅️', callback_data='prev')
            basket_kb.insert(previous_bt)
        if page < len(uniq_pizzas) // 5:
            next_bt = InlineKeyboardButton('➡️', callback_data='next')
            basket_kb.insert(next_bt)
    menu_bt = InlineKeyboardButton('ВЕРНУТЬСЯ\tВ\tМЕНЮ', callback_data='menu') #button 'go to menu'
    order_bt = InlineKeyboardButton('ОФОРМЛЕНИЕ\tЗАКАЗА', callback_data=f'order_{total}') #button 'make order'
    n_bt = InlineKeyboardButton(f'Товаров\tв\tкорзине: {number}', callback_data=f'b{number}')
    total_bt = InlineKeyboardButton(f'ИТОГО: {total} руб.', callback_data=f'b{total}\tруб.')
    basket_kb.add(n_bt, total_bt)
    basket_kb.add(menu_bt, order_bt)
    return basket_kb
