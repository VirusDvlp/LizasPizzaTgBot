def get_pizza_text(name, price, descr) -> str:
        text = f"{name} - <b>{price}₽</b>\n\n{descr}"
        return text


def get_invoice_descr(is_shipping, total: int, ship=100) -> str:
        ship_txt = '\nДоставка - 100 руб.' if is_shipping else ''
        text = f'Корзина - {total} руб.{ship_txt}'
        return text


def get_final_order_message_1(payment_type: str, total: int, shop_adress='') -> str:
        order_type = f'''\nВы сможете забрать и оплатить заказ в нашей пиццерии
по адресу {shop_adress}''' if payment_type == '3' else '''\nДоставка - 100 руб.\nКурьер приедет
в течении получаса, после уведомления о готовности заказа. Оплата по прибытию курьера''' 
        text = f'Ваш заказ принят.Чек:\nКорзина - {total}руб{order_type}\nМы будем уведомлять вас о состоянии вашего заказа.\nОстались вопросы или возникли проблемы? - lizzaspizza@gmail.com'
        return text 


def get_final_order_message_2(shop_address, order_type) -> str:
        otype = f'''Вы сможете забрать свой заказ 
в нашей пиццерии по адресу {shop_address}''' if order_type == '1' else '''Курьер приедет
в течении получаса, после уведомления о готовности заказа.'''
        text = f'''Ваш заказ оплачен и принят.{otype}\n
        Мы будем уведомлять вас о состоянии вашего заказа.\nОстались вопросы или возникли проблемы? - lizzaspizza@gmail.com'''
        return text


def get_order_message(basket: dict, total: int, order_type, pay_type, order_id, email, shop_address, home_address) -> str:
        order_type = 'Доставка на дом' if order_type == '1' else f'В заведении, по адресу {shop_address}'
        pay_type = 'Онлайн' if pay_type == '1' else 'оффлайн'
        shipping = 'Доставка по адресу⬇️⬇️⬇️' if home_address != (0, 0) else ''
        message = f'Поступил заказ на сумму {total} руб.'
        for key, value in basket.items():
                message += f'\n{key}: {value} шт.'
        message += f'''\nНомер заказа: {order_id}\n
Тип получения заказа: {order_type}\nТип оплаты: {pay_type}\n
Почта покупателя: {email[0]}\n{shipping}'''
        return message


start = 'Привет!\nРад\tприветсвовать\tвас\tв\tнашей\tпиццерии!\n' \
        'Здесь\tвы\tможете\tзадать\tкакие-то\tвопросы\tили\tже\tзаказать\tпиццу.'
registration_1 = 'Для\tначала\tвам\tнужно\tзарегистрироваться\t' \
                'Пришлите\tсвою\tрабочую\tпочту,\tчтобы\tмы\tмогли\tдержать\tсвязь\tс\tвами'
registration_2 = 'Хорошо\n' \
                'Пришлите\tсвою\tсвою\tдату\tрождения\tв\tформате:\tЧЧММГГГГ' \
                'Мы\tбудем\tприсылать\tбонусы\tна\tэту\tдату)'
registration_3 = '''Отлично\n
Теперь\tпришлите\tсвою\tосновную\tгеолокацию,\она\tавтоматически\tбудет\tопределяться\t
при\tвашем\tзаказе(её\tможно\tбудет\tпоменять)'''


redact_pizza_text = {
        'name': 'Придумайте название для вашей пиццы',
        'price': 'Определите цену вашей пиццы',
        'descr': 'Придумайте опиание для пиццы',
        'image': 'Пришлите <b>ссылку</b> на фотографию данной пиццы'
}
