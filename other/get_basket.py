from create_bot import db
from config import pizza_sizes


def get_basket(pizzas: str) -> dict:
    pizzas = pizzas.split(',')
    uniq_pizzas = list(set(pizzas))
    basket = {}
    for item in uniq_pizzas:
            pizza = item.split('*')
            print(pizza)
            try:
                pizza_name = f"{db.get_pizza_name(pizza[0])} {pizza_sizes[pizza[-1]]}"
            except TypeError:
                 continue

            pizza_n = pizzas.count(item)
            basket[pizza_name] = pizza_n
    return basket